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
import json
import tempfile
from pathlib import Path
from typing import (
    Dict
)

# =============== // LIBRARY IMPORT // ===============

from dotenv import load_dotenv

# =============== // DIRECTORIES // ===============

IS_PROD: bool = bool(os.getenv("MODE", "dev").lower() == "production")
ROOT: Path = Path(os.getenv("APP_ROOT", str(Path(__file__).resolve(strict=True).parent)))
ASSETS_ROOT: Path = ROOT / "assets"

TEMP_DIR: Path = Path(tempfile.gettempdir())

GOOGLE_OATH_JSON_PATH: Path = ROOT / "oauth2.json"

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

# =============== // LOGS // ===============

LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(TEMP_DIR / "logs")))

# =============== // GOOGLE EMAIL OAUTH // ===============

GMAIL_EMAIL_ADDRESS: str = os.getenv("GMAIL_EMAIL_ADDRESS")

GOOGLE_OATH: Dict = {
    "email_address": GMAIL_EMAIL_ADDRESS,
    "google_client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "google_client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "google_refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN")
}
GOOGLE_OATH_JSON_PATH.write_text(json.dumps(GOOGLE_OATH, indent=4))
if any([
    not value
    for value in GOOGLE_OATH.keys()
]):
    raise ValueError("Google Oauth variables not set")
