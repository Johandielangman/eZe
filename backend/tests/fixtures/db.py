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

from pathlib import Path
from typing import Generator

# =============== // LIBRARY IMPORTS // ===============

import pytest
from sqlmodel import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import Session

# =============== // MODULE IMPORT // ===============


@pytest.fixture(scope="function")
def sqlite_engine(request: pytest.FixtureRequest) -> Engine:
    """A fixture used to create a blank database using the SQLModel metadata.
    If an old database already exists, it will be removed before creating a new one.
    If the blank database creation is successful, it will be returned as a fixture.

    Returns:
        Engine: The engine used to connect to the blank database
    """
    test_name = request.node.name

    # ====> Craft the path to the DB
    db_dir: Path = Path(__file__).parent.parent / 'local' / 'test_dbs'
    db_dir.mkdir(parents=True, exist_ok=True)

    db_path: Path = db_dir / f"{test_name}.db"
    if db_path.exists():
        db_path.unlink()

    # ====> Ensure the parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # ====> Create an engine
    print(f"File is created at {db_path}")
    engine: Engine = create_engine(f"sqlite:///{db_path}")

    import modules.db as db
    db.schema.create_all(engine)

    return engine


@pytest.fixture(scope="function")
def sqlite_session(sqlite_engine: Engine) -> Generator[Session, None, None]:
    """A fixture that provides a database session using the test SQLite engine."""
    with Session(sqlite_engine) as session:
        yield session
