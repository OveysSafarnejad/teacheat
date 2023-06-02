# Helpful commands for beginners :)

## 1. generating requirements.in:

#### install pip-tools

```commandline
python -m  pip install pip-tools
```

#### then compile requirements.in using:
```commandline
pip-compile requirements/requirements.in -o requirements/requirements.txt
```

## 2. generating random secret:
```commandline
    openssl rand -hex 32
```


## 3. runing tests using coverage
```commandline
    coverage run manage.py test
    coverage report
    coverage html
```