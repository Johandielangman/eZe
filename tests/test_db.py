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
import backend.modules.db as db


def test_create_basic_stock(sqlite_engine):
    with Session(sqlite_engine) as s:
        new_stock = db.schema.Stocks(
            ticker="SOL"
        )
        s.add(new_stock)
        s.commit()


def test_create_user_and_portfolios(sqlite_engine):

    # ====> Create a user
    with Session(sqlite_engine) as s:
        user = db.schema.User(
            name="John",
            surname="Smith",
            email="jghanekom2@gmail.com"
        )
        s.add(user)
        s.commit()

    # ====> A user will create a bunch of portfolios
    with Session(sqlite_engine) as s:
        # Updated to use exec() instead of query()
        statement = select(db.schema.User).where(db.schema.User.email == "jghanekom2@gmail.com")
        user = s.exec(statement).first()

        rsa_portfolio = db.schema.Portfolios(
            name="RSA",
            user=user
        )
        s.add(rsa_portfolio)
        s.commit()

    # ====> Add some stocks
    with Session(sqlite_engine) as s:
        sol_stock = db.schema.Stocks(
            ticker="SOL"
        )
        s.add(sol_stock)
        bat_stock = db.schema.Stocks(
            ticker="BAT"
        )
        s.add(bat_stock)
        s.commit()

    with Session(sqlite_engine) as s:
        # Updated to use exec() instead of query()
        user = s.exec(select(db.schema.User).where(db.schema.User.email == "jghanekom2@gmail.com")).first()
        rsa_portfolio = s.exec(select(db.schema.Portfolios).where(db.schema.Portfolios.user_id == user.id)).first()
        bat_stock = s.exec(select(db.schema.Stocks).where(db.schema.Stocks.ticker == "BAT")).first()

        holding_a = db.schema.Holdings(
            purchased_at=time.time(),
            portfolio=rsa_portfolio,
            stock=bat_stock
        )
        s.add(holding_a)

        s.commit()
