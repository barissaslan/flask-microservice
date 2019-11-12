FROM python:3.7.4-alpine

COPY . /opt/flask-microservice
WORKDIR /opt/flask-microservice

ENV CELERY_BROKER_URL 'amqp://pyizcpcy:i8-DLpC9lKVReHWD0--fNDPT_QOJzNCJ@orangutan.rmq.cloudamqp.com/pyizcpcy'

RUN pip install -r requirements.txt

EXPOSE 8080

ENTRYPOINT python app.py