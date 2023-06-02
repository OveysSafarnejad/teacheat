# Helpful commands for beginners :)

## 1. generating requirements.txt from requirements.in:

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


# Deploy with k8s

### postgres using helm

1. create postgres-pv and postgres-pvc, then:

```commandline
kubectl apply -f deploy/postgres-pvc.yml
```

2. create postgresql-values.yml from sample.postgresql-values.yml, then run:
```commandline
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install teacheat-postgres -f deploy/postgresql-values.yml bitnami/postgresql
```
