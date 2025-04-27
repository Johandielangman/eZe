# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORTS // ===============

from typing import (
    Dict,
    List
)

# =============== // MODULE IMPORT // ===============

import constants as c

# =============== // DEFINE METADATA // ===============

tags_metadata: List[Dict] = [
    {
        "name": "users",
        "description": "Manage users in the database!"
    },
]


def read_markdown(file_name: str, extension: str = "md") -> str:
    return (c.META_DIR / f"{file_name}.{extension}").read_text()


fast_api_metadata: Dict = {
    "title": "eZe Finance",
    "description": read_markdown("DESCRIPTION"),
    "summary": read_markdown("SUMMARY", "txt"),
    "version": c.VERSION,
    "terms_of_service": "/terms",
    "openapi_tags": tags_metadata,
    "docs_url": "/api-docs",
    "redoc_url": None,
    "contact": {
        "name": "Johandielangman",
        "email": "jghanekom2@gmail.com",
    },
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/license/mit",
    }
}
