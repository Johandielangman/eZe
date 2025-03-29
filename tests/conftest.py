import pytest
from flask import Flask
from flask_socketio import test_client
from typing import Generator
from backend.main import create_app, socketio


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def socket_client(app: Flask) -> Generator[test_client.SocketIOTestClient, None, None]:
    with app.test_client():
        socket_client = socketio.test_client(app)
        assert socket_client.is_connected()
        yield socket_client
        socket_client.disconnect()
