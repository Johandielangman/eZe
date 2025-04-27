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
    TYPE_CHECKING
)

# =============== // LIBRARY IMPORT // ===============

import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient

# =============== // MODULE IMPORT // ===============

import backend.constants as c
from backend.main import app

# =============== // SETUP // ===============


if TYPE_CHECKING:
    from httpx import Response


@pytest.mark.order(1)
def test_ping(test_client: 'TestClient') -> None:
    response: 'Response' = test_client.get("/ping")
    assert response.text == "pong!"


@pytest.mark.order(2)
def test_delete_db():
    if c.DB_PATH_TEST.exists():
        c.DB_PATH_TEST.unlink()


@pytest.mark.order(3)
def test_create_user() -> None:
    engine = create_engine(
        c.DATABASE_URL_TEST, connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def get_session_override():
            return session

        app.dependency_overrides["get_session"] = get_session_override
        app.override_auth = True
        client = TestClient(app)
        response: 'Response' = client.post(
            "/v1/users",
            json={
                "name": "test",
                "surname": "client",
                "email": "johan@client.com",
                "id": "test_id"
            },
            headers={
                "Authorization": "Bearer YOUR_TOKEN_HERE"
            }
        )
        app.dependency_overrides.clear()
        assert response.status_code == 201
