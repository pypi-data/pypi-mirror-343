from __future__ import annotations

from . import _experimental as _experimental
from . import callbacks as callbacks
from . import data as data
from . import lr_scheduler as lr_scheduler
from . import metrics as metrics
from . import model as model
from . import nn as nn
from . import optimizer as optimizer
from . import profiler as profiler
from .data import LightningDataModuleBase as LightningDataModuleBase
from .metrics import MetricConfig as MetricConfig
from .model import LightningModuleBase as LightningModuleBase
from .trainer import Trainer as Trainer
from .trainer import TrainerConfig as TrainerConfig

try:
    from . import configs as configs
except BaseException:
    pass

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    # For Python <3.8
    from importlib_metadata import (  # pyright: ignore[reportMissingImports]
        PackageNotFoundError,
        version,
    )

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
