# Flask Microservice 

A basic Flask microservice application. 

## Installation

```bash
git clone git@github.com:barissaslan/flask-microservice.git
```

### Docker Build 

```bash
docker build . -t flask-microservice
```

### Docker Start 

Expose port 8080 for call api.

```bash
docker run -p 8080:8080 flask-microservice
```

### Python Setup

#### Installing Requirements

```bash
pip install -r requirements.txt
```

#### Set Environment Variables

```bash
export CELERY_BROKER_URL='celery broker url'
```

### Python Run

```bash
python3 app.py
```

## Usage

Call calculate endpoint: 

```bash
curl localhost:8080/calculate/3.4/12.7
```


## Run Unit Tests

```bash
python3 tests.py
```
