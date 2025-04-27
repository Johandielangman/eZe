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
    List,
    Optional
)
from datetime import (
    datetime
)

# =============== // LIBRARY IMPORT // ===============

from pydantic import BaseModel, Field

# =============== // MODULE IMPORT // ===============

import modules.utils as utils


class TokenPayload(BaseModel):
    application_properties: Optional[dict] = Field(default_factory=dict)
    aud: Optional[List[str]] = Field(default_factory=list)
    azp: Optional[str] = None
    email: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    iss: Optional[str] = None
    jti: Optional[str] = None
    org_code: Optional[str] = None
    org_name: Optional[str] = None
    permissions: Optional[List[str]] = Field(default_factory=list)
    scope: Optional[str] = None
    scp: List[str] = Field(default_factory=list)
    sub: Optional[str] = None
    v: Optional[str] = None
    token: Optional[str] = None

    def expires_at(self) -> datetime:
        """JHB timezone-aware expiry datetime"""
        return utils.from_timestamp(self.exp)

    def issued_at(self) -> datetime:
        """JHB timezone-aware issued datetime"""
        return utils.from_timestamp(self.iat)


class AccessTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    id_token: str
    refresh_token: str
    scope: str
    token_type: str
    expires_at: int
