from __future__ import annotations

import logging
import string
from abc import ABC, abstractmethod
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, Literal, TypeVar

import numpy as np
import torch
from lightning.pytorch import Trainer
from lightning.pytorch.callbacks import Checkpoint
from typing_extensions import override

from ..._checkpoint.metadata import CheckpointMetadata, _generate_checkpoint_metadata
from ..._checkpoint.saver import link_checkpoint, remove_checkpoint
from ..base import CallbackConfigBase

if TYPE_CHECKING:
    from ...trainer._config import TrainerConfig


log = logging.getLogger(__name__)


class _FormatDict(dict):
    """A dictionary that returns an empty string for missing keys when formatting."""

    def __missing__(self, key):
        log.debug(
            f"Missing format key '{key}' in checkpoint filename, using empty string"
        )
        return ""


def _get_checkpoint_metadata(dirpath: Path) -> list[CheckpointMetadata]:
    """Get all checkpoint metadata from a directory."""
    return [
        CheckpointMetadata.from_file(p)
        for p in dirpath.glob(f"*{CheckpointMetadata.PATH_SUFFIX}")
        if p.is_file() and not p.is_symlink()
    ]


def _sort_checkpoint_metadata(
    metas: list[CheckpointMetadata],
    key_fn: Callable[[CheckpointMetadata], Any],
    reverse: bool = False,
) -> list[CheckpointMetadata]:
    """Sort checkpoint metadata by the given key function."""
    return sorted(metas, key=key_fn, reverse=reverse)


def _remove_checkpoints(
    trainer: Trainer,
    dirpath: Path,
    metas_to_remove: list[CheckpointMetadata],
) -> None:
    """Remove checkpoint files and their metadata."""
    for meta in metas_to_remove:
        ckpt_path = dirpath / meta.checkpoint_filename
        if not ckpt_path.exists():
            log.warning(
                f"Checkpoint file not found: {ckpt_path}\n"
                "Skipping removal of the checkpoint metadata."
            )
            continue

        remove_checkpoint(trainer, ckpt_path, metadata=True)
        log.debug(f"Removed checkpoint: {ckpt_path}")


def _update_symlink(
    dirpath: Path,
    symlink_path: Path | None,
    sort_key_fn: Callable[[CheckpointMetadata], Any],
    sort_reverse: bool,
) -> None:
    """Update symlink to point to the best checkpoint."""
    if symlink_path is None:
        return

    # Get all checkpoint metadata after any removals
    remaining_metas = _get_checkpoint_metadata(dirpath)

    if remaining_metas:
        # Sort by the key function
        remaining_metas = _sort_checkpoint_metadata(
            remaining_metas, sort_key_fn, sort_reverse
        )

        # Link to the best checkpoint
        best_meta = remaining_metas[0]
        best_filepath = dirpath / best_meta.checkpoint_filename
        link_checkpoint(best_filepath, symlink_path, metadata=True)
        log.debug(f"Updated symlink {symlink_path.name} -> {best_filepath.name}")
    else:
        log.warning(f"No checkpoints found in {dirpath} to create symlink.")


class BaseCheckpointCallbackConfig(CallbackConfigBase, ABC):
    dirpath: str | Path | None = None
    """Directory path to save the checkpoint file."""

    filename: str | None = None
    """Checkpoint filename. This must not include the extension.
    If None, the default filename will be used."""

    save_weights_only: bool = False
    """Whether to save only the model's weights or the entire model object."""

    save_symlink: bool = True
    """Whether to create a symlink to the saved checkpoint."""

    topk: int | Literal["all"] = 1
    """The number of checkpoints to keep."""

    @abstractmethod
    def create_checkpoint(
        self,
        trainer_config: TrainerConfig,
        dirpath: Path,
    ) -> "CheckpointBase | None": ...

    @override
    def create_callbacks(self, trainer_config):
        dirpath = Path(
            self.dirpath
            or trainer_config.directory.resolve_subdirectory(
                trainer_config.id, "checkpoint"
            )
        )

        if (callback := self.create_checkpoint(trainer_config, dirpath)) is not None:
            yield callback


TConfig = TypeVar("TConfig", bound=BaseCheckpointCallbackConfig, infer_variance=True)


