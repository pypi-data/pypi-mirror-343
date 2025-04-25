from __future__ import annotations

import logging
from pathlib import Path

import nshconfig as C

from .callbacks.directory_setup import DirectorySetupCallbackConfig
from .loggers import LoggerConfig

log = logging.getLogger(__name__)


class DirectoryConfig(C.Config):
    project_root: Path | None = None
    """
    Root directory for this project.

    This isn't specific to the run; it is the parent directory of all runs.
    """

    logdir_basename: str = "nshtrainer"
    """Base name for the log directory."""

    setup_callback: DirectorySetupCallbackConfig = DirectorySetupCallbackConfig()
    """Configuration for the directory setup PyTorch Lightning callback."""

    def resolve_run_root_directory(self, run_id: str) -> Path:
        if (project_root_dir := self.project_root) is None:
            project_root_dir = Path.cwd()

        # The default base dir is $CWD/{logdir_basename}/{id}/
        base_dir = project_root_dir / self.logdir_basename
        base_dir.mkdir(exist_ok=True)

        # Add a .gitignore file to the {logdir_basename} directory
        #   which will ignore all files except for the .gitignore file itself
        gitignore_path = base_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.touch()
            gitignore_path.write_text("*\n")

        base_dir = base_dir / run_id
        base_dir.mkdir(exist_ok=True)

        return base_dir

    def resolve_subdirectory(self, run_id: str, subdirectory: str) -> Path:
        # The subdir will be $CWD/{logdir_basename}/{id}/{log, stdio, checkpoint, activation}/
        if (subdir := getattr(self, subdirectory, None)) is not None:
            assert isinstance(subdir, Path), (
                f"Expected a Path for {subdirectory}, got {type(subdir)}"
            )
            return subdir

        dir = self.resolve_run_root_directory(run_id)
        dir = dir / subdirectory
        dir.mkdir(exist_ok=True)
        return dir

    def _resolve_log_directory_for_logger(self, run_id: str, logger: LoggerConfig):
        if (log_dir := logger.log_dir) is not None:
            return log_dir

        # Save to {logdir_basename}/{id}/log/{logger name}
        log_dir = self.resolve_subdirectory(run_id, "log")
        log_dir = log_dir / logger.resolve_logger_dirname()
        # ^ NOTE: Logger must have a `name` attribute, as this is
        # the discriminator for the logger registry
        log_dir.mkdir(exist_ok=True)

        return log_dir
