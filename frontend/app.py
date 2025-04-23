from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Simule une vérification
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
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        age = request.form.get('age')
        niveau = request.form.get('niveau')
        email = request.form.get('email')

        # Simule la création (plus tard tu pourras appeler ton microservice ici)
        print(f"Nouvel utilisateur : {nom}, {prenom}, {email}, {age}, {niveau}")

        # Après inscription, redirige vers la connexion
        return redirect(url_for('login'))

    return render_template('sign_in.html')

@app.route('/admin')
def admin_dashboard():
    if session.get('role') == 'admin':
        return render_template('dashboard_admin.html')
    return redirect(url_for('login'))

@app.route('/student')
def student_dashboard():
    if session.get('role') == 'student':
        return render_template('dashboard_student.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
