
# Flask App CI/CD with GitHub Actions, SonarQube, Docker, Kubernetes & ArgoCD

![Image](https://github.com/user-attachments/assets/a0710c79-d6b9-4336-98d8-09396fcbb163)

This repository outlines a robust, production-grade CI/CD pipeline for a **Python Flask web application**. It leverages GitHub Actions for automation, SonarQube for continuous code quality, and a GitOps deployment model using Docker, Helm, and ArgoCD on a Kubernetes cluster.

## Technology Stack

| Component | Role |
| --- | --- |
| Flask | Web Application Framework |
| GitHub Actions | CI/CD and Workflow Automation |
| SonarQube | Static Code Analysis & Quality Gate |
| Docker | Application Containerization |
| Helm | Kubernetes Package Management |
| Kubernetes | Container Orchestration |
| ArgoCD | GitOps Continuous Delivery Engine |
| GitHub | Source Code & Helm Chart Repository |
| Docker Hub | Container Image Registry |

## Automated CI/CD Workflow

The entire pipeline is automated via GitHub Actions (`.github/workflows/ci-cd.yml`) and operates on a GitOps principle.

### Pipeline Stages

1. **Build & Test**: On a push to the `master` branch, the workflow initiates, sets up the Python environment, installs dependencies, and executes unit tests via `pytest`.
    
2. **Code Analysis**: The codebase is scanned by SonarQube to detect vulnerabilities, bugs, and code smells, ensuring code quality standards are met.
    
3. **Containerization**: A Docker image is built and pushed to Docker Hub, tagged with a unique identifier from the GitHub workflow run.
    
4. **Helm Chart Update**: The pipeline programmatically updates the `image.tag` in the application's Helm chart (`values.yaml`) to reference the newly published Docker image.
    
5. **GitOps Trigger**: The updated Helm chart is committed and pushed back to the Git repository.
    
6. **Automated Deployment**: ArgoCD, which continuously monitors the Git repository, detects the change in the Helm chart and automatically deploys the new application version to the Kubernetes cluster, ensuring the cluster state matches the configuration in Git.
    

## Configuration

### Repository Secrets & Variables

Configure the following in your GitHub repository under `Settings > Secrets and variables > Actions`:

| Type | Name | Description |
| --- | --- | --- |
| **Secret** | `SONAR_TOKEN` | SonarQube project analysis token. |
| **Secret** | `DOCKERHUB_USERNAME` | DockerHub username. |
| **Secret** | `DOCKERHUB_PASSWORD` | DockerHub password or access token. |
| **Secret** | `GIT_PAT` | GitHub Personal Access Token with `repo` scope to enable pushing Helm chart updates. |
| **Variable** | `SONAR_HOST_URL` | Public URL of your SonarQube instance (e.g., [`http://your-sonar-ip:9000`](http://your-sonar-ip:9000)). |

## System Implementation

### SonarQube Installation

```bash
# Update package list and install dependencies
sudo apt update
sudo apt install openjdk-17-jdk unzip wget -y
# ... (rest of SonarQube installation script)

```

Access the SonarQube UI at `http://<your_server_ip>:9000` (`admin`/`admin`). Create a project and generate a token for the `SONAR_TOKEN` secret.

### Kubernetes & ArgoCD Deployment

#### 1\. Prerequisite: Cluster Access

Ensure `kubectl` is installed and configured to communicate with your target Kubernetes cluster.

```bash
kubectl cluster-info

```

#### 2\. ArgoCD Installation

```bash
# Create a dedicated namespace for ArgoCD
kubectl create namespace argocd

# Apply the official ArgoCD installation manifests
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

```

To access the ArgoCD dashboard, expose the `argocd-server` service, typically via an **Ingress controller** (recommended for production) or a LoadBalancer.

Retrieve the initial admin password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 --decode

```

Access the UI via your configured Ingress host or LoadBalancer IP. The username is `admin`.

#### 3\. ArgoCD Application Configuration

In the ArgoCD UI, create a new application to monitor the Helm chart in your repository.

* **Application Name**: A unique name (e.g., `flask-production`).
    
* **Project**: `default`
    
* **Sync Policy**: `Automatic` (enable `Prune Resources` and `Self Heal` for a pure GitOps model).
    
* **Repository URL**: The URL of your GitHub repository.
    
* **Revision**: `HEAD`
    
* **Path**: `helm/flask-app-chart` (Path to the Helm chart within the repository).
    
* **Cluster URL**: [`https://kubernetes.default.svc`](https://kubernetes.default.svc)
    
* **Namespace**: The target namespace for deployment (e.g., `production`).
    

## Accessing the Deployed Application

When using an Ingress controller (e.g., NGINX), the application is accessed through the host defined in your Ingress resource. Based on your configuration, the application will be available at:

**URL:** [`http://flask-app.local`](http://flask-app.local)

To access this locally, you may need to map the hostname to your Ingress controller's external IP address in your `/etc/hosts` file:

```bash
<ingress-controller-ip>   flask-app.local
```

You can find the Ingress controller's IP with:

```bash
kubectl get svc -n <ingress-namespace>
```