class CheckpointBase(Checkpoint, ABC, Generic[TConfig]):
    def __init__(self, config: TConfig, dirpath: Path):
        super().__init__()

        self.config = config
        self.dirpath = dirpath / self.name()
        self.dirpath.mkdir(parents=True, exist_ok=True)
        self.symlink_dirpath = dirpath

    @abstractmethod
    def default_filename(self) -> str: ...

    @abstractmethod
    def name(self) -> str: ...

    def extension(self) -> str:
        return ".ckpt"

    @abstractmethod
    def topk_sort_key(self, metadata: CheckpointMetadata) -> Any: ...

    @abstractmethod
    def topk_sort_reverse(self) -> bool: ...

    def symlink_path(self):
        if not self.config.save_symlink:
            return None

        return self.symlink_dirpath / f"{self.name()}{self.extension()}"

    def resolve_checkpoint_path(self, current_metrics: dict[str, Any]) -> Path:
        if (filename := self.config.filename) is None:
            filename = self.default_filename()

        # Extract all field names from the format string
        field_names = [
            fname for _, fname, _, _ in string.Formatter().parse(filename) if fname
        ]

        # Filter current_metrics to only include keys that are in the format string
        format_dict = {k: v for k, v in current_metrics.items() if k in field_names}

        try:
            formatted_filename = filename.format(**format_dict)
        except KeyError as e:
            log.warning(
                f"Missing key {e} in {filename=} with {format_dict=}. Using default values."
            )
            # Provide a simple fallback for missing keys
            formatted_filename = string.Formatter().vformat(
                filename, (), _FormatDict(format_dict)
            )

        return self.dirpath / f"{formatted_filename}{self.extension()}"

    def current_metrics(self, trainer: Trainer) -> dict[str, Any]:
        current_metrics: dict[str, Any] = {
            "epoch": trainer.current_epoch,
            "step": trainer.global_step,
        }

        for name, value in trainer.callback_metrics.items():
            match value:
                case torch.Tensor() if value.numel() == 1:
                    value = value.detach().cpu().item()
                case np.ndarray() if value.size == 1:
                    value = value.item()
                case _:
                    pass

            current_metrics[name] = value

        log.debug(
            f"Current metrics: {current_metrics}, {trainer.callback_metrics=}, {trainer.logged_metrics=}"
        )
        return current_metrics

    def save_checkpoints(self, trainer: Trainer):
        log.debug(
            f"{type(self).__name__}.save_checkpoints() called at {trainer.current_epoch=}, {trainer.global_step=}"
        )
        # Also print out the current stack trace for debugging
        if log.isEnabledFor(logging.DEBUG):
            import traceback

            stack = traceback.extract_stack()
            log.debug(f"Stack trace: {''.join(traceback.format_list(stack))}")

        if self._should_skip_saving_checkpoint(trainer):
            return

        from ...trainer import Trainer as NTTrainer

        if not isinstance(trainer, NTTrainer):
            raise TypeError(
                f"Trainer must be an instance of {NTTrainer.__name__}, "
                f"but got {type(trainer).__name__}"
            )

        current_metrics = self.current_metrics(trainer)
        filepath = self.resolve_checkpoint_path(current_metrics)

        # Get all existing checkpoint metadata
        existing_metas = _get_checkpoint_metadata(self.dirpath)

        # Determine which checkpoints to remove
        to_remove: list[CheckpointMetadata] = []
        should_save = True

        # Check if we should save this checkpoint
        if (topk := self.config.topk) != "all" and len(existing_metas) >= topk:
            # Generate hypothetical metadata for the current checkpoint
            hypothetical_meta = _generate_checkpoint_metadata(
                trainer=trainer,
                checkpoint_path=filepath,
                metadata_path=filepath.with_suffix(CheckpointMetadata.PATH_SUFFIX),
                compute_checksum=False,
            )

            # Add the hypothetical metadata to the list and sort
            metas = _sort_checkpoint_metadata(
                [*existing_metas, hypothetical_meta],
                self.topk_sort_key,
                self.topk_sort_reverse(),
            )

            # If the hypothetical metadata is not in the top-k, skip saving
            if hypothetical_meta not in metas[:topk]:
                log.debug(
                    f"Skipping checkpoint save: would not make top {topk} "
                    f"based on {self.topk_sort_key.__name__}"
                )
                should_save = False
            else:
                # Determine which existing checkpoints to remove
                to_remove = metas[topk:]
                assert hypothetical_meta not in to_remove, (
                    "Hypothetical metadata should not be in the to_remove list."
                )
                log.debug(
                    f"Removing checkpoints: {[meta.checkpoint_filename for meta in to_remove]} "
                    f"and saving the new checkpoint: {hypothetical_meta.checkpoint_filename}"
                )

        # Only save if it would make it into the top-k
        if should_save:
            # Save the new checkpoint
            trainer.save_checkpoint(
                filepath,
                weights_only=self.config.save_weights_only,
            )

            if trainer.is_global_zero:
                # Remove old checkpoints that should be deleted
                if to_remove:
                    _remove_checkpoints(trainer, self.dirpath, to_remove)

                # Update the symlink to point to the best checkpoint
                _update_symlink(
                    self.dirpath,
                    self.symlink_path(),
                    self.topk_sort_key,
                    self.topk_sort_reverse(),
                )

        # Barrier to ensure all processes have completed checkpoint operations
        trainer.strategy.barrier()

    def _should_skip_saving_checkpoint(self, trainer: Trainer) -> bool:
        from lightning.pytorch.trainer.states import TrainerFn

        return (
            bool(
                getattr(trainer, "fast_dev_run", False)
            )  # disable checkpointing with fast_dev_run
            or trainer.state.fn
            != TrainerFn.FITTING  # don't save anything during non-fit
            or trainer.sanity_checking  # don't save anything during sanity check
        )
