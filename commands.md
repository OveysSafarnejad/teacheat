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

1. Start minikube cluster
```commandline
minikube start --driver=docker
```

2. Create app-configmap.yml from sample.app-configmap.yml, and:
```commandline
kubectl apply -f deploy/app-configmap.yml
```

3. Create app-secrets.yml from sample.app-secrets.yml, and:
```commandline
kubectl apply -f deploy/app-secrets.yml
```

4. Deploy teacheat deployment using:
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

5. Deploy redis, celery worker, celery beat and flower:
```commandline
kubectl apply -f deploy/redis/redis.yml
kubectl apply -f deploy/celery/worker.yml
kubectl apply -f deploy/celery/beat.yml
kubectl apply -f deploy/flower/flower.yml
```

# Create infrastructure using terraform

### terraform install on osx
```commandline
brew tap hashicorp/tap
brew install hashicorp/tap/terraform
```

### Configure aws IAM credential to be accessible from cli
```commandline
aws configure
```

### Initiate infrastructure on amazon
```commandline
terraform fmt
terraform init
terraform plan
terraform apply
```


### After authenticated within awscli
```commandline
aws eks --region eu-central-1 update-kubeconfig --name teacheat-cluster
```

And this command will set up or local kubernetes configuration, so that, it can authenticate with our new eks.

### Install kubernetes dashboard on eks
```commandline
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```

### Create service account that makes us able to connect
```commandline
kubectl apply -f /deploy/dashboard.yml
```

### Create cluster role binding so it gives access to our service account to allow us to login to the dashboard.
```commandline
kubectl create clusterrolebinding serviceaccounts-cluster-admin --clusterrole=cluster-admin --group=system:serviceaccounts
```

### Create dashboard token
```commandline
kubectl create token admin-user --duration 12h -n kubernetes-dashboard

eyJhbGciOiJSUzI1NiIsImtpZCI6ImVlMTVlMDYxOWM1YTM2NTRlMWNjNTRkNDZmYzEyODY1MzY3ZWI5ZDUifQ.eyJhdWQiOlsiaHR0cHM6Ly9rdWJlcm5ldGVzLmRlZmF1bHQuc3ZjIl0sImV4cCI6MTY4NjEwNzc3NiwiaWF0IjoxNjg2MDY0NTc2LCJpc3MiOiJodHRwczovL29pZGMuZWtzLmV1LWNlbnRyYWwtMS5hbWF6b25hd3MuY29tL2lkLzk2NjJGMDRBNTIzRkMzNjA0MUMxM0VCOEI0Mzg3MzMzIiwia3ViZXJuZXRlcy5pbyI6eyJuYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsInNlcnZpY2VhY2NvdW50Ijp7Im5hbWUiOiJhZG1pbi11c2VyIiwidWlkIjoiN2RlM2RhMGEtYzI2OC00YTk5LWEyNWUtOWFmYjNhYzZiODRmIn19LCJuYmYiOjE2ODYwNjQ1NzYsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDprdWJlcm5ldGVzLWRhc2hib2FyZDphZG1pbi11c2VyIn0.q9eGFvITAqRxmtTct8hgaHsE3UCGfR2cqcQB-2B0mnazr3pNlZvetdDycQxVsgp-pwJLj5-oUZsRfx2o5ryXCz9N5mJ4tbp6oxFHsKXx-7jEPMDGbJ5QRsPSSI1wZzFfBJoUYoMNr7qN0A4_zORStIQr3gudV3mzgnWN8HTsqYQ29KqNCZPM2En7cZ-CUHgCeYuOg6o-tzw-22zpY14X8YMaOFGGIC9SknGmxipT_ch-embzFQKgpiA6IOcme1xWYOCkMliAmoa-0vTSx6-u_lRsLdV8xZeCMdOIKgTzQeoIvBGueZcz1LkS0ui2vi3LYhXVvV0LxaDLABVwjjWlnA

```

### Create a proxy for dashboard using:
```commandline
kubectl proxy
```

and dashboard will be available at:
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=default

### 
