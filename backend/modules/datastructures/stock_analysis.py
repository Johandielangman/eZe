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
    Optional,
    ClassVar,
    Any,
    Dict
)

# =============== // LIBRARY IMPORTS // ===============

from sqlmodel import (
    SQLModel,
    Field,
)

# =============== // DATA CLASS DEFINITIONS // ===============


class StockData(SQLModel):
    price: Optional[float] = Field(default=None)
    change: Optional[float] = Field(default=None)
    change_pct: Optional[float] = Field(default=None)
    previous_close: Optional[float] = Field(default=None)
    open_: Optional[float] = Field(default=None)
    high: Optional[float] = Field(default=None)
    low: Optional[float] = Field(default=None)
    volume: Optional[float] = Field(default=None)
    api_last_update_datetime_str: Optional[str] = Field(default=None)
    api_last_update_date: Optional[str] = Field(default=None)
    api_last_update_timestamp: Optional[int] = Field(default=None)
    high_52: Optional[float] = Field(default=None)
    low_52: Optional[float] = Field(default=None)
    exchange: Optional[str] = Field(default=None)
    market_state: Optional[str] = Field(default=None)
    market_state_2: Optional[str] = Field(default=None)

    # Class variable for the API to field mapping
    _api_mapping: ClassVar[Dict[str, str]] = {
        "p": "price",
        "c": "change",
        "cp": "change_pct",
        "cl": "previous_close",
        "o": "open_",
        "h": "high",
        "l": "low",
        "v": "volume",
        "u": "api_last_update_datetime_str",
        "td": "api_last_update_date",
        "ts": "api_last_update_timestamp",
        "h52": "high_52",
        "l52": "low_52",
        "ex": "exchange",
        "ms": "market_state",
        "fms": "market_state_2"
    }

    @classmethod
    def from_api_data(
        cls,
        api_data: Dict[str, Any]
    ) -> 'StockData':
        mapped_data = {}
        for api_key, value in api_data.items():
            if api_key in cls._api_mapping:
                mapped_data[cls._api_mapping[api_key]] = value

        return cls(**mapped_data)
