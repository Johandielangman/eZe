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
from sqlmodel import create_engine
from sqlalchemy.engine import Engine


# =============== // MODULE IMPORT // ===============

import backend.modules.db as db


@pytest.fixture
def sqlite_engine() -> Engine:
    """A fixture used to create a blank database using the SQLModel metadata.
    If an old database already exists, it will be removed before creating a new one.
    If the blank database creation is successful, it will be returned as a fixture.

    Returns:
        Engine: The engine used to connect to the blank database
    """
    # ====> Craft the path to the DB
    db_path: Path = Path(__file__).parent.parent / 'local' / 'test_3.db'
    if db_path.exists():
        db_path.unlink()

    # ====> Create an engine
    print(f"File is created at {db_path}")
    engine: Engine = create_engine(f"sqlite:///{db_path}")

    # ====> Create all the tables
    db.schema._create_db_and_tables(engine)

    return engine
