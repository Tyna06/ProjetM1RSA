import requests
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Une "base de données" simulée
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
    nouvelle_note = {
        "id": len(notes) + 1,
        "etudiant_id": data.get("etudiant_id"),
        "valeur": data.get("valeur")
    }
    notes.append(nouvelle_note)
    return jsonify({"message": "Note ajoutée", "note": nouvelle_note}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
