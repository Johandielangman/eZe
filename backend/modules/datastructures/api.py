from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone, timedelta


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
        """UTC timezone-aware expiry datetime"""
        return datetime.fromtimestamp(self.exp, tz=timezone.utc)

    def issued_at(self) -> datetime:
        """UTC timezone-aware issued datetime"""
        return datetime.fromtimestamp(self.iat, tz=timezone.utc)

    def expires_at_local(self) -> datetime:
        """Convert expiry time to Johannesburg local time"""
        johannesburg_offset = timedelta(hours=2)
        return self.expires_at().astimezone(timezone(johannesburg_offset))

    def issued_at_local(self) -> datetime:
        """Convert issued time to Johannesburg local time"""
        johannesburg_offset = timedelta(hours=2)
        return self.issued_at().astimezone(timezone(johannesburg_offset))
