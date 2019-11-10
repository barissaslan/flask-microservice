from flask import Flask, request, jsonify

from config import make_celery, set_logger

app = Flask(__name__)

celery = make_celery(app)

set_logger(app)

app.logger.info('Calculate MicroService starting...')


@app.route("/calculate", methods=['POST'])
def calculate():
    req_data = request.json
    x = req_data['x']
    y = req_data['y']

    app.logger.info('Received: x: {}, y: {}'.format(x, y))

    celery.send_task('multiply', kwargs={'x': x, 'y': y})

    app.logger.info('x: {}, y: {} sending to celery application for the calculation.'.format(x, y))

    return jsonify({'x': x, 'y': y})


@app.route("/callback", methods=['POST'])
def callback():
    req_data = request.json
    result = req_data['result']
    x = req_data['x']
    y = req_data['y']

    app.logger.info('Result of the {} * {} = {}'.format(x, y, result))

    return {'result': result, 'x': x, 'y': y}


if __name__ == "__main__":
    app.run()
