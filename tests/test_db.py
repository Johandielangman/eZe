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
    # ====> Create a user
    with Session(sqlite_engine) as s:
        user: User = User(
            name="John",
            surname="Smith",
            username="johanlangman"
        )
        s.add(user)
        s.commit()

    # ====> A user will create a bunch of portfolios
    with Session(sqlite_engine) as s:
        user: User = s.query(User).filter_by(username="johanlangman").first()

        rsa_portfolio: Portfolios = Portfolios(
            name="RSA",
            user=user
        )
        s.add(rsa_portfolio)
        s.commit()

    # ====> Add some stocks
    with Session(sqlite_engine) as s:
        sol_stock: Stocks = Stocks(
            ticker="SOL"
        )
        s.add(sol_stock)
        bat_stock: Stocks = Stocks(
            ticker="BAT"
        )
        s.add(bat_stock)
        s.commit()

    with Session(sqlite_engine) as s:
        user: User = s.query(User).filter_by(username="johanlangman").first()
        rsa_portfolio: Portfolios = s.query(Portfolios).filter_by(user=user).first()
        bat_stock: Stocks = s.query(Stocks).filter_by(ticker="BAT").first()

        holding_a: Holdings = Holdings(
            purchased_at=time.time(),
            portfolio=rsa_portfolio,
            stock=bat_stock
        )
        s.add(holding_a)

        s.commit()
