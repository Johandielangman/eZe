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
from pathlib import Path
from typing import (
    Dict
)

# =============== // LIBRARY IMPORT // ===============

from dotenv import load_dotenv
from kinde_sdk.kinde_api_client import GrantType

# =============== // DIRECTORIES // ===============

REPOSITORY_ROOT: Path = Path(__file__).resolve(strict=True).parent.parent

BACKEND_ROOT: Path = REPOSITORY_ROOT / "backend"
TESTS_ROOT: Path = REPOSITORY_ROOT / "tests"
ASSETS_ROOT: Path = BACKEND_ROOT / "assets"

MAILER_DIR: Path = BACKEND_ROOT / "modules" / "mailer"
TEMPLATES_DIR: Path = ASSETS_ROOT / "email_templates"
META_DIR: Path = ASSETS_ROOT / "meta"
TESTS_LOCAL_DIR: Path = TESTS_ROOT / "local"

# ====> DEBUG LOGS
LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(TESTS_LOCAL_DIR / "logs")))

DEBUG_LOGS_DIR: Path = LOG_DIR / "debug"
DEBUG_LOGS_DIR.mkdir(parents=True, exist_ok=True)

ERROR_LOGS_DIR: Path = LOG_DIR / "error"
ERROR_LOGS_DIR.mkdir(parents=True, exist_ok=True)

# =============== // PATHS // ===============

ENV_FILE_PATH: Path = BACKEND_ROOT / ".env"
GOOGLE_OATH_JSON_PATH: Path = MAILER_DIR / "oauth2.json"
VERSION_FILE_PATH: Path = REPOSITORY_ROOT / "version.txt"

# =============== // LOAD ENVIRONMENT VARIABLES FROM .ENV // ===============

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(ENV_FILE_PATH))

# =============== // VERSION // ===============

VERSION: str = "v" + VERSION_FILE_PATH.read_text(
    encoding="utf-8"
).strip()


# =============== // KINDE // ===============

KINDE_CLIENT_ID: str = os.getenv("KINDE_CLIENT_ID")
KINDE_CLIENT_SECRET: str = os.getenv("KINDE_CLIENT_SECRET")
KINDE_ISSUER_URL: str = os.getenv("KINDE_ISSUER_URL")
KINDE_GRANT_TYPE = GrantType.CLIENT_CREDENTIALS

if any([
    not KINDE_CLIENT_ID,
    not KINDE_CLIENT_SECRET,
    not KINDE_ISSUER_URL,
]):
    raise ValueError(
        "KINDE_CLIENT_ID, KINDE_CLIENT_SECRET, and KINDE_ISSUER_URL must be set in the environment variables."
    )

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

# =============== // DATE TIME FORMATS // ===============

TZ: str = "Africa/Johannesburg"
DFORMAT_DATE_FOR_FILE: str = "%Y_%m_%d"
LANGUAGE: str = "en-gb"
