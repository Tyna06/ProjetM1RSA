import requests
from flask import Flask, jsonify, request
import requests
from models import db
from models.models import Note, Matiere,Etudiant



app = Flask(__name__)

# Connexion à la même base PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@postgres-service:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    # insérer les matières automatiquement si base vide
    matieres = ["Mathématiques", "Physique", "Chimie", "Informatique"]
    for nom in matieres:
        if not Matiere.query.filter_by(nom=nom).first():
            db.session.add(Matiere(nom=nom))
    db.session.commit()

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

@app.route('/matieres', methods=['GET'])
def get_matieres():
    matieres = Matiere.query.all()
    return jsonify([{"id": m.id, "nom": m.nom} for m in matieres])


# GET : récupérer toutes les notes
@app.route("/notes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    result = []
    for note in notes:
        result.append({
            "id": note.id,
            "valeur": note.valeur,
            "coefficient": note.coefficient,
            "date_evaluation": note.date_evaluation.isoformat(),
            "commentaire": note.commentaire,
            "etudiant_id": note.etudiant_id,
            "matiere_id": note.matiere_id
        })
    return jsonify(result)

# GET : Filtrer 
@app.route("/notes/filter", methods=["GET"])
def filter_notes():
    matiere_id = request.args.get("matiere_id")
    niveau = request.args.get("niveau")

    query = Note.query.join(Etudiant)
    if matiere_id:
        query = query.filter(Note.matiere_id == matiere_id)
    if niveau:
        query = query.filter(Etudiant.niveau == niveau)

    notes = query.all()
    result = [
        {
            "id": note.id,
            "valeur": note.valeur,
            "coefficient": note.coefficient,
            "date_evaluation": note.date_evaluation.isoformat(),
            "commentaire": note.commentaire,
            "etudiant_id": note.etudiant_id,
            "matiere_id": note.matiere_id
        }
        for note in notes
    ]
    return jsonify(result)



# POST : ajouter une note
@app.route("/notes", methods=["POST"])
def add_note():
    data = request.get_json()
    etudiant_id = data.get("etudiant_id")

    # Vérifier si l'étudiant existe via le service étudiant
    try:
        r = requests.get(f"http://etudiants-service/etudiants/{etudiant_id}")
        if r.status_code != 200:
            return jsonify({"error": "Étudiant non trouvé"}), 404
    except Exception as e:
        return jsonify({"error": f"Erreur connexion service étudiant: {e}"}), 500

    note = Note(
        etudiant_id=etudiant_id,
        matiere_id=data.get("matiere_id"),
        valeur=data.get("valeur"),
        coefficient=data.get("coefficient", 1),
        date_evaluation=data.get("date_evaluation"),
        commentaire=data.get("commentaire", "")
    )
    db.session.add(note)
    db.session.commit()
    return jsonify({"message": "Note ajoutée", "id": note.id}), 201

@app.route("/notes/<int:id>", methods=["GET"])
def get_note_by_id(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({"error": "Note introuvable"}), 404

    return jsonify({
        "id": note.id,
        "valeur": note.valeur,
        "coefficient": note.coefficient,
        "date_evaluation": note.date_evaluation.isoformat(),
        "commentaire": note.commentaire,
        "etudiant_id": note.etudiant_id,
        "matiere_id": note.matiere_id,
        "etudiant": {
            "id": note.etudiant.id,
            "nom": note.etudiant.nom,
            "prenom": note.etudiant.prenom
        },
        "matiere": {
            "id": note.matiere.id,
            "nom": note.matiere.nom
        }
    })
@app.route("/notes/<int:id>", methods=["PUT"])
def update_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({"error": "Note introuvable"}), 404

    data = request.get_json()
    try:
        note.etudiant_id = data.get("etudiant_id", note.etudiant_id)
        note.matiere_id = data.get("matiere_id", note.matiere_id)
        note.valeur = data.get("valeur", note.valeur)
        note.date_evaluation = data.get("date_evaluation", note.date_evaluation)
        note.coefficient = data.get("coefficient", note.coefficient)
        note.commentaire = data.get("commentaire", note.commentaire)

        db.session.commit()
        return jsonify({"message": "Note mise à jour avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
@app.route("/notes/<int:id>", methods=["DELETE"])
def delete_note(id):
    note = Note.query.get(id)
    if not note:
        return jsonify({"error": "Note introuvable"}), 404

    try:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"message": "Note supprimée avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)