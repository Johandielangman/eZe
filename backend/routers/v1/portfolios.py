# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: April 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from typing import (
    List
)

# =============== // LIBRARY IMPORT // ===============

from sqlmodel import (
    Session,
    select
)
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException
)

# =============== // MODULE IMPORT // ===============

import modules.db as db
from dependencies import (
    verify_token,
    get_session
)

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/portfolios",
    tags=["portfolios"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.post(
    "/",
    response_model=db.schema.PortfolioRead,
    status_code=status.HTTP_201_CREATED
)
def create_portfolio(
    portfolio: db.schema.PortfolioCreate,
    session: Session = Depends(get_session)
):
    user: db.schema.User = session.exec(
        select(
            db.schema.User
        ).where(
            db.schema.User.id == portfolio.user_id
        )
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db_portfolio = db.schema.Portfolios.model_validate(portfolio)
    session.add(db_portfolio)
    session.commit()
    session.refresh(db_portfolio)
    return db_portfolio


@router.get(
    "/",
    response_model=List[db.schema.PortfolioRead]
)
def read_portfolios(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    portfolios: List[db.schema.Portfolios] = session.exec(
        select(
            db.schema.Portfolios
        ).offset(
            skip
        ).limit(
            limit
        )
    ).all()
    return portfolios


@router.get(
    "/{portfolio_id}",
    response_model=db.schema.PortfolioReadWithRelations
)
def read_portfolio(
    portfolio_id: str,
    session: Session = Depends(get_session)
):
    portfolio: db.schema.Portfolios = session.exec(
        select(
            db.schema.Portfolios
        ).where(
            db.schema.Portfolios.id == portfolio_id
        )
    ).first()

    if not portfolio:
        raise HTTPException(
            status_code=404,
            detail="Portfolio not found"
        )
    return portfolio
