from flask import Flask, request, jsonify
from models import db
from models.models import Etudiant

app = Flask(__name__)

# Connexion PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@postgresql-service:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/init-db") 
def create_tables():
    # db.drop_all()
    db.create_all()
    return "✅ Base de données initialisée !"

    

# Connexion d'un etudiant
@app.route("/login", methods=["POST"])
def login_etudiant():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    etudiant = Etudiant.query.filter_by(email=email).first()

    if not etudiant:
        return jsonify({"error": "Email non trouvé"}), 404

    if etudiant.password != password:
        return jsonify({"error": "Mot de passe incorrect"}), 401

    return jsonify({
        "id": etudiant.id,
        "nom": etudiant.nom,
        "prenom": etudiant.prenom,
        "email": etudiant.email,
        "age": etudiant.age,              
        "niveau": etudiant.niveau
    }), 200

# GET : récupérer tous les étudiants
@app.route("/etudiants", methods=["GET"])
def get_etudiants():
    etudiants = Etudiant.query.all()
    resultats = []
    for e in etudiants:
        notes_data = [
            {
                "id": note.id,
                "matiere_id": note.matiere_id,
                "valeur": note.valeur
            } for note in e.notes
        ]
        resultats.append({
            "id": e.id,
            "nom": e.nom,
            "prenom": e.prenom,
            "email": e.email,
            "age": e.age,
            "niveau": e.niveau,
            "notes": notes_data  # ajoute cette clé
        })
    return jsonify(resultats)




# POST : ajouter un nouvel étudiant
@app.route("/etudiants", methods=["POST"])
def add_etudiant():
    data = request.get_json()
    print(data)

    # Normalisation du niveau avant création de l'étudiant
    niveau_input = data.get("niveau", "").strip().lower()
    mapping = {
        "l1": "L1",
        "l2": "L2",
        "l3": "L3",
        "master1": "M1",
        "master 1": "M1",
        "m1": "M1",
        "master2": "M2",
        "master 2": "M2",
        "m2": "M2",
        "doctorat": "Doctorat",
        "phd": "Doctorat"
    }
    niveau_final = mapping.get(niveau_input, niveau_input.upper())

    try:
        nouvel_etudiant = Etudiant(
            nom=data.get("nom"),
            prenom=data.get("prenom"),
            email=data.get("email"),
            password=data.get("password"),
            age=data.get("age"),
            niveau=niveau_final  # 💡 bien utiliser la valeur normalisée ici
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
        notes_data = [
            {
                "id": note.id,
                "matiere_id": note.matiere_id,
                "valeur": note.valeur,
                "coefficient": note.coefficient,
                "date_evaluation": note.date_evaluation.isoformat(),
                "commentaire": note.commentaire or ""
            }
            for note in etudiant.notes
        ]

        return jsonify({
            "id": etudiant.id,
            "nom": etudiant.nom,
            "prenom": etudiant.prenom,
            "email": etudiant.email,
            "age": etudiant.age,
            "niveau": etudiant.niveau,
            "notes": notes_data  
        })
    else:
        return jsonify({"error": "Étudiant non trouvé"}), 404

# PUT : modifier un étudiant existant
@app.route("/etudiants/<int:id_etudiant>", methods=["PUT"])
def update_etudiant(id_etudiant):
    etudiant = Etudiant.query.get(id_etudiant)
    if not etudiant:
        return jsonify({"error": "Étudiant non trouvé"}), 404

    data = request.get_json()
    try:
        etudiant.nom = data.get("nom", etudiant.nom)
        etudiant.prenom = data.get("prenom", etudiant.prenom)
        etudiant.email = data.get("email", etudiant.email)
        etudiant.age = data.get("age", etudiant.age)
        etudiant.niveau = data.get("niveau", etudiant.niveau)
        etudiant.normalize_niveau()

        db.session.commit()
        return jsonify({"message": "Étudiant mis à jour avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Delete un etudiant
@app.route("/etudiants/<int:id_etudiant>", methods=["DELETE"])
def delete_etudiant(id_etudiant):
    etudiant = Etudiant.query.get(id_etudiant)
    if not etudiant:
        return jsonify({"error": "Étudiant non trouvé"}), 404

    try:
        db.session.delete(etudiant)
        db.session.commit()
        return jsonify({"message": "Étudiant supprimé avec succès."}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
