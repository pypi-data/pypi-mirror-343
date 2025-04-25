from __future__ import annotations

import logging
from typing import Literal, cast

from lightning.pytorch import LightningModule, Trainer
from lightning.pytorch.callbacks.callback import Callback
from lightning.pytorch.loggers import WandbLogger
from typing_extensions import final, override

from ..util.code_upload import get_code_dir
from .base import CallbackConfigBase, callback_registry

log = logging.getLogger(__name__)


@final
@callback_registry.register
class WandbUploadCodeCallbackConfig(CallbackConfigBase):
    name: Literal["wandb_upload_code"] = "wandb_upload_code"

    enabled: bool = True
    """Enable uploading the code to wandb."""

    def __bool__(self):
        return self.enabled

    @override
    def create_callbacks(self, trainer_config):
        if not self:
            return

        yield WandbUploadCodeCallback(self)


class WandbUploadCodeCallback(Callback):
    def __init__(self, config: WandbUploadCodeCallbackConfig):
        super().__init__()

        self.config = config

    @override
    def setup(self, trainer: Trainer, pl_module: LightningModule, stage: str):
        if not self.config:
            return

        if not trainer.is_global_zero:
            return

        if (
            logger := next(
                (
                    logger
                    for logger in trainer.loggers
                    if isinstance(logger, WandbLogger)
                ),
                None,
            )
        ) is None:
            log.warning("Wandb logger not found. Skipping code upload.")
            return

        if (snapshot_dir := get_code_dir()) is None:
            log.info("No nshrunner snapshot found. Skipping code upload.")
            return

        from wandb.wandb_run import Run

        run = cast(Run, logger.experiment)
        log.info(f"Uploading code from snapshot directory '{snapshot_dir}'")
        run.log_code(str(snapshot_dir.absolute()))
