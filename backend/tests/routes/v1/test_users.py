# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: June 2025
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


# =============== // LIBRARY IMPORT // ===============

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlmodel import select


def test_create_user_success(
    api_version: str,
    test_client: TestClient,
    sqlite_session: Session
):
    from modules.db.schema import User  # Adjust import path if needed
    payload = {
        "name": "Johan",
        "surname": "Hanekom",
        "email": "johan@example.com",
        "password": "securePass123"
    }

    response = test_client.post(f"{api_version}/users", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Johan"
    assert data["surname"] == "Hanekom"
    assert data["email"] == "johan@example.com"
    assert "id" in data

    # Now verify the user is actually in the DB
    statement = select(User).where(User.email == "johan@example.com")
    user_in_db = sqlite_session.exec(statement).first()
    assert user_in_db is not None
    assert user_in_db.name == "Johan"
    assert user_in_db.surname == "Hanekom"
