# Kubernetes DevOps FinOps Assignment

## Repository and container links

- Code repository: https://github.com/akshay-zee93/nagp-k8s-devops-finops
- Docker Hub image: https://hub.docker.com/r/akshaynagarro01/fastapi-k8s
- Service API endpoint: http://<your-ingress-host>/records
- Demo video: Add your screen recording link here (Loom, Google Drive, or YouTube)

## Requirement Understanding

This assignment implements a cloud-native, containerized application on Kubernetes with the following goals:

- Deploy a FastAPI application as the service tier.
- Deploy PostgreSQL as the backend data tier with persistent storage.
- Use Kubernetes manifests for networking, configuration, secrets, scaling, and ingress.
- Demonstrate self-healing, persistence, rolling deployment strategy, and FinOps-aware resource sizing.

## Assumptions

- A Kubernetes cluster is already provisioned and accessible through kubectl.
- An ingress controller and DNS or host mapping are available for external access.
- Docker Hub credentials are available to publish the application image.
- The application is expected to serve a simple records endpoint backed by PostgreSQL.

## Solution Overview

### Architecture

- API tier: FastAPI deployment running 4 replicas with a RollingUpdate strategy.
- Database tier: PostgreSQL deployment running 1 replica backed by a PersistentVolumeClaim for data persistence.
- Networking: The API service is exposed through a Kubernetes Service and optionally an Ingress resource.
- Configuration: ConfigMaps and Secrets manage environment variables for the application and database.
- Scaling: HPA scales the FastAPI deployment based on CPU utilization.

### Key project files

- [api.yaml](api.yaml): Deployment and Service for the FastAPI application
- [postgres.yaml](postgres.yaml): PostgreSQL Deployment, PVC, and Service
- [k8s-configmap.yaml](k8s-configmap.yaml): ConfigMap for database host, name, and user
- [k8s-secret.yaml](k8s-secret.yaml): Secret for database credentials
- [hpa.yaml](hpa.yaml): Horizontal Pod Autoscaler for the API tier
- [ingress.yaml](ingress.yaml): External ingress configuration
- [Dockerfile](Dockerfile): Container image definition for the FastAPI app
- [init.sql](init.sql): Initialization script for PostgreSQL sample data

### Build and push Docker image

```bash
docker build -t akshaynagarro01/fastapi-k8s:v1 .
docker push akshaynagarro01/fastapi-k8s:v1
```

### Deploy the application to Kubernetes

```bash
kubectl apply -f k8s-secret.yaml
kubectl apply -f k8s-configmap.yaml
kubectl apply -f postgres.yaml
kubectl apply -f api.yaml
kubectl apply -f hpa.yaml
kubectl apply -f ingress.yaml
```

### Access the API

Once ingress is available, retrieve records with:

```bash
curl http://<your-ingress-host>/records
```

For local verification, use port-forwarding:

```bash
kubectl port-forward svc/fastapi-service 8000:80
curl http://127.0.0.1:8000/records
```

## Justification for the Resources Utilized

- API tier: CPU requests and limits of 100m / 500m and memory requests and limits of 128Mi / 512Mi provide a lightweight baseline while allowing burst capacity during traffic spikes.
- Database tier: A single PostgreSQL replica is sufficient for the assignment workload and keeps operational cost low while preserving durability through a PVC.
- Scaling policy: HPA is configured with a target CPU utilization of 70% and a range of 4 to 10 replicas to balance performance and cost.
- Deployment strategy: RollingUpdate limits disruption during updates and avoids unnecessary downtime.

## FinOps considerations

The solution is designed to reduce unnecessary cloud spend by:

1. Right-sizing CPU and memory requests for the API tier.
2. Using HPA to scale replicas only when workload increases.
3. Running only one PostgreSQL replica with persistent storage instead of over-provisioning a larger database setup.
4. Using rolling deployments to reduce downtime and avoid extra temporary replica overhead.

## Demo recording checklist

The screen recording should include:

- A complete view of all deployed Kubernetes objects such as Deployments, Pods, Services, PVCs, and HPA.
- An API call that retrieves records from PostgreSQL.
- Deleting an API pod and showing that Kubernetes recreates it automatically.
- Deleting the PostgreSQL pod and showing that it recovers while preserving existing data.
- A brief walkthrough of the deployment strategy, persistence, self-healing behavior, and FinOps choices.
