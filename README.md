# The Stack
This repo contains few apps necessary to train yourself in basic observability (O11Y) skills. Those are:
1. [Prometheus](https://prometheus.io/) - metrics collector and query engine
2. [Grafana]() - visualisations and dashboards
3. Flask API - sample app producing metrics in Prometheus

# Running
Install [Docker](https://docs.docker.com/get-docker/) and [Docker compose](https://docs.docker.com/compose/install/)

In the terminal, got to the root folder of the repository run command `docker-compose up`. Wait a moment to have the stack running. 

Open browser and verify the following addresses
1. `http://localhost:9090` - Prometheus
1. `http://localhost:3000` - Grafana
3. `http://localhost:5000` - Flask API

# Dashboard
You can import predefined API related dashboard to Grafana using the file in `grafana/api_dashboard.json`

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

### 95th percentile of response time for a particualr path last 1 minute
```
histogram_quantile(0.95, rate(flask_http_request_duration_seconds_bucket{status="200", path="/slow"}[1m]))
```

### Average response time last 30 seconds
```
rate(flask_http_request_duration_seconds_sum{status="200"}[30s])/rate(flask_http_request_duration_seconds_count{status="200"}[30s])
```