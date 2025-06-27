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
from passlib.context import CryptContext

# =============== // MODULE IMPORT // ===============

from sqlalchemy.engine import URL

# =============== // DIRECTORIES // ===============

IS_PROD: bool = bool(os.getenv("MODE", "dev").lower() == "production")
ROOT: Path = Path(os.getenv("APP_ROOT", str(Path(__file__).resolve(strict=True).parent)))

ASSETS_ROOT: Path = ROOT / "assets"

TEMPLATES_DIR: Path = ASSETS_ROOT / "email_templates"
META_DIR: Path = ASSETS_ROOT / "meta"
TEMP_DIR: Path = Path(tempfile.gettempdir())


# =============== // PATHS // ===============

ENV_FILE_PATH: Path = ROOT / ".env"
DEV_ENV_FILE_PATH: Path = ROOT / ".env.dev"
PROD_ENV_FILE_PATH: Path = ROOT / ".env.prod"
SHARED_ENV_FILE_PATH: Path = ROOT / ".env.shared"

# =============== // LOAD ENVIRONMENT VARIABLES FROM .ENV // ===============

if (
    IS_PROD and
    PROD_ENV_FILE_PATH.exists()
):
    load_dotenv(dotenv_path=str(PROD_ENV_FILE_PATH))

if (
    not IS_PROD and
    DEV_ENV_FILE_PATH.exists()
):
    load_dotenv(dotenv_path=str(DEV_ENV_FILE_PATH))

if SHARED_ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(SHARED_ENV_FILE_PATH))

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(ENV_FILE_PATH))

# =============== // ENVIRONMENT VARIABLES // ===============

POSTGRES_USERNAME: str = str(os.getenv("POSTGRES_USERNAME"))
POSTGRES_PASSWORD: str = str(os.getenv("POSTGRES_PASSWORD"))
POSTGRES_HOST: str = str(os.getenv("POSTGRES_HOST"))
POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))
POSTGRES_DB: str = str(os.getenv("POSTGRES_DB"))

# =============== // DB // ===============

DB_URL: URL = URL.create(
    drivername="postgresql+psycopg2",
    username=POSTGRES_USERNAME,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB
)

# =============== // DEBUG LOGS // ===============

LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(TEMP_DIR / "logs")))

DEBUG_LOGS_DIR: Path = LOG_DIR / "debug"
DEBUG_LOGS_DIR.mkdir(parents=True, exist_ok=True)

ERROR_LOGS_DIR: Path = LOG_DIR / "error"
ERROR_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =============== // DATE TIME FORMATS // ===============

TZ: str = "Africa/Johannesburg"
DFORMAT_DATE_FOR_FILE: str = "%Y_%m_%d"
LANGUAGE: str = "en-gb"

# =============== // AUTH // ===============

JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
if JWT_SECRET_KEY is None:
    raise ValueError("JWT_SECRET_KEY environment variable is not set.")

JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
if JWT_ALGORITHM is None:
    raise ValueError("JWT_ALGORITHM environment variable is not set.")

BCRYPT_CONTEXT = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)
