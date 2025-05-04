# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: January 2025

# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORTS // ===============

from typing import (
    Optional
)

# =============== // MODULE IMPORTS // ===============

import modules.datastructures as dc
from modules.stock.stock_analysis import (
    StockAnalysis
)


def price(
    ticker: str
) -> Optional[float]:
    return StockAnalysis(
        ticker=ticker
    ).stock.price


def stock(
    ticker: str
) -> dc.StockData:
    return StockAnalysis(
        ticker=ticker
    ).stock
