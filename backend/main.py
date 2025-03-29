from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

socketio = SocketIO()


@socketio.on('message')
def handle_message(data):
    print('received the following message: ' + data)
    send(f"go yo message! {data}")


@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    emit('json_send', json)


# @socketio.on('my event', namespace='/test')
# def handle_my_custom_namespace_event(json):
#     print('received json: ' + str(json))

@socketio.on('my_event')
def handle_my_custom_event(arg1, arg2, arg3):
    print('received args: ' + arg1 + arg2 + arg3)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    socketio.run(app)
