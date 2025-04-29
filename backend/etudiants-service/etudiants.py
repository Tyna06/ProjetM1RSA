from flask import Flask, request, jsonify

app = Flask(__name__)

# Liste simulée d'étudiants (base de données temporaire)
etudiants = [
    {"id": 1, "nom": "Alice", "email": "alice@example.com"},
    {"id": 2, "nom": "Bob", "email": "bob@example.com"},
    {"id": 101, "nom": "Ndeye", "email": "ndeye@example.com"}
]

# GET : récupérer tous les étudiants
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    return jsonify(etudiants)

# GET : récupérer un étudiant par son ID
@app.route("/etudiants/<int:id>", methods=["GET"])
def get_etudiant(id):
    etudiant = next((e for e in etudiants if e["id"] == id), None)
    if etudiant:
        return jsonify(etudiant)
    else:
        return jsonify({"error": "Étudiant non trouvé"}), 404

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
# GET : récupérer un étudiant par ID
@app.route("/etudiants/<int:id_etudiant>", methods=["GET"])
def get_etudiant(id_etudiant):
    etudiant = next((e for e in etudiants if e["id"] == id_etudiant), None)
    if etudiant:
        return jsonify(etudiant)
    else:
        return jsonify({"error": "Étudiant non trouvé"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
