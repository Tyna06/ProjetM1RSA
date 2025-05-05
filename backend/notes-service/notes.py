import requests
from flask import Flask, jsonify, request
import requests
from models import db
from models.models import Note, Matiere


app = Flask(__name__)


# Connexion à la même base PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@localhost:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/init-db")
def create_tables():
    with app.app_context():
        db.create_all()
    return "✅ Base de données (notes) initialisée !"


# POST : ajouter une matière
@app.route("/ajouter-matiere", methods=["POST"])
def ajouter_matiere():
    data = request.get_json()
    try:
        matiere = Matiere(nom=data["nom"])
        db.session.add(matiere)
        db.session.commit()
        return jsonify({"message": "Matière ajoutée", "id": matiere.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": str(e)}), 400


# GET : récupérer toutes les notes
@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    return jsonify([
        {
            "id": n.id,
            "etudiant_id": n.etudiant_id,
            "valeur": n.valeur,
            "date": n.date_evaluation.isoformat()
        } for n in notes
    ])

# POST : ajouter une note
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    etudiant_id = data.get("etudiant_id")

    # Vérifier si l'étudiant existe via le service étudiant
    try:
        r = requests.get(f"http://localhost:5001/etudiants/{etudiant_id}")
        if r.status_code != 200:
            return jsonify({"error": "Étudiant non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur connexion service étudiant: {e}"}), 500

    note = Note(
        etudiant_id=etudiant_id,
        matiere_id=data.get("matiere_id"),
        valeur=data.get("valeur"),
        coefficient=data.get("coefficient", 1),
        commentaire=data.get("commentaire", "")
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note ajoutée", "id": note.id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)