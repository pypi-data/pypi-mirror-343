from __future__ import annotations

import logging
from pathlib import Path

log = logging.getLogger(__name__)


def get_code_dir() -> Path | None:
    try:
        import nshrunner as nr

        if (session := nr.Session.from_current_session()) is None:
            log.debug("No active session found. Skipping code upload.")
            return None

        # New versions of nshrunner will have the code_dir attribute
        #   in the session object. We should use that. Otherwise, use snapshot_dir.
        try:
            code_dir = session.code_dir  # type: ignore
        except AttributeError:
            code_dir = session.snapshot_dir

        if code_dir is None:
            log.debug("No code directory found. Skipping code upload.")
            return None

        assert isinstance(code_dir, Path), (
            f"Code directory should be a Path object. Got {type(code_dir)} instead."
        )
        if not code_dir.exists() or not code_dir.is_dir():
            log.warning(
                f"Code directory '{code_dir}' does not exist or is not a directory."
            )
            return None

        return code_dir
    except ImportError:
        log.debug("nshrunner not found. Skipping code upload.")
        return None
