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
from sqlmodel import Session, select
from backend.modules.datastructures.db import (
    Stocks,
    User,
    Portfolios,
    Holdings
)


def test_create_basic_stock(sqlite_engine):
    with Session(sqlite_engine) as s:
        new_stock = Stocks(
            ticker="SOL"
        )
        s.add(new_stock)
        s.commit()


def test_create_user_and_portfolios(sqlite_engine):
    # ====> Create a user
    with Session(sqlite_engine) as s:
        user = User(
            name="John",
            surname="Smith",
            email="jghanekom2@gmail.com"
        )
        s.add(user)
        s.commit()

    # ====> A user will create a bunch of portfolios
    with Session(sqlite_engine) as s:
        # Updated to use exec() instead of query()
        statement = select(User).where(User.username == "johanlangman")
        user = s.exec(statement).first()

        rsa_portfolio = Portfolios(
            name="RSA",
            user=user
        )
        s.add(rsa_portfolio)
        s.commit()

    # ====> Add some stocks
    with Session(sqlite_engine) as s:
        sol_stock = Stocks(
            ticker="SOL"
        )
        s.add(sol_stock)
        bat_stock = Stocks(
            ticker="BAT"
        )
        s.add(bat_stock)
        s.commit()

    with Session(sqlite_engine) as s:
        # Updated to use exec() instead of query()
        user = s.exec(select(User).where(User.username == "johanlangman")).first()
        rsa_portfolio = s.exec(select(Portfolios).where(Portfolios.user_id == user.id)).first()
        bat_stock = s.exec(select(Stocks).where(Stocks.ticker == "BAT")).first()

        holding_a = Holdings(
            purchased_at=time.time(),
            portfolio=rsa_portfolio,
            stock=bat_stock
        )
        s.add(holding_a)

        s.commit()
