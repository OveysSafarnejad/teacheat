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


# Deploy with k8s on minikube

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

### Django app and Reverse proxy

0. Start minikube cluster
```commandline
minikube start --driver=docker
```

1. Create app-configmap.yml from sample.app-configmap.yml, and:
```commandline
kubectl apply -f deploy/app-configmap.yml
```

2. Create app-secrets.yml from sample.app-secrets.yml, and:
```commandline
kubectl apply -f deploy/app-secrets.yml
```

3. Deploy teacheat deployment using:
```commandline
kubectl apply -f deploy/teacheat.yml
```

prerequisites:
```commandline
docker build teacheat-app:latest .
docker build teacheat-proxy:latest proxy/

minikube image load teacheat-app:latest
minikube image load teacheat-proxy:latest
```

4. Deploy redis, celery worker, celery beat and flower:
```commandline
kubectl apply -f deploy/redis/redis.yml
kubectl apply -f deploy/celery/worker.yml
kubectl apply -f deploy/celery/beat.yml
kubectl apply -f deploy/flower/flower.yml
```