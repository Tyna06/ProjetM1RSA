# 🧑‍🎓 Projet M1 RSA - Application de Gestion Scolaire (Cloud Native)

Projet réalisé par Ziane Thinhinane et Gaye Ndeye Cissé dans le cadre du Master 1 Informatique (Réseaux et Systèmes autonome) à l'UFR de Mathématiques et Informatique de l'Université Paris Cité.

## 🌟 Objectif du projet

Concevoir, développer et déployer une application web cloud-native de gestion d'étudiants et de notes à l'aide de microservices conteneurisés, orchestrés par Kubernetes, sécurisés via Istio et exposés via une Gateway.

## 🧱 Technologies utilisées

* Python / Flask (API REST)
* PostgreSQL (base de données relationnelle)
* Docker (conteneurs)
* Kubernetes (orchestration)
* Istio (service mesh, sécurité mTLS)
* HTML/CSS (templates Flask front-end)

## 🚪 Fonctionnalités principales

* Authentification admin / étudiant
* Ajout, modification, suppression d'étudiants
* Ajout, modification, suppression de notes
* Calcul automatique des moyennes
* Dashboard étudiant personnalisé
* Interface admin avec statistiques globales
* Filtrage des notes par matière et niveau

  ## 🧪 Utilisation et authentification

### 🎓 Accès étudiant
- Chaque étudiant peut s'inscrire via le formulaire prévu.
- Une fois connecté, il accède à son dashboard personnel avec ses informations et ses notes.

### 👨‍💼 Accès admin
- Identifiant : `admin@demo`
- Mot de passe : `admin`

> ⚠️ Ces identifiants sont **simulés dans le front Flask** et peuvent être modifiés dans le code si nécessaire.

### 🔄 Possibilités de test :
- Ajouter des étudiants
- Ajouter des notes
- Filtrer les notes par matière ou niveau
- Modifier / supprimer les données
- Vérifier les dashboards dynamiques


## 📊 Architecture globale

* 2 microservices backend :

  * `etudiants-service` (Flask + PostgreSQL)
  * `notes-service` (Flask + PostgreSQL)
* 1 front-end Flask (dashboards)
* Gateway Istio + VirtualServices
* Base de données PostgreSQL

Chaque service est conteneurisé avec Docker et déployé avec Kubernetes dans Minikube. Les communications passent par la Gateway Istio.

## 🚧 Sécurité : mTLS avec Istio

Une politique de `PeerAuthentication` est appliquée avec Istio pour activer le **mutual TLS (mTLS)** sur tout le namespace `default`.

```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
```

Cela garantit que toutes les communications entre services sont **chiffrées** et passent via les sidecars `istio-proxy`.

## 🚀 Déploiement local (Minikube)

1. Builder les images :

```bash
docker build -t etudiants-service ./backend/etudiants-service
docker build -t notes-service ./backend/notes-service
docker build -t frontend ./frontend
```

2. Lancer Minikube avec le profil Istio :

```bash
minikube start --driver=docker
```

3. Appliquer les déploiements et services Kubernetes :

```bash
kubectl apply -f kubernetes/
```

4. Récupérer l'URL Istio Gateway :

```bash
minikube service istio-ingressgateway -n istio-system --url
```

## 📚 Structure du projet

```
ProjetM1RSA/
├── backend/
│   ├── etudiants-service/
│   └── notes-service/
├── frontend/
├── kubernetes/
│   ├── deployments + services
│   └── peer-auth.yaml
├── README.md
```

## 🤝 Travail réalisé par

* Ziane Thinhinane (Tyna)
* Gaye Ndeye Cissé

## 🔗 Lien du dépôt

[https://github.com/Tyna06/ProjetM1RSA](https://github.com/Tyna06/ProjetM1RSA)

---

> Ce projet a été réalisé dans le cadre du cours "Cloud Native & Microservices" encadré par M. Charroux
