import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request, jsonify

from celery_config import make_celery

app = Flask(__name__)

celery = make_celery(app)

if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

app.logger.info('Calculate Service Started')


@app.route("/calculate", methods=['POST'])
def calculate():
    req_data = request.json
    x = req_data['number1']
    y = req_data['number2']

    celery.send_task('multiply', kwargs={'x': x, 'y': y})

    return jsonify({'x': x, 'y': y}), 201


@app.route("/callback", methods=['POST'])
def callback():
    req_data = request.json
    result = req_data['result']

    print('Result of callback', result)

    return {'result': result}


if __name__ == "__main__":
    app.run()
