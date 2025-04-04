# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORTS // ===============

from typing import (
    Callable,
    Dict,
    Any,
    Optional
)

# =============== // LIBRARY IMPORTS // ===============

import pytest
from validator_collection import checkers

# =============== // MODULE IMPORTS // ===============

import backend.modules.YahooFinance as yf

# =============== // SETUP // ===============


@pytest.mark.parametrize(
    "ticker, validator, validator_kwargs",
    [
        pytest.param(
            ticker,
            checkers.is_numeric,
            {
                "allow_empty": True,
                "minimum": 0
            },
            id=f"{ticker} {suffix}"
        )
        for suffix, ticker in {
            "(pass)": "JSE:SOL",
            "(weird one)": "JSE:GLD",
            "(no result)": "JSE:LOL"
        }.items()
    ]
)
def test_basic_JSE_price(
    ticker: str,
    validator: Callable,
    validator_kwargs: Dict[str, Any]
) -> None:
    value: Optional[float] = yf.price(ticker)
    assert validator(
        value=value,
        **validator_kwargs
    )
