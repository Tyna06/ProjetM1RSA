# Étape 1 : Choisir une image Python légère
FROM python:3.9-slim
# Étape 2 : Définir le répertoire de travail
WORKDIR /app
# Étape 3 : Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Étape 4 : Copier le reste du code
COPY . .
# Étape 5 : Lancer l’application
CMD ["sh", "-c", "python notes.py & sleep 5 && python add_matiere.py && wait"]