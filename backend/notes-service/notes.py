import requests
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)


# Données simulées en mémoire


notes = [
    {"id": 1, "etudiant_id": 101, "valeur": 15.5},
    {"id": 2, "etudiant_id": 102, "valeur": 12.0}
]

# GET : récupérer toutes les notes
@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify(notes)

# POST : ajouter une note
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()

    id_etudiant = data.get("etudiant_id")
    valeur = data.get("valeur")

    # Vérification que les données sont présentes
    if id_etudiant is None or valeur is None:
        return jsonify({"error": "Champs manquants"}), 400

    # Vérifier si l'étudiant existe dans le microservice etudiants
    try:
        # Utilise localhost:5001 uniquement pour les tests en local
        resp = requests.get(f"http://localhost:5001/etudiants/{id_etudiant}")
        if resp.status_code != 200:
            return jsonify({"error": "Étudiant non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": "Erreur lors de la communication avec etudiant-service"}), 500

    # Ajouter la note si l'étudiant existe
    nouvelle_note = {
        "id": len(notes) + 1,
        "etudiant_id": id_etudiant,

        "valeur": valeur
    }
    notes.append(nouvelle_note)
    return jsonify({"message": "Note ajoutée", "note": nouvelle_note}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
