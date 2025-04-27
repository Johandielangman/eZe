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

import backend.modules.utils as utils


class TokenPayload(BaseModel):
    application_properties: Optional[dict] = Field(default_factory=dict)
    aud: List[str] = Field(default_factory=list)
    azp: str
    exp: int
    gty: List[str] = Field(default_factory=list)
    iat: int
    iss: str
    jti: str
    scope: str
    scp: List[str] = Field(default_factory=list)
    v: str

    def expires_at(self) -> datetime:
        """JHB timezone-aware expiry datetime"""
        return utils.from_timestamp(self.exp)

    def issued_at(self) -> datetime:
        """JHB timezone-aware issued datetime"""
        return utils.from_timestamp(self.iat)
