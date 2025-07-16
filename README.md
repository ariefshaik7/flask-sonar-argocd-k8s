# Flask App CI/CD with Jenkins, SonarQube, Docker, Kubernetes & ArgoCD

![CI/CD Pipeline](https://github.com/user-attachments/assets/ad08378e-3702-43b3-9dad-691835d9bc35)


This project demonstrates a complete DevOps workflow using a **Python Flask web application** with a CI/CD pipeline powered by Jenkins, SonarQube, Docker, Kubernetes, and ArgoCD.

---

## Tools Used

| Tool | Purpose |
| --- | --- |
| Flask | Python web application framework |
| Jenkins | CI/CD automation |
| SonarQube | Code quality and static analysis |
| Docker | Containerization |
| Kubernetes | Application deployment/scaling |
| ArgoCD | GitOps continuous delivery |
| GitHub | Code and manifests hosting |
| Docker Hub | Container image registry |

---

## Step-by-Step Setup Instructions

### 1\. Install Jenkins

```bash
sudo apt update
sudo apt install openjdk-17-jdk -y
wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
sudo apt update
sudo apt install jenkins -y
sudo systemctl enable jenkins
sudo systemctl start jenkins
```

Access Jenkins at `http://<ip>:8080`. To get the password:

```bash
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

Install suggested plugins and also install:

* Docker Pipeline
    
* SonarQube Scanner
    
* GitHub Plugin
    

---

### 2\. Install Docker

```bash
sudo apt install docker.io -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

---

### 3\. Install SonarQube

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

### 4\. Add Credentials in Jenkins

Go to **Manage Jenkins &gt; Credentials &gt; Global &gt; Add Credentials**:

* **GitHub**: Username + Token (with repo access)
    
* **Docker Hub**: Username + Docker token
    
* **SonarQube**: Secret text (Sonar token)
    

---

### 5\. Install Kubernetes CLI and Start Minikube Cluster

```bash
curl -LO "https://dl.k8s.io/release/$(curl -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start Minikube
minikube start
```

---

### 6\. Install and Configure ArgoCD

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

Access ArgoCD UI using the NodePort IP and login with username `admin` and the decoded password.

---

### 7\. Configure ArgoCD Application

Use the ArgoCD UI to configure your application:

* **Git Repo**: Link to your GitHub repo
    
* **Path**: Folder containing Kubernetes manifests (e.g. `flask-app-manifests`)
    
* **Namespace**: `default`
    
* **Sync Policy**: Auto or Manual
    

Ensure the `service.yaml` contains:

```yaml
spec:
  type: NodePort
```

---

### 8\. Sample Flask `service.yaml`

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

Get the URL:

```bash
minikube service flask-app -n default
```

---

## Jenkins Pipeline Flow

1. Pull code from GitHub
    
2. Run SonarQube analysis (for Python)
    
3. Build and package Flask app
    
4. Build Docker image and push to Docker Hub
    
5. Update `deployment.yaml` with new image tag
    
6. Push updated YAMLs to GitHub
    
7. ArgoCD detects change and deploys automatically
    

---

This project demonstrates an end-to-end DevOps CI/CD pipeline for a Python Flask web application using Jenkins, SonarQube, Docker, Kubernetes, and ArgoCD.