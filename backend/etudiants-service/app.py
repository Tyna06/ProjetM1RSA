from flask import Flask, request, jsonify
from models import db, Etudiant, Note, Matiere
import os

app = Flask(__name__)

# Configuration PostgreSQL (adapter selon tes variables Docker)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@localhost:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base
db.init_app(app)

# 🚀 Route pour ajouter un étudiant
@app.route("/ajouter-etudiant", methods=["POST"])
def ajouter_etudiant():
    data = request.get_json()
    try:
        nouvel_etudiant = Etudiant(
            nom=data["nom"],
            prenom=data["prenom"],
            mot_de_passe=data["mot_de_passe"],  # à sécuriser plus tard
            age=data["age"],
            niveau=data["niveau"]
        )
        db.session.add(nouvel_etudiant)
        db.session.commit()
        return jsonify({"message": "Étudiant ajouté avec succès"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": str(e)}), 400
from models import Note  # déjà fait pour Etudiant, ajoute Note aussi

@app.route("/ajouter-note", methods=["POST"])
def ajouter_note():
    data = request.get_json()
    try:
        nouvelle_note = Note(
            etudiant_id=data["etudiant_id"],
            matiere_id=data["matiere_id"],
            valeur=data["valeur"],
            coefficient=data.get("coefficient", 1),
            commentaire=data.get("commentaire", None)
        )
        db.session.add(nouvelle_note)
        db.session.commit()
        return jsonify({"message": "Note ajoutée avec succès"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": str(e)}), 400
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
    

# Créer les tables à la première exécution
def create_database():
    with app.app_context():
        db.create_all()
        print("✅ Base de données initialisée avec les tables.")

if __name__ == "__main__":
    create_database()
    app.run(debug=True, port=5003)
