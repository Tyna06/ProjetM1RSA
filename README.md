
#  Projet M1 RSA – Gestion Étudiants & Notes 

Microservices Flask | PostgreSQL | Kubernetes | Istio | Minikube

---

##  Description

Ce projet implémente une application de gestion d’étudiants et de leurs notes sous forme de microservices (Flask), déployés avec Kubernetes sur Minikube et connectés via Istio (service mesh).  
Le projet contient :
- Un front-end Flask
- Deux microservices : `etudiants-service`, `notes-service`
- Une base de données PostgreSQL
- Une architecture distribuée gérée avec Kubernetes + Istio

---

##  Prérequis

Avant de démarrer, assurez-vous d’avoir les outils suivants installés :

```bash
- Python 3.9+
- pip
- Docker Desktop
- Minikube
- kubectl
- Istio (installé sur le cluster Minikube)
- Git
```

---

##  Arborescence du projet

```
ProjetM1RSA/
│
├── backend/
│   ├── etudiants-service/
│   ├── notes-service/
│
├── frontend/ (Flask)
│
├── kubernetes/
│   ├── postgresql.yml
│   ├── init-db-job-etudiants.yml
│   ├── init-db-job-notes.yml
│   ├── peer-auth.yml
│   ├── frontend.yml
│   ├── etudiants-deployment.yml
│   ├── notes-deployment.yml
│   ├── gateway.yml 
│
├── README.md
├── requirements.txt
└── .env
```

---

##  Lancement de l’application (Étapes)

### 1. Cloner le dépôt

```bash
git clone https://github.com/Tyna06/ProjetM1RSA.git
cd ProjetM1RSA
```

### 2. Lancer Minikube et activer Istio

```bash
minikube start --driver=docker

istioctl install --set profile=demo -y
kubectl label namespace default istio-injection=enabled
```

### 3. Déployer la base de données PostgreSQL

```bash
kubectl apply -f kubernetes/postgres.yaml
```

### 4. Déployer les microservices

```bash
kubectl apply -f kubernetes/etudiants-deployment.yaml
kubectl apply -f kubernetes/notes-deployment.yaml
```

### 5. Initialiser la base de données (si nécessaire)

Appeler manuellement `/init-db` si les tables ne sont pas automatiquement créées.

### 6. Déployer la Gateway et les VirtualServices (Istio)

```bash
kubectl apply -f kubernetes/gateway.yaml
```

### 7. Accéder à l’application

```bash
minikube tunnel
# puis accéder via : http://<@-ip>/
```

---

##  Utilisation locale (optionnel)

```bash
cd backend/etudiants-service
pip install -r requirements.txt
python etudiant.py
```

---

##  Fonctionnalités

- Ajout / Suppression / Modification d’étudiants
- Ajout / Modification / Suppression de notes
- Dashboard pour Admin et Étudiant
- Séparation des microservices
- Connexion sécurisée avec Istio Gateway

---

##  Auteurs

- Tyna Ziane ([@Tyna06](https://github.com/Tyna06))
- Gaye Ndeye Cissé

---

##  Tests & Validation

- `kubectl get pods`
- `kubectl logs`
- Tests Postman
- Vérification du front-end connecté

---

##  Conseils & Remarques

- `psql` peut ne pas être disponible dans les containers Flask, utiliser un pod postgres temporaire.
- Ne pas oublier `minikube tunnel` pour exposer la Gateway.
