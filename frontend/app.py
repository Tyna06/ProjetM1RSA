from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import requests


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'secret_key'




matieres = [
    {'id': 1, 'nom': 'Mathématiques'},
    {'id': 2, 'nom': 'Physique'}
]


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
                r = requests.post("http://etudiants-service/login", json={"email": email, "password": password})
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
                response = requests.post("http://etudiants-service/etudiants", json={
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
        try:
            r = requests.get("http://etudiants-service/etudiants")
            if r.status_code == 200:
                etudiants = r.json()
                nombre_etudiants = len(etudiants)
            else:
                etudiants = []
                nombre_etudiants = 0
        except Exception as e:
            etudiants = []
            nombre_etudiants = 0

        # Calcul dynamique des statistiques
        total_notes = 0
        total_valeurs = 0

        for etudiant in etudiants:
            notes = etudiant.get('notes', [])
            valeurs = [note['valeur'] for note in notes]
            total_notes += len(valeurs)
            total_valeurs += sum(valeurs)

        moyenne_generale = round(total_valeurs / total_notes, 2) if total_notes > 0 else 0.0
        date_du_jour = datetime.now().strftime("%d/%m/%Y")

        return render_template('admin/dashboard_admin.html',
                               nombre_etudiants=nombre_etudiants,
                               moyenne_generale=moyenne_generale,
                               nombre_evaluations=total_notes,
                               date_du_jour=date_du_jour)

    return redirect(url_for('login'))





# ==== Étudiants ====

@app.route('/etudiant/ajouter', methods=['GET', 'POST'])
def ajouter_etudiant():
    if request.method == 'POST':
        etudiant_data = {
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'email': request.form.get('email'),
            'age': request.form.get('age'),
            'niveau': request.form.get('niveau'),
            'password': request.form.get('password')

        }

        try:
            r = requests.post('http://etudiants-service/etudiants', json=etudiant_data)
            if r.status_code == 201:
                return redirect(url_for('liste_etudiants'))
            else:
                error = f"Erreur: {r.json().get('erreur', 'Inconnue')}"
        except Exception as e:
            error = f"Erreur de connexion au microservice : {e}"

        return render_template('admin/ajouter_etudiant.html', error=error)

    return render_template('admin/ajouter_etudiant.html')

# Lister les etudiants 

@app.route('/etudiant/liste')
def liste_etudiants():
    try:
        r = requests.get("http://etudiants-service/etudiants")
        if r.status_code == 200:
            etudiants = r.json()
        else:
            etudiants = []
            error = f"Erreur: {r.status_code}"
    except Exception as e:
        etudiants = []
        error = f"Erreur connexion microservice : {e}"

    return render_template('admin/liste_etudiants.html', etudiants=etudiants)


# Détail d'un etudiant spécifique

@app.route('/etudiant/<int:id>')
def details_etudiant(id):
    try:
        r = requests.get(f"http://etudiants-service/etudiants/{id}")
        if r.status_code == 200:
            etudiant = r.json()
        else:
            return "Étudiant non trouvé", 404
    except Exception as e:
        return f"Erreur lors de la connexion au microservice : {e}", 500

    try:
        r = requests.get("http://notes-service/matieres")
        matieres = r.json() if r.status_code == 200 else []
        print(" Matières récupérées :", matieres)
    except:
        matieres = []

    # Remplacer les IDs des matières par leur nom
    for note in etudiant.get("notes", []):
        matiere_nom = next((m['nom'] for m in matieres if m['id'] == note['matiere_id']), "Inconnue")
        note['matiere_nom'] = matiere_nom

        # Conversion de la date_evaluation en datetime si c'est une chaîne
        if isinstance(note.get('date_evaluation'), str):
            note['date_evaluation'] = datetime.strptime(note['date_evaluation'], "%Y-%m-%d").date()

    # Calcul de la moyenne (optionnel ici si le microservice ne la fournit pas)
    if etudiant.get("notes"):
        total = sum(n['valeur'] * n['coefficient'] for n in etudiant['notes'])
        coef_total = sum(n['coefficient'] for n in etudiant['notes'])
        etudiant['moyenne'] = round(total / coef_total, 2) if coef_total > 0 else None
    else:
        etudiant['moyenne'] = None

    return render_template('admin/details_etudiant.html', etudiant=etudiant)

# Supprimer un etudiant 
@app.route('/etudiant/supprimer/<int:id>', methods=['POST'])
def supprimer_etudiant(id):
    try:
        r = requests.delete(f"http://etudiants-service/etudiants/{id}")
        if r.status_code == 200:
            return redirect(url_for('liste_etudiants'))
        else:
            return f"Erreur : {r.status_code}", 400
    except Exception as e:
        return f"Erreur de connexion au microservice : {e}", 500

# Modifier etudiant 
@app.route('/etudiant/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_etudiant(id):
    try:
        r = requests.get(f"http://etudiants-service/etudiants/{id}")
        if r.status_code != 200:
            return "Étudiant introuvable", 404
        etudiant = r.json()
    except Exception as e:
        return f"Erreur de récupération : {e}", 500

    if request.method == 'POST':
        updated_data = {
            'nom': request.form.get('nom'),
            'prenom': request.form.get('prenom'),
            'email': request.form.get('email'),
            'age': request.form.get('age'),
            'niveau': request.form.get('niveau'),
            'password': request.form.get('password')  # si tu veux permettre la modif
        }
        try:
            r = requests.put(f"http://etudiants-service/etudiants/{id}", json=updated_data)
            if r.status_code == 200:
                return redirect(url_for('liste_etudiants'))
            else:
                error = r.json().get("erreur", "Erreur lors de la mise à jour.")
        except Exception as e:
            error = f"Erreur de connexion : {e}"
        return render_template('admin/modifier_etudiant.html', etudiant=etudiant, error=error)

    return render_template('admin/modifier_etudiant.html', etudiant=etudiant)

# ==== Notes ====
# Update un etudiant info
@app.route('/notes/modifier/<int:id>', methods=['GET', 'POST'])
def modifier_note(id):
    error = None

    if request.method == 'POST':
        data = {
            "etudiant_id": int(request.form.get('etudiant_id')),
            "matiere_id": int(request.form.get('matiere_id')),
            "valeur": float(request.form.get('note')),
            "date_evaluation": request.form.get('date_evaluation'),
            "coefficient": int(request.form.get('coefficient')),
            "commentaire": request.form.get('commentaire')
        }

        try:
            r = requests.put(f"http://notes-service/notes/{id}", json=data)
            if r.status_code == 200:
                return redirect(url_for('liste_notes'))
            else:
                error = f"Erreur : {r.status_code}"
        except Exception as e:
            error = f"Erreur de connexion au microservice : {e}"

    # GET : afficher la note à modifier
    try:
        r_note = requests.get(f"http://notes-service/notes/{id}")
        r_matieres = requests.get("http://notes-service/matieres")
        if r_note.status_code == 200 and r_matieres.status_code == 200:
            note = r_note.json()
            matieres_list = r_matieres.json()
            return render_template("admin/modifier_note.html", note=note, matieres=matieres_list, error=error)
        else:
            return "Note introuvable", 404
    except Exception as e:
        return f"Erreur de récupération : {e}", 500

@app.route('/notes')
def liste_notes():
    
    try:
        r = requests.get("http://etudiants-service/etudiants")
        etudiants = r.json() if r.status_code == 200 else []
    except Exception as e:
        etudiants = []
        
    print("Étudiants reçus :")
    for e in etudiants:
        print(e)

    total_notes = 0
    total_valeurs = 0

    for etudiant in etudiants:
        notes = etudiant.get('notes', [])

        # ✅ Ajoute cette ligne pour conserver les notes complètes avec id
        etudiant['notes'] = notes

        # ✅ Dictionnaire pour l'affichage simple des notes
        etudiant['notes_dict'] = {note['matiere_id']: note['valeur'] for note in notes}

        # ✅ Calcule la moyenne
        valeurs = [note['valeur'] for note in notes]
        etudiant['moyenne'] = round(sum(valeurs) / len(valeurs), 2) if valeurs else 0.0

        # ✅ Incrémente les totaux pour la moyenne générale
        total_notes += len(valeurs)
        total_valeurs += sum(valeurs)
    moyenne_generale = round(total_valeurs / total_notes, 2) if total_notes > 0 else 0.0
    try:
        r = requests.get("http://notes-service/matieres")
        matieres = r.json() if r.status_code == 200 else []
        print("📚 Matières récupérées :", matieres)

    except:
        matieres = []
    niveaux = ["L1", "L2", "L3", "M1", "M2", "Doctorat"]
    
    return render_template("admin/liste_etudiants_note.html",
                           etudiants=etudiants,
                           matieres=matieres,
                           niveaux=niveaux,
                           matieres_affichees=matieres,
                           nombre_etudiants=len(etudiants),
                           moyenne_generale=moyenne_generale,
                           nombre_evaluations=total_notes,
                           search_name='',
                           matiere_id='',
                           niveau_filtre='')


# Ajout Notes
@app.route('/notes/ajouter', methods=['GET', 'POST'])
def ajouter_note():
    error = None

    # Toujours récupérer les étudiants et matières, quelle que soit la méthode
    try:
        r = requests.get("http://etudiants-service/etudiants")
        etudiants = r.json() if r.status_code == 200 else []
    except:
        etudiants = []

    try:
        r = requests.get("http://notes-service/matieres")
        matieres = r.json() if r.status_code == 200 else []

    except:
        matieres = []

    if request.method == 'POST':
        try:
            etudiant_id = int(request.form.get('etudiant_id'))
            matiere_id = int(request.form.get('matiere_id'))
            note_valeur = float(request.form.get('note'))
            date_evaluation = request.form.get('date_evaluation')
            coefficient = int(request.form.get('coefficient'))
            commentaire = request.form.get('commentaire')

            r = requests.post("http://notes-service/notes", json={
                "etudiant_id": etudiant_id,
                "matiere_id": matiere_id,
                "valeur": note_valeur,
                "date_evaluation": date_evaluation,
                "coefficient": coefficient,
                "commentaire": commentaire
            })

            if r.status_code == 201:
                return redirect(url_for('liste_notes'))
            else:
                error = f"Erreur : {r.json().get('erreur', 'Ajout impossible')}"
        except Exception as e:
            error = f"Erreur microservice : {e}"

    return render_template('admin/ajouter_note.html', etudiants=etudiants, matieres=matieres, error=error)

# ==== Accès rapide etudiant ====

@app.route('/student-direct/<int:id>')
def student_direct(id):
    session['role'] = 'student'
    session['student_id'] = id
    return redirect(url_for('dashboard_etudiant', id=id))



@app.route("/student/dashboard/<int:id>")
def dashboard_etudiant(id):
    if session.get('role') != 'student' or session.get('student_id') != id:
        return redirect(url_for('login'))

    try:
        r = requests.get(f"http://etudiants-service/etudiants/{id}")
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
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
