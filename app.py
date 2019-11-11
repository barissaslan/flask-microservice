from flask import Flask, jsonify

from config import make_celery, set_logger

app = Flask(__name__)

celery = make_celery(app)

set_logger(app)

app.logger.info('Calculate MicroService starting...')


@app.route("/", methods=['GET'])
def home():
    return jsonify({'message': 'hello'})


@app.route("/calculate/<float:x>/<float:y>", methods=['GET'])
def calculate(x: float, y: float) -> jsonify:
    app.logger.info('Received: x: {}, y: {}'.format(x, y))

    celery.send_task('tasks.multiply', kwargs={'x': x, 'y': y})

    app.logger.info('x: {}, y: {} sending to celery application for the calculation.'.format(x, y))

    return jsonify({'x': x, 'y': y})


@app.route("/callback/<float:result>", methods=['GET'])
def callback(result: float) -> jsonify:
    app.logger.info('Result: {}'.format(result))

    return {'result': result}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
