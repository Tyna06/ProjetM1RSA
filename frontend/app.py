from flask import Flask, render_template, request, redirect, url_for, session

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
    if request.method == 'POST':
        role = request.form.get('role')
        session['username'] = request.form.get('username')
        session['role'] = role
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif role == 'student':
            return redirect(url_for('student_dashboard'))
    return render_template('login.html')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        # Simule création
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        email = request.form.get('email')
        print(f"Nouvel utilisateur : {nom} {prenom} ({email})")
        return redirect(url_for('login'))
    return render_template('sign_in.html')

# ==== Dashboards ====
@app.route('/admin')
def admin_dashboard():
    if session.get('role') == 'admin':
        return render_template('dashboard_admin.html', 
                               nombre_etudiants=len(etudiants_list),
                               moyenne_generale=12.0, 
                               nombre_evaluations=5)
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    if session.get('role') == 'student':
        return render_template('dashboard_student.html')
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
    return render_template('ajouter_etudiant.html')

@app.route('/etudiant/liste')
def liste_etudiants():
    return render_template('liste_etudiants.html', etudiants=etudiants_list)

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
    return render_template('details_etudiant.html', etudiant=etudiant)
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

    return render_template('modifier_etudiant.html', etudiant=etudiant)
@app.route('/etudiant/supprimer/<int:id>', methods=['POST'])
def supprimer_etudiant(id):
    global etudiants_list
    etudiants_list = [e for e in etudiants_list if e['id'] != id]
    return redirect(url_for('liste_etudiants'))

# ==== Notes ====
@app.route('/notes')
def liste_notes():
    return render_template('liste_notes.html', 
                           etudiants=etudiants_list, 
                           matieres=matieres, 
                           niveaux=niveaux, 
                           matieres_affichees=matieres, 
                           nombre_etudiants=len(etudiants_list), 
                           moyenne_generale=12.0, 
                           nombre_evaluations=6)

@app.route('/notes/ajouter', methods=['GET', 'POST'])
def ajouter_note():
    if request.method == 'POST':
        print(request.form)  # Simule enregistrement
        return redirect(url_for('liste_notes'))
    return render_template('ajouter_note.html', etudiants=etudiants_list, matieres=matieres)

# ==== Accès rapide admin ====
@app.route('/admin-direct')
def admin_direct():
    session['role'] = 'admin'
    return redirect(url_for('admin_dashboard'))

# ==== Lancement ====
if __name__ == '__main__':
    app.run(debug=True)
