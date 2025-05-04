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
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

# =============== // ROUTES // ===============


@router.post("/", response_model=db.schema.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: db.schema.UserCreate,
    session: Session = Depends(get_session)
):
    """Create a new user in the database
    You don't _have_ to give a user id! The server can create one FOR you (UUID).
    But it is highly recommended to use the Kinde User Id for this step!
    """
    db_user = db.schema.User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[db.schema.UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Read users from the database
    TODO: Add permissions! Lol.
    """
    users: List[db.schema.UserRead] = session.exec(select(db.schema.User).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=db.schema.UserReadWithPortfolios)
def read_user(user_id: str, session: Session = Depends(get_session)):
    user: db.schema.User = session.exec(
        select(
            db.schema.User
        ).where(
            db.schema.User.id == user_id
        )
    ).first()
    # TODO: Check that the user id matches the one in the token
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user


@router.get("/{user_id}/portfolios", response_model=List[db.schema.PortfolioRead])
def read_user_portfolios(user_id: str, session: Session = Depends(get_session)):
    user: db.schema.User = session.exec(
        select(
            db.schema.User
        ).where(
            db.schema.User.id == user_id
        )
    ).first()

    # TODO: Check that the user id matches the one in the token
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    portfolios: db.schema.PortfolioRead = session.exec(
        select(
            db.schema.Portfolios
        ).where(
            db.schema.Portfolios.user_id == user_id
        )
    ).all()
    return portfolios


@router.put("/{user_id}", response_model=db.schema.UserRead)
def update_user(
    user_id: str,
    user: db.schema.UserBase,
    session: Session = Depends(get_session)
):
    db_user = session.exec(
        select(
            db.schema.User
        ).where(
            db.schema.User.id == user_id
        )
    ).first()

    # TODO: Check that the user id matches the one in the token
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Update user attributes
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    session: Session = Depends(get_session)
):
    db_user = session.exec(
        select(
            db.schema.User
        ).where(
            db.schema.User.id == user_id
        )
    ).first()

    # TODO: Check that the user id matches the one in the token
    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Get all user portfolios to delete first (cascade delete)
    portfolios = session.exec(
        select(
            db.schema.Portfolios
        ).where(
            db.schema.Portfolios.user_id == user_id
        )
    ).all()

    # For each portfolio, delete related holdings and history
    for portfolio in portfolios:
        # Delete holdings
        holdings = session.exec(
            select(
                db.schema.Holdings
            ).where(
                db.schema.Holdings.portfolio_id == portfolio.id
            )
        ).all()
        for holding in holdings:
            session.delete(holding)

        # Delete history
        history_items = session.exec(
            select(
                db.schema.History
            ).where(
                db.schema.History.portfolio_id == portfolio.id
            )
        ).all()
        for history_item in history_items:
            session.delete(history_item)

        # Delete the portfolio
        session.delete(portfolio)

    # Finally delete the user
    session.delete(db_user)
    session.commit()
    return None
