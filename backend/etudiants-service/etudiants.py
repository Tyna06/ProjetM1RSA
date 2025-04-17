from flask import Flask, request, jsonify

app = Flask(__name__)

# Liste simulée d'étudiants (base de données temporaire)
etudiants = [
    {"id": 1, "nom": "Alice", "email": "alice@example.com"},
    {"id": 2, "nom": "Bob", "email": "bob@example.com"}
]

# GET : récupérer tous les étudiants
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    return jsonify(etudiants)

# POST : ajouter un nouvel étudiant
@app.route("/etudiants", methods=["POST"])
def add_etudiant():
    data = request.get_json()
    new_etudiant = {
        "id": len(etudiants) + 1,
        "nom": data.get("nom"),
        "email": data.get("email")
    }
    etudiants.append(new_etudiant)
    return jsonify({"message": "Étudiant ajouté", "etudiant": new_etudiant}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
