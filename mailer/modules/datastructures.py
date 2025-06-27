# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: June 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from enum import StrEnum

# =============== // LIBRARY IMPORT // ===============

from pydantic import (
    BaseModel,
    Field
)


class Actions(StrEnum):
    CREATE: str = "create"


class RMQMessage(BaseModel):
    timestamp: int
    action: str = Field(
        default=Actions.CREATE,
        examples=[Actions.CREATE]
    )
