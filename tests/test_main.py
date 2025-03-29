from flask_socketio import test_client
from typing import List, Dict, Any


def test_connect(socket_client: test_client.SocketIOTestClient) -> None:
    assert socket_client.is_connected()


def test_message_handler(socket_client: test_client.SocketIOTestClient) -> None:
    socket_client.emit('message', 'Hello World')
    received: List[Dict[str, Any]] = socket_client.get_received()

    assert len(received) == 1
    assert received[0]['name'] == 'message'
    assert 'Hello World' in received[0]['args']
