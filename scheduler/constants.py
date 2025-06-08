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
import tempfile
import os

# =============== // LIBRARY IMPORT // ===============

from dotenv import load_dotenv

# =============== // DIRECTORIES // ===============

ROOT: Path = Path(os.getenv("APP_ROOT", str(Path(__file__).resolve(strict=True).parent)))

ASSETS_ROOT: Path = ROOT / "assets"

TEMPLATES_DIR: Path = ASSETS_ROOT / "email_templates"
META_DIR: Path = ASSETS_ROOT / "meta"
TEMP_DIR: Path = Path(tempfile.gettempdir())

# ====> DEBUG LOGS
LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(TEMPLATES_DIR / "logs")))

DEBUG_LOGS_DIR: Path = LOG_DIR / "debug"
DEBUG_LOGS_DIR.mkdir(parents=True, exist_ok=True)

ERROR_LOGS_DIR: Path = LOG_DIR / "error"
ERROR_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =============== // PATHS // ===============

ENV_FILE_PATH: Path = ROOT / ".env"

# =============== // LOAD ENVIRONMENT VARIABLES FROM .ENV // ===============

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(ENV_FILE_PATH))

# =============== // DATE TIME FORMATS // ===============

TZ: str = "Africa/Johannesburg"
DFORMAT_DATE_FOR_FILE: str = "%Y_%m_%d"
LANGUAGE: str = "en-gb"
