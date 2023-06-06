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
```

### Create a proxy for dashboard using:
```commandline
kubectl proxy
```

and dashboard will be available at:
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/workloads?namespace=default

### Add efs csi driver into the cluster 
```commandline
helm repo add aws-efs-csi-driver https://kubernetes-sigs.github.io/aws-efs-csi-driver/
helm repo update


terraform output -raw efs_csi_sa_role

helm upgrade -i aws-efs-csi-driver aws-efs-csi-driver/aws-efs-csi-driver \
    --namespace kube-system \
    --set image.repository=602401143452.dkr.ecr.eu-central-1.amazonaws.com/eks/aws-efs-csi-driver \
    --set controller.serviceAccount.create=true \
    --set controller.serviceAccount.name=efs-csi-controller-sa\
    --set "controller.serviceAccount.annotations.eks\\.amazonaws\\.com/role-arn"=arn:aws:iam::662355493241:role/teacheat-efs-csi20230606154226219900000001
```


### Authenticate with ecr from within your computer:
```commandline
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 662355493241.dkr.ecr.eu-central-1.amazonaws.com
```



### Build fresh images and push them to ecr
```commandline
docker build -t 662355493241.dkr.ecr.eu-central-1.amazonaws.com/teacheat-app:latest --platform linux/amd64 --compress .
docker build -t 662355493241.dkr.ecr.eu-central-1.amazonaws.com/teacheat-proxy:latest --platform linux/amd64 --compress proxy/
docker push 662355493241.dkr.ecr.eu-central-1.amazonaws.com/teacheat-app:latest
docker push 662355493241.dkr.ecr.eu-central-1.amazonaws.com/teacheat-proxy:latest

```
