# Phase 4: Local Kubernetes Deployment - Design

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                    GITHUB CODESPACES                                │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │                    MINIKUBE CLUSTER                           │  │
│  │                                                               │  │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │  │
│  │  │   Ingress   │    │   Ingress   │    │   Ingress   │       │  │
│  │  │  Controller │    │  /api/*     │    │  /*         │       │  │
│  │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘       │  │
│  │         │                  │                  │               │  │
│  │         ▼                  ▼                  ▼               │  │
│  │  ┌─────────────────────────────────────────────────────┐     │  │
│  │  │              Kubernetes Services                     │     │  │
│  │  │  ┌──────────────────┐  ┌──────────────────┐         │     │  │
│  │  │  │ backend-service  │  │ frontend-service │         │     │  │
│  │  │  │   (ClusterIP)    │  │   (ClusterIP)    │         │     │  │
│  │  │  └────────┬─────────┘  └────────┬─────────┘         │     │  │
│  │  └───────────┼─────────────────────┼───────────────────┘     │  │
│  │              │                     │                         │  │
│  │              ▼                     ▼                         │  │
│  │  ┌──────────────────┐  ┌──────────────────┐                 │  │
│  │  │ Backend Pods     │  │ Frontend Pods    │                 │  │
│  │  │ ┌──────────────┐ │  │ ┌──────────────┐ │                 │  │
│  │  │ │   FastAPI    │ │  │ │   Next.js    │ │                 │  │
│  │  │ │   + MCP      │ │  │ │   + React    │ │                 │  │
│  │  │ └──────────────┘ │  │ └──────────────┘ │                 │  │
│  │  │ Replicas: 1-3    │  │ Replicas: 1-2    │                 │  │
│  │  └──────────────────┘  └──────────────────┘                 │  │
│  │              │                                               │  │
│  │              ▼                                               │  │
│  │  ┌──────────────────┐                                       │  │
│  │  │  ConfigMaps &    │                                       │  │
│  │  │  Secrets         │                                       │  │
│  │  └──────────────────┘                                       │  │
│  └───────────────────────────────────────────────────────────────┘  │
│                              │                                      │
│                              ▼                                      │
│                    ┌──────────────────┐                            │
│                    │   External DB    │                            │
│                    │   (Neon.tech)    │                            │
│                    └──────────────────┘                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Design

### 1. Docker Images

#### Backend Dockerfile (`backend/Dockerfile`)
```dockerfile
# Multi-stage build for smaller image
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Non-root user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Frontend Dockerfile (`frontend/Dockerfile`)
```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

---

### 2. Helm Chart Structure

```
helm/
├── todo-app/
│   ├── Chart.yaml
│   ├── values.yaml
│   ├── values-dev.yaml
│   ├── templates/
│   │   ├── _helpers.tpl
│   │   ├── backend-deployment.yaml
│   │   ├── backend-service.yaml
│   │   ├── frontend-deployment.yaml
│   │   ├── frontend-service.yaml
│   │   ├── ingress.yaml
│   │   ├── configmap.yaml
│   │   └── secrets.yaml
│   └── .helmignore
```

#### Chart.yaml
```yaml
apiVersion: v2
name: todo-app
description: Todo Chatbot Application Helm Chart
type: application
version: 1.0.0
appVersion: "3.0.0"
```

#### values.yaml (Default Configuration)
```yaml
# Backend Configuration
backend:
  replicaCount: 1
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi
  env:
    DATABASE_URL: ""
    LLM_API_KEY: ""

# Frontend Configuration
frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 3000
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
  env:
    NEXT_PUBLIC_API_URL: "http://backend-service:8000"

# Ingress Configuration
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: todo.local
      paths:
        - path: /api
          pathType: Prefix
          service: backend
        - path: /
          pathType: Prefix
          service: frontend
```

---

### 3. Kubernetes Resources

#### Backend Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-backend
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: {{ include "todo-app.fullname" . }}-config
            - secretRef:
                name: {{ include "todo-app.fullname" . }}-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            {{- toYaml .Values.backend.resources | nindent 12 }}
```

---

### 4. Directory Structure (Final)

```
project-root/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── ... (existing code)
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   └── ... (existing code)
├── helm/
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       ├── values-dev.yaml
│       └── templates/
│           └── ... (K8s manifests)
├── docker-compose.yml
├── k8s/
│   └── minikube-setup.sh
└── docs/
    └── KUBERNETES_SETUP.md
```

---

## Data Flow

1. **User Request** → Ingress Controller
2. **Ingress** routes `/api/*` → Backend Service → Backend Pod
3. **Ingress** routes `/*` → Frontend Service → Frontend Pod
4. **Backend Pod** → External Neon DB (via DATABASE_URL secret)
5. **Backend Pod** → External LLM API (via LLM_API_KEY secret)

---

## Security Considerations

1. **Secrets Management**: All sensitive data (DB URL, API keys) stored in K8s Secrets
2. **Non-root Containers**: Both images run as non-root users
3. **Resource Limits**: Prevent resource exhaustion attacks
4. **Network Policies**: (Optional) Restrict pod-to-pod communication

---

## Scaling Strategy

| Service  | Min Replicas | Max Replicas | Scaling Trigger |
|----------|--------------|--------------|-----------------|
| Backend  | 1            | 3            | CPU > 70%       |
| Frontend | 1            | 2            | CPU > 80%       |

---

## Health Checks

| Service  | Liveness Path | Readiness Path | Interval |
|----------|---------------|----------------|----------|
| Backend  | /health       | /health        | 30s      |
| Frontend | /api/health   | /api/health    | 30s      |
