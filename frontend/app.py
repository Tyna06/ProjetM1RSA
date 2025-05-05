from flask import Flask, render_template, request, redirect, url_for, session
import requests
app = Flask(__name__)
app.secret_key = 'secret_key'

# ==== Données simulées ====
etudiants_list = [
    {'id': 1, 'nom': 'Dupont', 'prenom': 'Jean', 'email': 'jean@exemple.com', 'age': 20, 'niveau': 'L1', 'notes': {1: 14.5, 2: 12}, 'moyenne': 13.25},
    {'id': 2, 'nom': 'Durand', 'prenom': 'Marie', 'email': 'marie@exemple.com', 'age': 22, 'niveau': 'L2', 'notes': {1: 9, 2: 11}, 'moyenne': 10.0},
]

matieres = [
    {'id': 1, 'nom': 'Mathématiques'},
    {'id': 2, 'nom': 'Physique'}
]

niveaux = ['L1', 'L2', 'L3']

# ==== Auth Routes ====
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('adressmail')  # nom du champ dans le HTML
        password = request.form.get('password')
        role = request.form.get('role')

        if role == 'admin':
            if email == "admin@admin.com" and password == "admin":
                session['username'] = email
                session['role'] = role
                return redirect(url_for('admin_dashboard'))
            else:
                error = "Admin incorrect"

        elif role == 'student':
            try:
                r = requests.post("http://localhost:5001/login", json={"email": email, "password": password})
                if r.status_code == 200:
                    data = r.json()
                    session['username'] = email
                    session['role'] = role
                    session['student_id'] = data['id']
                    session['student_nom'] = data.get('nom')
                    session['student_prenom'] = data.get('prenom')
                    session['student_email'] = data.get('email')
                    session['student_age'] = data.get('age')
                    session['student_niveau'] = data.get('niveau')
                    return redirect(url_for('dashboard_etudiant', id=data['id']))
                elif r.status_code == 404:
                    error = "Email introuvable"
                elif r.status_code == 401:
                    error = "Mot de passe incorrect"
                else:
                    error = "Erreur lors de la connexion"
            except Exception as e:
                error = f"Erreur connexion microservice : {e}"

    return render_template('auth/login.html', error=error)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    error = None
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        age = request.form.get('age')
        niveau = request.form.get('niveau')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            error = "Les mots de passe ne correspondent pas."
        else:
            try:
                # Appel microservice
                response = requests.post("http://localhost:5001/etudiants", json={
                    "nom": nom,
                    "prenom": prenom,
                    "age": age,
                    "niveau": niveau,
                    "email": email,
                    "password": password
                })

                if response.status_code == 201:
                    return redirect(url_for('login'))
                else:
                    error = response.json().get("erreur", "Erreur lors de l'inscription.")
            except Exception as e:
                error = f"Erreur de connexion au microservice : {e}"

    return render_template('auth/sign_in.html', error=error)

# ==== Dashboards ====
@app.route('/admin')
def admin_dashboard():
    if session.get('role') == 'admin':
        return render_template('admin/dashboard_admin.html', 
                               nombre_etudiants=len(etudiants_list),
                               moyenne_generale=12.0, 
                               nombre_evaluations=5)
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    if session.get('role') == 'student':
        return render_template('admin/dashboard_student.html')
    return redirect(url_for('login'))

# ==== Étudiants ====
@app.route('/etudiant/ajouter', methods=['GET', 'POST'])
def ajouter_etudiant():
    if request.method == 'POST':
        new_id = len(etudiants_list) + 1
        etudiant = {
            'id': new_id,
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'email': request.form.get('email'),
            'age': request.form.get('age'),
            'niveau': request.form.get('niveau'),
            'notes': {},
            'moyenne': 0.0
        }
        etudiants_list.append(etudiant)
        return redirect(url_for('liste_etudiants'))
    return render_template('admin/ajouter_etudiant.html')

@app.route('/etudiant/liste')
def liste_etudiants():
    return render_template('admin/liste_etudiants.html', etudiants=etudiants_list)

@app.route('/etudiant/<int:id>')
def details_etudiant(id):
    # Simule la récupération d'un étudiant
    etudiant = {
        'id': id,
        'nom': 'Dupont',
        'prenom': 'Alice',
        'email': 'alice.dupont@example.com',
        'age': 21,
        'niveau': 'Licence 3',
        'moyenne': 14.2,
        'notes': [
            {'matiere': 'Mathématiques', 'note': 16, 'date': '2025-03-15', 'coefficient': 2},
            {'matiere': 'Physique', 'note': 12.5, 'date': '2025-03-20', 'coefficient': 1},
            {'matiere': 'Chimie', 'note': 14, 'date': '2025-04-10', 'coefficient': 3},
        ]
    }
    return render_template('admin/details_etudiant.html', etudiant=etudiant)
