from flask import Flask
from models.models import db
from models.models import Matiere

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rsa_user:rsa_pass@localhost:5432/rsa_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    matieres = ["Mathématiques", "Physique", "Chimie", "Informatique"]
    for nom in matieres:
        if not Matiere.query.filter_by(nom=nom).first():
            db.session.add(Matiere(nom=nom))
    db.session.commit()
    print("✅ Matières insérées avec succès.")
