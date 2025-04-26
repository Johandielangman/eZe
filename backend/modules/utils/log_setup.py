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

from typing import (
    TYPE_CHECKING
)

# =============== // MODULE IMPORT // ===============

from backend.modules.utils.date import get_today
import backend.constants as c

# =============== // SETUP // ===============

if TYPE_CHECKING:
    from loguru import Logger


# =============== // LOGGER SETUP // ===============


def setup_logger(logger: 'Logger'):
    debug_logs: str = f"debug_{get_today()}.log"
    warning_logs: str = f"errors_{get_today()}.log"
    log_format: str = "{time} | {level} | {name}:{module}:{function}:{line} | {message}"

    logger.add(
        f"{c.DEBUG_LOGS_DIR / debug_logs}",
        level="DEBUG",
        rotation="20 MB",
        retention="7 days",
        compression="zip",
        format=log_format
    )

    logger.add(
        f"{c.ERROR_LOGS_DIR / warning_logs}",
        level="WARNING",
        rotation="20 MB",
        retention="30 days",
        compression="zip",
        format=log_format
    )
