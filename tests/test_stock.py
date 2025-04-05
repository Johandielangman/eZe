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

import backend.modules.stock as sm

# =============== // SETUP // ===============


@pytest.mark.parametrize(
    "ticker, validator, validator_kwargs",
    [
        pytest.param(
            ticker,
            checkers.is_numeric,
            {
                "allow_empty": False,
                "minimum": 0
            },
            id=f"{ticker} ({suffix})"
        )
        for ticker, suffix in {
            "JSE:ANH": "AbInBev",
            "JSE:BHG": "BHP",
            "JSE:BTI": "BAT",
            "JSE:CPI": "Capitec",
            "JSE:DTC": "Datatec",
            "JSE:DCP": "Dis-Chem",
            "JSE:DSY": "Discovery",
            "JSE:EXX": "Exxaro",
            "JSE:FBR": "Famous Brands",
            "JSE:FSR": "First Rand",
            "JSE:FNBEQF": "FNB Global 1200 FOF",
            "JSE:GPL": "Grand Parade",
            "JSE:INL": "Investec",
            "JSE:KIO": "Kumba Iron ORe",
            "JSE:LEW": "Lewis",
            "JSE:MNP": "Mondi",
            "JSE:MTN": "MTN",
            "JSE:NPN": "Naspers",
            "JSE:GLD": "ABSA NewGold",
            "JSE:PPH": "Pepkor",
            "JSE:PIK": "Pick n Pay",
            "JSE:KST": "PSG",
            "JSE:SAP": "Sappi",
            "JSE:SOL": "Sasol",
            "JSE:STXDIV": "SATRIX Divi Plus",
            "JSE:SHP": "Shoprite",
            "JSE:S32": "South32",
            "JSE:SBK": "Standard Bank",
            "JSE:TRU": "Truworths",
            "JSE:WBC": "WeBuyCars",
            "JSE:WHL": "Woolworths",
        }.items()
    ]
)
def test_everything_i_own_in_rsa(
    ticker: str,
    validator: Callable,
    validator_kwargs: Dict[str, Any]
) -> None:
    value: Optional[float] = sm.price(ticker)
    assert validator(
        value=value,
        **validator_kwargs
    )


@pytest.mark.parametrize(
    "ticker, validator, validator_kwargs",
    [
        pytest.param(
            ticker,
            checkers.is_numeric,
            {
                "allow_empty": False,
                "minimum": 0
            },
            id=f"{ticker} ({suffix})"
        )
        for ticker, suffix in {
            "AMZN": "Amazon",
            "BEP": "Brookfield",
            "NET": "Cloudflare",
            "DKNG": "Draft Kings",
            "RACE": "Ferrari",
            "HPE": "Kewlett Packard",
            "INTC": "Intel",
            "MDT": "Medtonic",
            "META": "Meta",
            "MSFT": "Microsoft",
            "NVDA": "Nvidia",
            "PM": "Phillip Morris",
            "PINS": "Pinterest",
            "CRM": "Salesforce",
            "LUV": "Southwest",
            "SPOT": "Spotify",
            "SBUX": "Starbucks",
            "TSLA": "Tesla",
            "TXN": "Texas Instruments",
            "UPS": "UPS",
            "VOO": "Vanguard",
            "V": "Visa",
            "XPEV": "Xpeng",
        }.items()
    ]
)
def test_everything_i_own_in_usa(
    ticker: str,
    validator: Callable,
    validator_kwargs: Dict[str, Any]
) -> None:
    value: Optional[float] = sm.price(ticker)
    assert validator(
        value=value,
        **validator_kwargs
    )


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
            id=f"{ticker} ({suffix})"
        )
        for ticker, suffix in {
            "johannes": "Johan"
        }.items()
    ]
)
def test_one_that_dont_exist(
    ticker: str,
    validator: Callable,
    validator_kwargs: Dict[str, Any]
) -> None:
    value: Optional[float] = sm.price(ticker)
    assert validator(
        value=value,
        **validator_kwargs
    )
