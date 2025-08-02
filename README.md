
# Flask App CI/CD with GitHub Actions, SonarQube, Docker, Kubernetes & ArgoCD

![Image](https://github.com/user-attachments/assets/a3b2585a-86bb-4999-a92d-bd530f2b0c85)

This project demonstrates a complete DevOps workflow using a **Python Flask web application** with a CI/CD pipeline powered by GitHub Actions, SonarQube, Docker, Kubernetes, and ArgoCD.

---

## Tools Used

| Tool | Purpose |
| --- | --- |
| Flask | Python web application framework |
| GitHub Actions | CI/CD automation |
| SonarQube | Code quality and static analysis |
| Docker | Containerization |
| Kubernetes | Application deployment/scaling |
| ArgoCD | GitOps continuous delivery |
| GitHub | Code and manifests hosting |
| Docker Hub | Container image registry |

---

## CI/CD Workflow with GitHub Actions

### ✅ Steps

1. Checkout code from GitHub
2. Set up Python 3.11
3. Install dependencies and run unit tests with `pytest`
4. Perform static code analysis with SonarQube
5. Build Docker image and push to DockerHub
6. Update Kubernetes manifest file (`deployment.yml`) with new image tag
7. Push updated YAMLs to GitHub
8. ArgoCD detects the change and deploys the new version automatically

---

## Secrets Configuration (GitHub Settings > Secrets)

| Secret Name           | Description |
|-----------------------|-------------|
| `SONARQUBE`           | SonarQube token |
| `DOCKERHUB_USERNAME`  | DockerHub username |
| `DOCKERHUB_PASSWORD`  | DockerHub password |
| `GIT_PAT`             | GitHub Personal Access Token with repo push permissions |

---

### Install SonarQube

```bash
sudo apt update
sudo apt install openjdk-17-jdk unzip wget -y
sudo adduser sonarqube
cd /opt
sudo wget https://binaries.sonarsource.com/Distribution/sonarqube/sonarqube-9.9.4.87374.zip
sudo unzip sonarqube-9.9.4.87374.zip
sudo mv sonarqube-9.9.4.87374 sonarqube
sudo chown -R sonarqube:sonarqube /opt/sonarqube
sudo chmod -R 775 /opt/sonarqube
sudo su -s /bin/bash sonarqube
cd /opt/sonarqube/bin/linux-x86-64/
./sonar.sh start
./sonar.sh status
```

Access SonarQube at `http://<ip>:9000` and log in using `admin/admin`. Create a project and generate a token.

---
## Kubernetes & ArgoCD Setup

### 1. Install Kubernetes CLI and Minikube

```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube start
```

### 2. Install and Configure ArgoCD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "NodePort"}}'
kubectl get svc argocd-server -n argocd
```

Get ArgoCD password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode
```

Access ArgoCD UI using NodePort IP. Login: `admin` / `<decoded password>`

---

## Configure ArgoCD Application

- **Git Repo**: Your GitHub repo URL
- **Path**: Folder with Kubernetes manifests (`flask-app-manifests`)
- **Namespace**: `default`
- **Sync Policy**: Manual or Auto

Ensure your `service.yaml` contains:

```yaml
spec:
  type: NodePort
```

---

## Sample Flask `service.yaml`

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-app
  namespace: default
spec:
  selector:
    app: flask-app
  type: NodePort
  ports:
    - protocol: TCP
      port: 5000
      targetPort: 5000
```

Apply the service:

```bash
kubectl apply -f service.yaml
```

Get the app URL:

```bash
minikube service flask-app -n default
```

---

## GitHub Actions Workflow Overview

This project uses GitHub Actions as the CI/CD engine. Here's a summary of the `.github/workflows/ci-cd.yml`:

- Code checkout
- Python test with `pytest`
- Static analysis using SonarQube
- Docker image build and push
- Deployment file update with latest image tag
- Git push for GitOps (ArgoCD)

---

