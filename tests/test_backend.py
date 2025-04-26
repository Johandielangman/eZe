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

# =============== // SETUP // ===============


if TYPE_CHECKING:
    from httpx import Response
    from fastapi.testclient import TestClient


def test_ping(test_client: 'TestClient') -> None:
    response: 'Response' = test_client.get("/ping")
    assert response.text == "pong!"


def test_root(test_client: 'TestClient') -> None:
    response: 'Response' = test_client.get("/")
    assert response.text == "Hello from root!"


def test_kinde(test_client: 'TestClient') -> None:
    response: 'Response' = test_client.get("/kinde")
    assert response.text == "pong!"
