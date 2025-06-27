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

from typing import (
    Generator
)

# =============== // LIBRARY IMPORTS // ===============

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


# =============== // OVERRIDE // ===============


@pytest.fixture(scope="function")
def test_client(sqlite_session: Session) -> Generator[TestClient, None, None]:
    from main import app
    from dependencies import get_session
    app.override_auth = True
    app.dependency_overrides[get_session] = lambda: sqlite_session
    client: TestClient = TestClient(app)
    yield client
    app.dependency_overrides.clear()
