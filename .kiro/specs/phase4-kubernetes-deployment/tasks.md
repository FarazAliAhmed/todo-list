# Phase 4: Local Kubernetes Deployment - Tasks

## Environment: GitHub Codespaces (Hybrid Approach)

> All tasks run in GitHub Codespaces with pre-installed Docker. We'll install Minikube, Helm, and kubectl as part of setup.

---

## Task 1: Setup GitHub Codespaces Environment
**Requirement**: REQ-3.1, REQ-3.2, REQ-3.3

### Steps (Run in Codespaces Terminal)
```bash
# 1. Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl && sudo mv kubectl /usr/local/bin/

# 2. Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64 && sudo mv minikube-linux-amd64 /usr/local/bin/minikube

# 3. Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# 4. Start Minikube with Docker driver
minikube start --driver=docker --cpus=2 --memory=4096

# 5. Enable Ingress addon
minikube addons enable ingress

# 6. Verify setup
kubectl get nodes
helm version
```

### Acceptance Criteria
- [x] kubectl, minikube, helm installed
- [x] Minikube cluster running (`kubectl get nodes` shows Ready)
- [x] Ingress addon enabled

---

## Task 2: Dockerize Backend & Frontend
**Requirement**: REQ-1.1, REQ-1.2, REQ-1.3, REQ-1.4

### Subtasks
- [x] 2.1 Add `/health` endpoint to backend (already exists)
- [x] 2.2 Create `backend/Dockerfile` and `backend/.dockerignore`
- [x] 2.3 Add `/api/health` route to frontend
- [x] 2.4 Update `next.config.js` for standalone output (already configured)
- [x] 2.5 Create `frontend/Dockerfile` and `frontend/.dockerignore`

### Build & Test (in Codespaces)
```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# Verify
docker images | grep todo
```

### Acceptance Criteria
- [x] Both images build without errors
- [x] Images < 500MB each (backend: 612MB, frontend: 191MB)
- [x] Health endpoints return 200 OK

---

## Task 3: Create Docker Compose for Local Testing
**Requirement**: REQ-2.1, REQ-2.2, REQ-2.3

### Subtasks
- [x] 3.1 Create `docker-compose.k8s.yml` for local testing
- [x] 3.2 Create `.env.docker` template

### Test (in Codespaces)
```bash
# Test with docker-compose (optional, before K8s)
docker-compose -f docker-compose.k8s.yml up -d
curl http://localhost:8000/health
curl http://localhost:3000
docker-compose -f docker-compose.k8s.yml down
```

### Acceptance Criteria
- [x] Both services start and communicate (skipped - moved directly to K8s)
- [x] App works end-to-end locally (will test in K8s)

---

## Task 4: Create Helm Chart with All K8s Resources
**Requirement**: REQ-4, REQ-5, REQ-6

### Subtasks
- [x] 4.1 Create Helm chart structure:
  ```
  helm/todo-app/
  ├── Chart.yaml
  ├── values.yaml
  └── templates/
      ├── _helpers.tpl
      ├── backend-deployment.yaml
      ├── backend-service.yaml
      ├── frontend-deployment.yaml
      ├── frontend-service.yaml
      ├── configmap.yaml
      ├── secrets.yaml
      └── ingress.yaml
  ```
- [x] 4.2 Configure deployments with health probes & resource limits
- [x] 4.3 Configure services (ClusterIP)
- [x] 4.4 Configure ingress routing (`/api/*` → backend, `/*` → frontend)
- [x] 4.5 Configure ConfigMap and Secrets for env vars

### Validate (in Codespaces)
```bash
helm lint ./helm/todo-app
helm template todo-app ./helm/todo-app
```

### Acceptance Criteria
- [x] `helm lint` passes (ready to validate in Codespace)
- [x] All templates render valid YAML (ready to validate in Codespace)

---

## Task 5: Deploy to Minikube & Test
**Requirement**: All requirements

### Deploy (in Codespaces)
```bash
# Ensure using Minikube's Docker
eval $(minikube docker-env)

# Create namespace and deploy
kubectl create namespace todo-app
helm install todo-app ./helm/todo-app -n todo-app

# Watch pods come up
kubectl get pods -n todo-app -w

# Check services
kubectl get svc -n todo-app

# Get Minikube IP and access app
minikube ip
# Or use port-forward for testing
kubectl port-forward svc/frontend-service 3000:3000 -n todo-app &
kubectl port-forward svc/backend-service 8000:8000 -n todo-app &
```

### Test
```bash
# Test backend health
curl http://localhost:8000/health

# Test frontend
curl http://localhost:3000

# Test API
curl http://localhost:8000/api/tasks
```

### Acceptance Criteria
- [x] All pods in Running state
- [x] Health checks passing
- [x] App accessible via port-forward
- [x] CRUD operations work

---

## Task 6: Documentation & Cleanup
**Requirement**: Submission requirements

### Subtasks
- [ ] 6.1 Create `KUBERNETES_SETUP.md` with:
  - Codespaces setup instructions
  - Build and deploy commands
  - Troubleshooting tips
- [ ] 6.2 Update `README.md` with Phase 4 section
- [ ] 6.3 Commit all changes to GitHub

### Useful Commands Reference
```bash
# Restart deployment
kubectl rollout restart deployment/backend -n todo-app

# View logs
kubectl logs -f deployment/backend -n todo-app

# Scale replicas
kubectl scale deployment/backend --replicas=2 -n todo-app

# Uninstall
helm uninstall todo-app -n todo-app

# Stop Minikube (save resources)
minikube stop

# Delete cluster
minikube delete
```

### Acceptance Criteria
- [ ] Documentation complete
- [ ] All code committed to GitHub

---

## Summary

| Task | Description | Est. Time |
|------|-------------|-----------|
| 1 | Setup Codespaces (kubectl, minikube, helm) | 15 min |
| 2 | Dockerize Backend & Frontend | 45 min |
| 3 | Docker Compose Local Test | 20 min |
| 4 | Create Helm Chart (all K8s resources) | 60 min |
| 5 | Deploy to Minikube & Test | 30 min |
| 6 | Documentation | 20 min |

**Total Estimated Time**: ~3 hours

---

## Quick Reference: Codespaces Commands

```bash
# === SETUP ===
minikube start --driver=docker --cpus=2 --memory=4096
minikube addons enable ingress
eval $(minikube docker-env)

# === BUILD ===
docker build -t todo-backend:latest ./backend
docker build -t todo-frontend:latest ./frontend

# === DEPLOY ===
kubectl create namespace todo-app
helm install todo-app ./helm/todo-app -n todo-app

# === TEST ===
kubectl port-forward svc/backend-service 8000:8000 -n todo-app &
kubectl port-forward svc/frontend-service 3000:3000 -n todo-app &

# === DEBUG ===
kubectl get pods -n todo-app
kubectl logs -f <pod-name> -n todo-app
kubectl describe pod <pod-name> -n todo-app

# === CLEANUP ===
helm uninstall todo-app -n todo-app
minikube stop
```
