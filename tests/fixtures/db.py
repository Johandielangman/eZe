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

# =============== // LIBRARY IMPORTS // ===============

import pytest
from sqlmodel import create_engine, SQLModel
from sqlalchemy.engine import Engine


@pytest.fixture
def sqlite_engine() -> Engine:
    """A fixture used to create a blank database using the SQLModel metadata.
    If an old database already exists, it will be removed before creating a new one.
    If the blank database creation is successful, it will be returned as a fixture.

    Returns:
        Engine: The engine used to connect to the blank database
    """
    # ====> Craft the path to the DB
    db_path: Path = Path(__file__).parent.parent / 'local' / 'test.db'
    if db_path.exists():
        db_path.unlink()

    # ====> Create an engine
    print(f"File is created at {db_path}")
    engine: Engine = create_engine(f"sqlite:///{db_path}")

    # ====> Create all the tables
    SQLModel.metadata.create_all(engine)

    return engine
