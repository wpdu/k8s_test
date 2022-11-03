import socket
from flask import Flask, jsonify, current_app


app = Flask('app')


def get_server_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    return {
        'ip': ip,
        'host name': socket.gethostname()
    }


@app.route('/')
def home():
    current_app.logger.info('home invoke')
    return jsonify(flag='success', info=get_server_info())


if __name__ == "__main__":
    app.logger.info('app server start')
    app.run(host='0.0.0.0', port=5002)