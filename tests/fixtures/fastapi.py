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

import pytest
from fastapi.testclient import TestClient

# =============== // MODULE IMPORT // ===============

from backend.main import app

# =============== // OVERRIDE // ===============


@pytest.fixture(scope="session")
def test_client() -> TestClient:
    app.override_auth = True
    client: TestClient = TestClient(app)
    return client
