# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: May 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~

# =============== // STANDARD IMPORT // ===============

from typing import (
    List,
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
    prefix="/holdings",
    tags=["holdings"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)


# =============== // ROUTES // ===============

@router.get(
    "/",
    response_model=List[db.schema.HoldingRead]
)
def read_all_holdings(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    holdings: List[db.schema.HoldingRead] = session.exec(
        select(
            db.schema.Holdings
        ).offset(
            skip
        ).limit(
            limit
        )
    ).all()
    return holdings


@router.get(
    "/{portfolio_id}",
    response_model=List[db.schema.HoldingRead]
)
def read_holdings_from_portfolio(
    portfolio_id: str,
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    holdings: List[db.schema.HoldingRead] = session.exec(
        select(
            db.schema.Holdings
        ).where(
            db.schema.Holdings.portfolio_id == portfolio_id
        ).offset(
            skip
        ).limit(
            limit
        )
    ).all()
    return holdings


@router.get(
    "/{portfolio_id}/{stock_id}",
    response_model=db.schema.HoldingRead
)
def read_holding(
    portfolio_id: str,
    stock_id: str,
    session: Session = Depends(get_session)
):
    holding: db.schema.HoldingRead = session.exec(
        select(
            db.schema.Holdings
        ).where(
            db.schema.Holdings.portfolio_id == portfolio_id
        ).where(
            db.schema.Holdings.stock_id == stock_id
        )
    ).first()

    if holding is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Holding with portfolio_id {portfolio_id} and stock_id {stock_id} not found"
        )

    return holding


@router.post(
    "/",
    response_model=db.schema.HoldingRead,
    status_code=status.HTTP_201_CREATED
)
def create_holding(
    holding: db.schema.HoldingCreate,
    session: Session = Depends(get_session)
):
    db_holding = db.schema.Holdings.model_validate(holding)

    # ====> SOME VALIDATIONS FOR BETTER COMMUNICATION WITH THE USER

    db.utils.validate_portfolio_exists(
        session=session,
        portfolio_id=holding.portfolio_id
    )

    db.utils.validate_stock_exists(
        session=session,
        stock_id=holding.stock_id
    )

    # ====> CHECK TO SEE IF THE HOLDING COMBINATION DOES NOT ALREADY EXIST

    existing_holding = session.exec(
        select(
            db.schema.Holdings
        ).where(
            db.schema.Holdings.portfolio_id == holding.portfolio_id
        ).where(
            db.schema.Holdings.stock_id == holding.stock_id
        )
    ).first()

    if existing_holding is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Holding already exists"
        )

    # ====> AT THIS POINT, ALL IS GOOD -- CREATE THE HOLDING

    session.add(db_holding)
    session.commit()
    session.refresh(db_holding)
    return db_holding
