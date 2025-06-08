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
    get_session
)

# =============== // ROUTER // ===============

router: APIRouter = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
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


@router.get("/{user_id}", response_model=db.schema.UserRead)
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
