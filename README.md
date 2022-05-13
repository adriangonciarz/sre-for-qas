# Docker Compose 
## The Stack
This repo contains few apps necessary to train yourself in basic observability (O11Y) skills. Those are:
1. [Prometheus](https://prometheus.io/) - metrics collector and query engine
2. [Grafana]() - visualisations and dashboards
3. Flask API - sample app producing metrics in Prometheus

## Running
Install [Docker](https://docs.docker.com/get-docker/) and [Docker compose](https://docs.docker.com/compose/install/)

In the terminal, got to the root folder of the repository run command `docker-compose up`. Wait a moment to have the stack running. 

Open browser and verify the following addresses
1. `http://localhost:9090` - Prometheus
1. `http://localhost:3000` - Grafana
3. `http://localhost:5000` - Flask API

## Dashboard
You can import predefined API related dashboard to Grafana using the file in `grafana/api_dashboard.json`

# Kubernetes + Keptn
## Kubernetes cluster creation
First, install [kubectl tool](https://kubernetes.io/docs/tasks/tools/#kubectl)

Then run your own Kubernetes cluster. One suggested way to run your own Kuberenetes Cluster is to use [eksctl](https://eksctl.io/).
1. Create AWS account
2. [create new user with Admin role](https://docs.aws.amazon.com/eks/latest/userguide/create-cluster.html) 
3. configure credentials for AWS via `aws configure` 
4. Use `eksctl` to create cluster, for example: 
```
eksctl create cluster \
  --name sre-cluster \
  --node-type t2.large \
  --nodes 2 \
  --version=1.19 \
  --region eu-central-1
```
Warning: AWS resources such as EC2 are paid. Use it carefully, stop/delete when not used. I am not be responsible for any AWS billings:)

Alternatively, you can use small K8S clusters like [minikube](https://minikube.sigs.k8s.io/docs/start/) for free.

## Install Helm
Helm tool will be required to deploy apps using charts, follow [installation steps](https://helm.sh/docs/intro/install/)

## Environment deployment
In order to deploy whole working environment, we will use Helm Charts. If you're not familiar with Helm, this [quickstart](https://helm.sh/docs/intro/quickstart/) can help. 

Open terminal and got o the root directory of this repository. Run `helm install sre-for-qas charts/`. Wait until apps get deployed on your cluster.

## Keptn configuration
It's best to follow the officail Tutorial, but to get up and running:
1. Download latest Keptn client and add it to path
2. Switch kubectl context to your cluster
3. Install Keptn via `./keptn install --endpoint-service-type=ClusterIP`
4. export the following env variables
```
KEPTN_ENDPOINT=http://$(kubectl -n keptn get ingress api-keptn-ingress -ojsonpath='{.spec.rules[0].host}')/api
KEPTN_API_TOKEN=$(kubectl get secret keptn-api-token -n keptn -ojsonpath='{.data.keptn-api-token}' | base64 --decode)
KEPTN_BRIDGE_URL=http://$(kubectl -n keptn get ingress api-keptn-ingress -ojsonpath='{.spec.rules[0].host}')/bridge
``` 
5. Authenticate client `keptn auth --endpoint=$KEPTN_ENDPOINT --api-token=$KEPTN_API_TOKEN`
6. Create keptn project `keptn create project sre-for-qas --shipyard=keptn/shipyard.yaml`
7. Get Keptn basic auth data
```
echo Username: $(kubectl get secret -n keptn bridge-credentials -o jsonpath="{.data.BASIC_AUTH_USERNAME}" | base64 --decode)
echo Password: $(kubectl get secret -n keptn bridge-credentials -o jsonpath="{.data.BASIC_AUTH_PASSWORD}" | base64 --decode)
```
8. Open Keptn UI and see the project created
9. Create service Flask API `keptn create service flask-api --project=sre-for-qas`
9. Add Prometheus service, role and assign Prometheus as monitoring for keptn project
```
helm install -n keptn prometheus-service https://github.com/keptn-contrib/prometheus-service/releases/download/0.8.0/prometheus-service-0.8.0.tgz --wait
kubectl apply -f https://raw.githubusercontent.com/keptn-contrib/prometheus-service/0.8.0/deploy/role.yaml -n monitoring
keptn configure monitoring prometheus --project=sre-for-qas --service=flask-api
```
9. Create the SLI definitions `keptn add-resource --project=sre-for-qas --stage=dev --service=flask-api --resource=keptn/sli.yaml --resourceUri=prometheus/sli.yaml`
9. Create resource `keptn add-resource --project=sre-for-qas --stage=dev --service=flask-api --resource=slo.yaml --resourceUri=slo.yaml`

# API Endpoints
Endpoints of sample API:
- `GET /ok` - always returns 200 HTTP Status Code, supported methods: 
- `POST /echostatus/<status_code>` - returns status code passed in the URL. If you use non-supported status code - returns 400 code
- `GET /areyoulucky` - returns random;ly: 200 or 500 Status Code
- `GET /slow` - returns responses with delay up to 3 seconds

# SLI Definitions
Some Example SLI definitions.

### Error rate for a particular path last 1 minute
```
sum(rate(flask_http_request_duration_seconds_count{status!="200", path="/areyoulucky"}[1m]))/sum(rate(flask_http_request_duration_seconds_count{path="/areyoulucky"}[1m]))
```

### 95th percentile of response time for a particular path last 1 minute
```
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket{status="200", path="/slow"}[1m]))
```

### Average response time last 30 seconds
```
rate(flask_http_request_duration_seconds_sum{status="200"}[30s])/rate(flask_http_request_duration_seconds_count{status="200"}[30s])
```