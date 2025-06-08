# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from pathlib import Path
from typing import (
    TYPE_CHECKING
)

# =============== // MODULE IMPORT // ===============

from modules.utils.date import get_today
import constants as c

# =============== // SETUP // ===============

if TYPE_CHECKING:
    from loguru import Logger


# =============== // LOGGER SETUP // ===============

LOG_FORMAT: str = "{time} | {level} | {name}:{module}:{function}:{line} | {message}"


def setup_debug_log(
    logger: 'Logger',
    dir: Path = c.DEBUG_LOGS_DIR
) -> None:
    debug_logs: str = f"eze_debug_{get_today()}.log"
    logger.add(
        f"{dir / debug_logs}",
        level="DEBUG",
        rotation="20 MB",
        retention="7 days",
        compression="zip",
        format=LOG_FORMAT
    )


def setup_error_log(
    logger: 'Logger',
    dir: Path = c.ERROR_LOGS_DIR
) -> None:
    warning_logs: str = f"eze_errors_{get_today()}.log"
    logger.add(
        f"{c.ERROR_LOGS_DIR / warning_logs}",
        level="WARNING",
        rotation="20 MB",
        retention="30 days",
        compression="zip",
        format=LOG_FORMAT
    )


def setup_logger(logger: 'Logger'):
    setup_debug_log(logger)
    setup_error_log(logger)
