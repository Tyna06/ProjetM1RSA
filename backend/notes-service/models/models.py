from . import db
from datetime import date
from sqlalchemy import Enum

niveau_enum = Enum('L1', 'L2', 'L3', 'M1', 'M2', 'Doctorat', name='niveau_enum', create_type=False)

class Etudiant(db.Model):
    __tablename__ = "etudiants"
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), nullable=False)
    prenom = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    age = db.Column(db.Integer)
    niveau = db.Column(niveau_enum)
    notes = db.relationship("Note", backref="etudiant", lazy=True, cascade="all, delete-orphan")
    def normalize_niveau(self):
        if self.niveau:
            self.niveau = self.niveau.strip().lower()
            mapping = {
                'l1': 'L1',
                'l2': 'L2',
                'l3': 'L3',
                'master1': 'M1',
                'm1': 'M1',
                'master 1': 'M1',
                'master2': 'M2',
                'm2': 'M2',
                'master 2': 'M2',
                'doctorat': 'Doctorat',
                'phd': 'Doctorat'
            }
            self.niveau = mapping.get(self.niveau, self.niveau.upper())

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

