from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Liste simulée d'étudiants
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
    etudiant_id = data.get("etudiant_id")
    valeur = data.get("valeur")

    # Vérifie que les champs sont là
    if not etudiant_id or valeur is None:
        return jsonify({"error": "Champs manquants"}), 400

    # Print pour vérifier l'URL de la requête
    print(f"Tentative de connexion à l'URL : http://localhost:5001/etudiants/{etudiant_id}")

    # Appelle le service étudiant pour vérifier si l'étudiant existe
    try:
        resp = requests.get(f"http://localhost:5001/etudiants/{etudiant_id}")
        print(f"Réponse du service étudiant : {resp.status_code}")  # Print pour le statut de la réponse
        if resp.status_code == 200:
            etudiant = resp.json()  # Récupère les données de l'étudiant
            print(f"Étudiant trouvé : {etudiant}")
        else:
            return jsonify({"error": "Étudiant non trouvé"}), 404
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel HTTP : {e}")
        return jsonify({"error": "Erreur de communication avec le service étudiant"}), 503

    # Si tout est bon, ajoute la note
    nouvelle_note = {
        "id": len(notes) + 1,
        "etudiant_id": etudiant_id,
        "valeur": valeur
    }
    notes.append(nouvelle_note)
    return jsonify({"message": "Note ajoutée", "note": nouvelle_note}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
