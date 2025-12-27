# Phase 4: Kubernetes Deployment Guide

This guide explains how to deploy the Todo Chatbot application to Kubernetes using Minikube and Helm in GitHub Codespaces.

---

## Prerequisites

- GitHub Codespaces (or local machine with Docker)
- kubectl, Minikube, and Helm installed
- Docker images built

---

## Quick Start

### 1. Setup Environment

```bash
# Clone the repository
git clone https://github.com/FarazAliAhmed/todo-list.git
cd todo-list

# Run setup script (installs kubectl, minikube, helm)
chmod +x k8s/setup-codespace.sh
./k8s/setup-codespace.sh
```

### 2. Build Docker Images

```bash
# Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Verify images
docker images | grep todo
```

### 3. Configure Secrets

Create a `helm-values.yaml` file with your secrets:

```yaml
secrets:
  databaseUrl: "postgresql://user:password@host/database"
  llmApiKey: "sk-proj-your-openai-key"  # Optional
```

**Important:** Never commit this file to Git! Add it to `.gitignore`.

### 4. Deploy with Helm

```bash
# Validate Helm chart
helm lint ./helm/todo-app

# Create namespace
kubectl create namespace todo-app

# Install application
helm install todo-app ./helm/todo-app -n todo-app -f helm-values.yaml

# Watch pods start
kubectl get pods -n todo-app -w
```

Expected output:
```
NAME                                 READY   STATUS    RESTARTS   AGE
todo-app-backend-xxxxxxxxx-xxxxx    1/1     Running   0          30s
todo-app-frontend-xxxxxxxxx-xxxxx   1/1     Running   0          30s
```

### 5. Access the Application

```bash
# Forward ports to localhost
kubectl port-forward svc/todo-app-backend 8000:8000 -n todo-app &
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app &

# Test backend
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000/api/health

# Open frontend in browser
# Codespaces will show a popup - click "Open in Browser"
# Or manually open: https://YOUR-CODESPACE-URL-3000.preview.app.github.dev
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MINIKUBE CLUSTER                         │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    │
│  │   Ingress   │───▶│   Backend   │───▶│  External   │    │
│  │ Controller  │    │   Service   │    │  Neon DB    │    │
│  └──────┬──────┘    └─────────────┘    └─────────────┘    │
│         │                                                   │
│         │           ┌─────────────┐                        │
│         └──────────▶│  Frontend   │                        │
│                     │   Service   │                        │
│                     └─────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Kubernetes Resources Created

| Resource | Name | Purpose |
|----------|------|---------|
| **Namespace** | `todo-app` | Logical grouping for all resources |
| **Deployment** | `todo-app-backend` | Runs backend FastAPI pods |
| **Deployment** | `todo-app-frontend` | Runs frontend Next.js pods |
| **Service** | `todo-app-backend` | Internal routing to backend (ClusterIP) |
| **Service** | `todo-app-frontend` | Internal routing to frontend (ClusterIP) |
| **ConfigMap** | `todo-app-config` | Non-sensitive environment variables |
| **Secret** | `todo-app-secrets` | Database URL and API keys |
| **Ingress** | `todo-app` | External routing (path-based) |

---

## Useful Commands

### View Resources

```bash
# List all resources
kubectl get all -n todo-app

# Check pod status
kubectl get pods -n todo-app

# Check services
kubectl get svc -n todo-app

# Check ingress
kubectl get ingress -n todo-app
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/todo-app-backend -n todo-app

# Frontend logs
kubectl logs -f deployment/todo-app-frontend -n todo-app

# Specific pod logs
kubectl logs -f <pod-name> -n todo-app
```

### Debug Issues

```bash
# Describe pod (shows events and errors)
kubectl describe pod <pod-name> -n todo-app

# Get pod details
kubectl get pod <pod-name> -n todo-app -o yaml

# Execute command in pod
kubectl exec -it <pod-name> -n todo-app -- /bin/sh
```

### Scale Application

```bash
# Scale backend to 3 replicas
kubectl scale deployment/todo-app-backend --replicas=3 -n todo-app

