#!/bin/bash
set -e

echo "=========================================="
echo "Phase 4: Setting up Kubernetes in Codespace"
echo "=========================================="

# Install kubectl
echo "📦 Installing kubectl..."
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
echo "✅ kubectl installed: $(kubectl version --client --short)"

# Install Minikube
echo "📦 Installing Minikube..."
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
chmod +x minikube-linux-amd64
sudo mv minikube-linux-amd64 /usr/local/bin/minikube
echo "✅ Minikube installed: $(minikube version --short)"

# Install Helm
echo "📦 Installing Helm..."
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
echo "✅ Helm installed: $(helm version --short)"

# Start Minikube
echo "🚀 Starting Minikube cluster..."
minikube start --driver=docker --cpus=2 --memory=4096

# Enable Ingress
echo "🔌 Enabling Ingress addon..."
minikube addons enable ingress

# Verify setup
echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
kubectl get nodes
echo ""
echo "Next steps:"
echo "1. Run: eval \$(minikube docker-env)"
echo "2. Continue with Task 2 (Dockerize apps)"
