from flask import Flask, request, jsonify
from models import db
from models.models import Etudiant, Note, Matiere

app = Flask(__name__)

# Connexion PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@localhost:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/init-db") 
def create_tables():
    db.create_all()
    return "✅ Base de données initialisée !"

    
# GET : récupérer tous les étudiants
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    etudiants = Etudiant.query.all()
    return jsonify([{"id": e.id, "nom": e.nom, "email": e.email} for e in etudiants])

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
    try:
        nouvel_etudiant = Etudiant(
            nom=data.get("nom"),
            email=data.get("email"),
            mot_de_passe=data.get("mot_de_passe"),
            age=data.get("age"),
            niveau=data.get("niveau")
        )
        db.session.add(nouvel_etudiant)
        db.session.commit()
        return jsonify({"message": "Étudiant ajouté", "etudiant": {"id": nouvel_etudiant.id}}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": str(e)}), 400
    
  
# GET : récupérer un étudiant par ID
@app.route("/etudiants/<int:id_etudiant>", methods=["GET"])
def get_etudiant(id_etudiant):
    etudiant = Etudiant.query.get(id_etudiant)
    if etudiant:
        return jsonify({
            "id": etudiant.id,
            "nom": etudiant.nom,
            "email": etudiant.email,
            "age": etudiant.age,
            "niveau": etudiant.niveau
        })
    else:
        return jsonify({"error": "Étudiant non trouvé"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
