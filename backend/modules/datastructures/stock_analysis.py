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
    Optional
)

# =============== // LIBRARY IMPORTS // ===============

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

# =============== // DATA CLASS DEFINITIONS // ===============


class StockData(BaseModel):
    price: Optional[float] = Field(default=None, alias="p")
    change: Optional[float] = Field(default=None, alias="c")
    change_pct: Optional[float] = Field(default=None, alias="cp")
    previous_close: Optional[float] = Field(default=None, alias="cl")
    open_: Optional[float] = Field(default=None, alias="o")
    high: Optional[float] = Field(default=None, alias="h")
    low: Optional[float] = Field(default=None, alias="l")
    volume: Optional[float] = Field(default=None, alias="v")
    last_update_datetime_str: Optional[str] = Field(default=None, alias="u")
    last_update_date: Optional[str] = Field(default=None, alias="td")
    last_update_timestamp: Optional[int] = Field(default=None, alias="ts")
    high_52: Optional[float] = Field(default=None, alias="h52")
    low_52: Optional[float] = Field(default=None, alias="l52")
    exchange: Optional[str] = Field(default=None, alias="ex")
    market_state: Optional[str] = Field(default=None, alias="ms")
    market_state_2: Optional[str] = Field(default=None, alias="fms")

    model_config = ConfigDict(
        extra='ignore',
    )
