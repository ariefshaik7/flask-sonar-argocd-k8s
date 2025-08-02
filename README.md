
# Flask App CI/CD with GitHub Actions, SonarQube, Docker, Kubernetes & ArgoCD

![CI/CD Architecture](https://github.com/user-attachments/assets/a0710c79-d6b9-4336-98d8-09396fcbb163)

This repository outlines a robust, production-grade CI/CD pipeline for a **Python Flask web application**. It leverages GitHub Actions for automation, SonarQube for continuous code quality, and a GitOps deployment model using Docker, Helm, and ArgoCD on a Kubernetes cluster.

##  Technology Stack

| Component       | Role                                               |
|----------------|----------------------------------------------------|
| Flask          | Web Application Framework                          |
| GitHub Actions | CI/CD and Workflow Automation                      |
| SonarQube      | Static Code Analysis & Quality Gate                |
| Docker         | Application Containerization                       |
| Helm           | Kubernetes Package Management                      |
| Kubernetes     | Container Orchestration                            |
| ArgoCD         | GitOps Continuous Delivery Engine                  |
| GitHub         | Source Code & Helm Chart Repository                |
| Docker Hub     | Container Image Registry                           |

---

##  Automated CI/CD Workflow

The entire pipeline is automated via GitHub Actions (`.github/workflows/ci-cd.yml`) and operates on a GitOps principle.

### Pipeline Stages

1. **Build & Test**: On a push to the `master` branch, the workflow initiates, sets up the Python environment, installs dependencies, and executes unit tests via `pytest`.
2. **Code Analysis**: SonarQube scans the codebase to detect bugs, vulnerabilities, and code smells.
3. **Containerization**: A Docker image is built and pushed to Docker Hub using a unique GitHub Actions run ID as the image tag.
4. **Helm Chart Update**: The pipeline updates the `image.tag` in the Helm chart (`values.yaml`).
5. **GitOps Trigger**: The updated chart is committed back to the GitHub repo.
6. **Automated Deployment**: ArgoCD detects the chart update and syncs the deployment to the Kubernetes cluster.

---

##  GitHub Secrets & Variables

Configure these in **Settings > Secrets and variables > Actions**:

| Type       | Name                 | Description                                                |
|------------|----------------------|------------------------------------------------------------|
| Secret     | `SONAR_TOKEN`        | SonarQube analysis token                                   |
| Secret     | `DOCKERHUB_USERNAME` | DockerHub username                                         |
| Secret     | `DOCKERHUB_PASSWORD` | DockerHub password or token                                |
| Secret     | `GIT_PAT`            | GitHub token with `repo` scope to update Helm chart        |
| Variable   | `SONAR_HOST_URL`     | SonarQube server URL, e.g. `http://your-sonar-ip:9000`     |

---

##  SonarQube Installation

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

Access at: `http://<your_server_ip>:9000` (`admin` / `admin`).Create a project and generate a token.

---

##  Kubernetes & ArgoCD Setup

### 1. Cluster Access

Ensure `kubectl` is installed and configured:

```bash
kubectl cluster-info
```

### 2. ArgoCD Installation

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Expose ArgoCD via LoadBalancer (important for UI access)
kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
```

### 3. NGINX Ingress Controller

Based on your cloud provider, install ingress:

For AKS (Azure Kubernetes Service):

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.0/deploy/static/provider/cloud/deploy.yaml
```

** Refer to** [NGINX Ingress Installation Guide](https://kubernetes.github.io/ingress-nginx/deploy/) for other platforms (EKS, GKE, minikube, etc.).

---

##  ArgoCD App Configuration

In the ArgoCD UI:

| Field             | Value                              |
|------------------|------------------------------------|
| Name              | `flask-production`                |
| Project           | `default`                         |
| Sync Policy       | `Automatic` (Prune + Self-Heal)   |
| Repo URL          | `<Your GitHub Repo>`              |
| Revision          | `HEAD`                            |
| Path              | `helm/flask-app-chart`            |
| Cluster URL       | `https://kubernetes.default.svc`  |
| Namespace         | `production`                      |

---

##  Accessing the App via Ingress

**URL:** [`http://flask-app.local`](http://flask-app.local)

Update your `/etc/hosts` file:

```bash
<ingress-controller-ip>   flask-app.local
```

Find ingress IP:

```bash
kubectl get svc -n <ingress-namespace>
```

---