# Scale frontend to 2 replicas
kubectl scale deployment/todo-app-frontend --replicas=2 -n todo-app

# Verify scaling
kubectl get pods -n todo-app
```

### Update Application

```bash
# Rebuild images
eval $(minikube docker-env)
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Restart deployments (pulls new images)
kubectl rollout restart deployment/todo-app-backend -n todo-app
kubectl rollout restart deployment/todo-app-frontend -n todo-app

# Watch rollout status
kubectl rollout status deployment/todo-app-backend -n todo-app
```

### Upgrade with Helm

```bash
# Update Helm chart
helm upgrade todo-app ./helm/todo-app -n todo-app -f helm-values.yaml

# Rollback to previous version
helm rollback todo-app -n todo-app

# View release history
helm history todo-app -n todo-app
```

---

## Troubleshooting

### Pods in CrashLoopBackOff

**Symptom:** Pod keeps restarting
```bash
kubectl get pods -n todo-app
# Shows: CrashLoopBackOff
```

**Solution:**
```bash
# Check logs for error messages
kubectl logs <pod-name> -n todo-app

# Common causes:
# - Missing DATABASE_URL in secrets
# - Wrong database connection string
# - Missing dependencies in Docker image
```

### ImagePullBackOff

**Symptom:** Can't pull Docker image
```bash
kubectl describe pod <pod-name> -n todo-app
# Shows: Failed to pull image
```

**Solution:**
```bash
# Make sure you built images in Minikube's Docker
eval $(minikube docker-env)
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend
```

### Can't Connect to Minikube

**Symptom:** `Unable to connect to the server`

**Solution:**
```bash
# Check Minikube status
minikube status

# If stopped, restart
minikube start --driver=docker --cpus=2 --memory=4096

# Verify connection
kubectl get nodes
```

### Port-Forward Not Working

**Symptom:** `curl: Failed to connect to localhost`

**Solution:**
```bash
# Kill existing port-forwards
pkill -f "port-forward"

# Start fresh
kubectl port-forward svc/todo-app-backend 8000:8000 -n todo-app &
kubectl port-forward svc/todo-app-frontend 3000:3000 -n todo-app &

# Wait 2 seconds before testing
sleep 2
curl http://localhost:8000/health
```

---

## Environment Variables

### ConfigMap (Non-sensitive)

| Variable | Default | Description |
|----------|---------|-------------|
| `CORS_ORIGINS` | `http://localhost:3000,http://todo.local` | Allowed CORS origins |
| `NEXT_PUBLIC_API_URL` | `http://backend-service:8000` | Backend API URL for frontend |

### Secret (Sensitive)

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes | PostgreSQL connection string (Neon) |
| `LLM_API_KEY` | No | OpenAI API key for AI chat feature |

---

## Cleanup

### Uninstall Application

```bash
# Remove Helm release
helm uninstall todo-app -n todo-app

# Delete namespace (removes all resources)
kubectl delete namespace todo-app
```

### Stop Minikube

```bash
# Stop cluster (saves state)
minikube stop

# Delete cluster (removes everything)
minikube delete
```

---

## Production Considerations

This setup is for **local development and learning**. For production:

1. **Use a real Kubernetes cluster** (AWS EKS, Google GKE, DigitalOcean DOKS)
2. **Use a container registry** (Docker Hub, AWS ECR, GitHub Container Registry)
3. **Add TLS/SSL** for HTTPS
4. **Set up monitoring** (Prometheus, Grafana)
5. **Configure autoscaling** (HPA - Horizontal Pod Autoscaler)
6. **Add resource limits** (prevent resource exhaustion)
7. **Use managed databases** (don't run DB in Kubernetes)
8. **Set up CI/CD** (GitHub Actions, GitLab CI)

---

## Next Steps: Phase 5

Phase 5 will cover:
- Advanced features (recurring tasks, reminders)
- Event-driven architecture with Kafka
- Dapr for microservices
- Deployment to DigitalOcean Kubernetes (DOKS)
- Production monitoring and logging

---

## Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
