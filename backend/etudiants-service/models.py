from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Etudiant(db.Model):
    __tablename__ = "etudiants"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    mot_de_passe = db.Column(db.String(128), nullable=False)  # hashé !
    age = db.Column(db.Integer)
    niveau = db.Column(db.String(32))

    notes = db.relationship("Note", backref="etudiant", lazy=True)


class Matiere(db.Model):
    __tablename__ = "matieres"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    notes = db.relationship("Note", backref="matiere", lazy=True)


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey("etudiants.id"), nullable=False)
    matiere_id = db.Column(db.Integer, db.ForeignKey("matieres.id"), nullable=False)
    valeur = db.Column(db.Float, nullable=False)
    date_evaluation = db.Column(db.Date, default=date.today)
    coefficient = db.Column(db.Integer)
    commentaire = db.Column(db.String(255))
