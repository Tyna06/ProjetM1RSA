# ProjetM1RSA
# Plan de Tâches Projet M1RSA

## 🔓 Authentification et Sécurité (Binôme A)
| Tâche | Description | Assigné à |
|--------|-------------|-----------|
| [ ] Gérer POST login | `login.html` → Flask vérifie email + mot de passe | Binôme A |
| [ ] Créer table `users` dans la base de données | Champs : id, nom, email, mdp hashé, rôle | Binôme A |
| [ ] Stocker les sessions utilisateurs | `session['user_id']`, `session['role']` | Binôme A |
| [ ] Protéger les pages admin et étudiant selon rôle | Si pas connecté ou mauvais rôle → redirect | Binôme A |

## 🧑‍🏫 Front étudiant + admin (Toi)
| Tâche | Description | Assigné à |
|--------|-------------|-----------|
| [ ] Compléter le dashboard étudiant | Voir ses infos et ses notes via API | Toi |
| [ ] Compléter dashboard admin | Voir tous les étudiants + ajouter | Toi |
| [ ] Connecter le front aux microservices avec `requests.get/post` | Depuis `app.py` du front | Toi |
| [ ] Ajouter feedback visuel sur succès/erreur | Message de confirmation, redirection | Toi |

## 📃 Back-end + Base de Données (Binôme A ou B)
| Tâche | Description | Assigné à |
|--------|-------------|-----------|
| [ ] Ajouter une vraie BDD (PostgreSQL ou SQLite) | Une pour chaque microservice, ou centralisée | Binôme A |
| [ ] Connecter `etudiants.py` à la BDD | Ajout, lecture, suppression... avec SQLAlchemy | Binôme B |
| [ ] Connecter `notes.py` à la BDD | Idem pour les notes | Binôme B |
| [ ] Ajouter gestion des erreurs API (404, 500, etc.) | API Flask propre | Binôme B |

## 🐳 Docker / Kubernetes
| Tâche | Description | Assigné à |
|--------|-------------|-----------|
| [x] Dockerfile pour chaque service | Déjà fait ✔️ | Fait |
| [x] Kubernetes YAML | Déjà fait ✔️ | Fait |
| [ ] Ajouter volume pour PostgreSQL | Pour persister les données | Binôme A ou B |
| [ ] `docker-compose.yml` (optionnel pour local) | Regrouper services + BDD | Fac. |

## 🔢 Test de bout en bout
| Tâche | Description |
|--------|-------------|
| [ ] Test : inscription → enregistrement → login → redirection |
| [ ] Test : ajouter étudiant → vérifier dans la base |
| [ ] Test : affichage des notes côté étudiant/admin |

