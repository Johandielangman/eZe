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

import os
from pathlib import Path

# =============== // LIBRARY IMPORT // ===============

from dotenv import load_dotenv

# =============== // DIRECTORIES // ===============

REPOSITORY_ROOT: Path = Path(__file__).resolve(strict=True).parent.parent

BACKEND_ROOT: Path = REPOSITORY_ROOT / "backend"
TESTS_ROOT: Path = REPOSITORY_ROOT / "tests"

MAILER_DIR: Path = BACKEND_ROOT / "modules" / "mailer"
TEMPLATES_DIR: Path = MAILER_DIR / "templates"
TESTS_LOCAL_DIR: Path = TESTS_ROOT / "local"

# ====> DEBUG LOGS
LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(TESTS_LOCAL_DIR / "logs")))

DEBUG_LOGS_DIR: Path = LOG_DIR / "debug"
DEBUG_LOGS_DIR.mkdir(parents=True, exist_ok=True)

ERROR_LOGS_DIR: Path = LOG_DIR / "error"
ERROR_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =============== // PATHS // ===============

ENV_FILE_PATH: Path = BACKEND_ROOT / ".env"

# =============== // LOAD ENVIRONMENT VARIABLES FROM .ENV // ===============

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(ENV_FILE_PATH))

# =============== // VERSION // ===============

VERSION: str = "v" + (
    REPOSITORY_ROOT / "version.txt"
).read_text(
    encoding="utf-8"
).strip()


# =============== // KINDE // ===============

KINDE_CLIENT_ID: str = os.getenv("KINDE_CLIENT_ID")
KINDE_CLIENT_SECRET: str = os.getenv("KINDE_CLIENT_SECRET")
KINDE_ISSUER_URL: str = os.getenv("KINDE_ISSUER_URL")

if any([
    not KINDE_CLIENT_ID,
    not KINDE_CLIENT_SECRET,
    not KINDE_ISSUER_URL,
]):
    raise ValueError(
        "KINDE_CLIENT_ID, KINDE_CLIENT_SECRET, and KINDE_ISSUER_URL must be set in the environment variables."
    )
