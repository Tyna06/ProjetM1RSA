# Étape 1 : Choisir une image Python
FROM python:3.9-slim

# Étape 2 : Définir le dossier de travail dans le conteneur
WORKDIR /app

# Étape 3 : Copier les fichiers nécessaires dans le conteneur
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Étape 4 : Démarrer l’application
CMD ["python", "notes.py"]