@app.route('/etudiant/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_etudiant(id):
    etudiant = next((e for e in etudiants_list if e['id'] == id), None)
    if not etudiant:
        return "Étudiant introuvable", 404

    if request.method == 'POST':
        etudiant['nom'] = request.form.get('nom')
        etudiant['prenom'] = request.form.get('prenom')
        etudiant['email'] = request.form.get('email')
        etudiant['age'] = request.form.get('age')
        etudiant['niveau'] = request.form.get('niveau')
        return redirect(url_for('liste_etudiants'))

    return render_template('admin/modifier_etudiant.html', etudiant=etudiant)
@app.route('/etudiant/supprimer/<int:id>', methods=['POST'])
def supprimer_etudiant(id):
    global etudiants_list
    etudiants_list = [e for e in etudiants_list if e['id'] != id]
    return redirect(url_for('liste_etudiants'))

# ==== Notes ====
@app.route('/notes')
def liste_notes():
    search_name = request.args.get('search_name', '')
    matiere_id = request.args.get('matiere_id')
    niveau_filtre = request.args.get('niveau')

    # Filtrage simple (optionnel pour après)
    filtered_etudiants = etudiants_list
    if search_name:
        filtered_etudiants = [e for e in filtered_etudiants if search_name.lower() in (e['nom'] + e['prenom']).lower()]
    if matiere_id:
        matiere_id = int(matiere_id)
        filtered_etudiants = [e for e in filtered_etudiants if matiere_id in e['notes']]
    if niveau_filtre:
        filtered_etudiants = [e for e in filtered_etudiants if e['niveau'] == niveau_filtre]

    return render_template('admin/liste_etudiants_note.html', 
                           etudiants=filtered_etudiants, 
                           matieres=matieres, 
                           niveaux=niveaux, 
                           matieres_affichees=matieres, 
                           nombre_etudiants=len(filtered_etudiants), 
                           moyenne_generale=round(sum(e['moyenne'] for e in filtered_etudiants) / len(filtered_etudiants), 2) if filtered_etudiants else 0,
                           nombre_evaluations=sum(len(e['notes']) for e in filtered_etudiants),
                           search_name=search_name,
                           matiere_id=matiere_id,
                           niveau_filtre=niveau_filtre)


@app.route('/notes/ajouter', methods=['GET', 'POST'])
def ajouter_note():
    if request.method == 'POST':
        # Récupérer les données du formulaire
        etudiant_id = int(request.form.get('etudiant_id'))
        matiere_id = int(request.form.get('matiere_id'))
        note_valeur = float(request.form.get('note'))
        date_evaluation = request.form.get('date_evaluation')
        coefficient = int(request.form.get('coefficient'))
        commentaire = request.form.get('commentaire')

        # Trouver l'étudiant
        etudiant = next((e for e in etudiants_list if e['id'] == etudiant_id), None)
        if etudiant:
            # Ajouter la note à l'étudiant
            etudiant['notes'][matiere_id] = note_valeur

            # Recalcul de la moyenne simple (à affiner avec coefficient si besoin)
            notes_values = etudiant['notes'].values()
            etudiant['moyenne'] = sum(notes_values) / len(notes_values)

        # Retour à la liste des notes
        return redirect(url_for('liste_notes'))

    # GET : afficher le formulaire
    return render_template('admin/ajouter_note.html', etudiants=etudiants_list, matieres=matieres)


# ==== Accès rapide admin ====
@app.route('/admin-direct')
def admin_direct():
    session['role'] = 'admin'
    return redirect(url_for('admin_dashboard'))

# ==== Accès rapide etudiant ====

@app.route('/student-direct/<int:id>')
def student_direct(id):
    session['role'] = 'student'
    session['student_id'] = id
    return redirect(url_for('dashboard_etudiant', id=id))

from datetime import datetime

@app.route("/student/dashboard/<int:id>")
def dashboard_etudiant(id):
    if session.get('role') != 'student' or session.get('student_id') != id:
        return redirect(url_for('login'))

    try:
        r = requests.get(f"http://localhost:5001/etudiants/{id}")
        if r.status_code == 200:
            etudiant = r.json()
            etudiant['prenom'] = session.get('student_prenom', '')
        else:
            return "Étudiant introuvable", 404
    except Exception as e:
        return f"Erreur connexion microservice : {e}", 500

    if not etudiant:
        return "Étudiant introuvable", 404

    notes = []
    for note in etudiant['notes']:
        matiere_nom = next((m['nom'] for m in matieres if m['id'] == note['matiere_id']), 'Inconnue')
        notes.append({
            'matiere': matiere_nom,
            'valeur': note['valeur'],
            'date_evaluation': note.get('date_evaluation', ''),
            'coefficient': note.get('coefficient', 1),
            'commentaire': note.get('commentaire', '')
        })

    moyenne = round(sum(n['valeur'] for n in notes) / len(notes), 2) if notes else 0
    total_notes = len(notes)
    matieres_unique = {note['matiere'] for note in notes}

    return render_template("student/dashboard_etudiant.html",
                           etudiant=etudiant,
                           notes=notes,
                           moyenne_generale=moyenne,
                           total_notes=total_notes,
                           nombre_matieres=len(matieres_unique),
                           date_du_jour=datetime.now().strftime("%d/%m/%Y"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ==== Lancement ====
if __name__ == '__main__':
    app.run(debug=True)
