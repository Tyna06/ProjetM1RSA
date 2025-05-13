# Étape 1 : Image de base
FROM python:3.9-slim

# Étape 2 : Définir le dossier de travail
WORKDIR /app

# Étape 3 : Copier les dépendances et installer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape 4 : Copier le reste du code
COPY . .

# Étape 5 : Exposer le port utilisé par Flask
EXPOSE 5002

# Étape 6 : Lancer l’application
CMD ["python", "app.py"]
