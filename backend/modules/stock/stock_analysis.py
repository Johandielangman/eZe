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

import requests

# =============== // MODULE IMPORTS // ===============

from modules.stock.utils import (
    new_session
)
import modules.datastructures as dc


class StockAnalysis:
    base_url: str = "https://stockanalysis.com/api/quotes"

    def __init__(
        self,
        ticker: str
    ) -> None:
        """A class used to extract stock data from a website called https://stockanalysis.com

        Args:
            ticker (str): The stock ticker symbol.
            for example "JSE:SOL" for RSA stocks and "VOO" for USA stocks
        """

        # ====> Parse the ticker
        self.ticker: str = ""
        self.market: str = ""  # USA or RSA
        self.__parse_ticker(ticker=ticker)

        # ====> Create session
        self.session: requests.Session = new_session()
        self.response: Optional[requests.Response] = None

        # ====> Create URL and make request
        self.url: str = ""
        self.__create_url()

        # ====> Make request and parse
        self.stock: dc.StockData = None
        self.__get_stock_data()

    def __parse_ticker(
        self,
        ticker: str
    ) -> None:
        """A function to parse a given ticker.
        From "JSE:SOL" it will determine the market to be "RSA" given the "JSE:" prefix
        and from "VOO", it will determine the market to be "USA"

        Args:
            ticker (str): The stock ticker symbol, as "JSE:SOL" or "VOO"
        """
        # ====> Simple validation
        if (
            not ticker or
            not isinstance(ticker, str)
        ):
            raise ValueError("Invalid ticker provided")

        # ====> Make sure the ticker is uppercase
        ticker = ticker.upper()

        # ====> Determine market
        if ticker.startswith("JSE:"):
            self.market = "RSA"
            self.ticker = ticker.split(":")[1]
            return
        else:
            self.market = "USA"
            self.ticker = ticker
            return

    def __create_url(
        self
    ) -> None:
        """Creates the URL given the market and ticker information
        """
        self.url = self.base_url
        match self.market:
            case "RSA":
                self.url += f"/a/JSE-{self.ticker}"
            case "USA":
                self.url += f"/e/{self.ticker}"
            case _:
                raise ValueError(f"{self.market=} is not a valid value")

    def __get_stock_data(
        self
    ) -> None:
        """Sends a request to `self.url` and parses the result
        """
        try:
            self.response: requests.Response = self.session.get(self.url)
            self.response.raise_for_status()
            self.stock = dc.StockData.from_api_data(self.response.json()['data'])
        except Exception:
            self.stock = dc.StockData()
