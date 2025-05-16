# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: May 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // LIBRARY IMPORT // ===============

from sqlmodel import (
    Session,
    select
)
from fastapi import (
    status,
    HTTPException
)

# =============== // MODULE IMPORT // ===============

import modules.db as db


def validate_portfolio_exists(
    portfolio_id: str,
    session: Session
):
    portfolio = session.exec(
        select(
            db.schema.Portfolios
        ).where(
            db.schema.Portfolios.id == portfolio_id
        )
    ).first()
    if portfolio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Portfolio with id {portfolio_id} not found"
        )
    return portfolio


def validate_stock_exists(
    stock_id: str,
    session: Session
):
    stock = session.exec(
        select(db.schema.Stocks).where(db.schema.Stocks.id == stock_id)
    ).first()
    if stock is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Stock with id {stock_id} not found"
        )
    return stock
