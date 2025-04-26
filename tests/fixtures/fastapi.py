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

from backend.modules.datastructures.api import TokenPayload
from backend.dependencies import verify_token
from backend.main import app

# =============== // OVERRIDE // ===============


def override_verify_token() -> TokenPayload:
    return TokenPayload(**{
        'application_properties': {
            'kp_app_name': {}
        },
        'aud': [
            'https://happybread.kinde.com/api'
        ],
        'azp': 'fcb42b3db61648d48da2f3a58b9d7d14',
        'exp': 1745783250,
        'gty': [
            'client_credentials'
        ],
        'iat': 1745696850,
        'iss': 'https://happybread.kinde.com',
        'jti': '847aeefe-8c3f-44ea-a162-fc8fde0bcce5',
        'scope': 'create:roles',
        'scp': [],
        'v': '2'
    })


@pytest.fixture
def test_client() -> TestClient:
    app.dependency_overrides[verify_token] = override_verify_token
    client: TestClient = TestClient(app)
    return client
