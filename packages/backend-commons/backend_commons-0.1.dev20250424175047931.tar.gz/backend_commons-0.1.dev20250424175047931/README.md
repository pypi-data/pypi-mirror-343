# Common Libraries for Backend Services

Python libraries that can be commonly used by all backend services

## Setup Env

Create a virtual env

```
python3 -m venv backendCommons
source backendCommons/bin/activate
```

## Run Tests with Coverage

It requires pytest and pytest-cov installed.

```
pytest --cov=. --cov-report=xml --cov-report=term

```
