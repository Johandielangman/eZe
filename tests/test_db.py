# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


# =============== // LIBRARY IMPORTS // ===============

import time
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from backend.modules.db.schema import (
    Stocks,
    User,
    Portfolios,
    Holdings
)


def test_create_basic_stock(sqlite_engine: Engine):
    with Session(sqlite_engine) as s:
        new_stock: Stocks = Stocks(
            ticker="SOL"
        )
        s.add(new_stock)
        s.commit()


def test_create_user_and_portfolios(sqlite_engine: Engine):
    with Session(sqlite_engine) as s:
        user = User(name="Alice", surname="Smith")
        s.add(user)

        rsa_portfolio: Portfolios = Portfolios(name="RSA", user=user)
        s.add(rsa_portfolio)
        usa_portfolio: Portfolios = Portfolios(name="USA", user=user)
        s.add(usa_portfolio)

        sol_stock: Stocks = Stocks(
            ticker="SOL"
        )
        s.add(sol_stock)
        bat_stock: Stocks = Stocks(
            ticker="BAT"
        )
        s.add(bat_stock)

        holding_a: Holdings = Holdings(
            purchased_at=time.time(),
            portfolio=rsa_portfolio,
            stock=bat_stock
        )
        s.add(holding_a)

        s.commit()
