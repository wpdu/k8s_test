import os
import socket
from pathlib import Path
from datetime import datetime
from flask import Flask, jsonify, current_app
from pymongo import MongoClient


app = Flask('app')


def get_server_info():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return {
        'ip': ip,
        'host name': socket.gethostname(),
        'time': time_str
    }


@app.route('/')
def home():
    current_app.logger.info('home invoke')
    return jsonify(flag='success', info=get_server_info())


mongo_host = '192.168.31.204' # 'localhost' # 
mongo_port = 27017
mongo_user = 'mongoadmin'
mongo_pswd = 'huawei@P30'
if Path('/.dockerenv').exists():
    mongo_host = os.getenv('MONGO_HOST') #'mongodb-0.mongodb' #
    mongo_port = os.getenv('MONGO_PORT') # 27017
    mongo_user = os.getenv('MONGO_USERNAME') # 
    mongo_pswd = os.getenv('MONGO_PASSWORD') # 
host_url = f'mongodb://{mongo_host}:{mongo_port}'


@app.route('/user/add')
def user_add():
    client = MongoClient(host=host_url, username=mongo_user, password=mongo_pswd)
    test_db = client['test']
    n = test_db['user'].count_documents({})
    n = n + 1
    ret = test_db['user'].insert_one({'_id': n, 'name': 'tom', 'age': 13})
    user = test_db['user'].find_one({'_id': ret.inserted_id})
    return jsonify(flag='success', user=user)


if __name__ == "__main__":
    # print(user_add())
    app.logger.info('app server start')
    app.run(host='0.0.0.0', port=5002)
