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

# =============== // DIRECTORIES // ===============

ROOT: Path = Path(os.getenv("APP_ROOT", str(Path(__file__).resolve(strict=True).parent)))
ASSETS_ROOT: Path = ROOT / "assets"

MAILER_DIR: Path = ROOT / "modules" / "mailer"

GOOGLE_OATH_JSON_PATH: Path = MAILER_DIR / "oauth2.json"
# =============== // PATHS // ===============

ENV_FILE_PATH: Path = ROOT / ".env"

# =============== // LOAD ENVIRONMENT VARIABLES FROM .ENV // ===============

if ENV_FILE_PATH.exists():
    load_dotenv(dotenv_path=str(ENV_FILE_PATH))
# =============== // GOOGLE EMAIL OAUTH // ===============

GMAIL_EMAIL_ADDRESS: str = os.getenv("GMAIL_EMAIL_ADDRESS")

GOOGLE_OATH: Dict = {
    "email_address": GMAIL_EMAIL_ADDRESS,
    "google_client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "google_client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "google_refresh_token": os.getenv("GOOGLE_REFRESH_TOKEN")
}
print(GOOGLE_OATH)
GOOGLE_OATH_JSON_PATH.write_text(json.dumps(GOOGLE_OATH, indent=4))
if any([
    not value
    for value in GOOGLE_OATH.keys()
]):
    raise ValueError("Google Oauth variables not set")
