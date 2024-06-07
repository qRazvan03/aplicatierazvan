import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # pentru a dezactiva mesajele de avertizare
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nume_utilizator = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    parola = db.Column(db.String(150), nullable=False)
    cod_postal = db.Column(db.String(10), nullable=False)
    adresa_domiciliu = db.Column(db.String(200), nullable=False)
    sex = db.Column(db.String(10), nullable=False)

@app.before_first_request
def create_tables():
    os.makedirs(app.instance_path, exist_ok=True)  # asigură-te că folderul instance există
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/despre')
def despre():
    return render_template('despre.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.filter_by(id=session['user_id']).first()
    users = User.query.all()
    return render_template('dashboard.html', user=user, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nume_utilizator = request.form['nume_utilizator']
        parola = request.form['parola']

        user = User.query.filter_by(nume_utilizator=nume_utilizator).first()
        if user and check_password_hash(user.parola, parola):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            flash('Credențiale invalide. Vă rugăm să încercați din nou.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nume_utilizator = request.form['nume_utilizator']
        email = request.form['email']
        parola = request.form['parola']
        cod_postal = request.form['cod_postal']
        adresa_domiciliu = request.form['adresa_domiciliu']
        sex = request.form['sex']

        hashed_password = generate_password_hash(parola, method='sha256')
        new_user = User(nume_utilizator=nume_utilizator, email=email, parola=hashed_password, cod_postal=cod_postal, adresa_domiciliu=adresa_domiciliu, sex=sex)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Înregistrare reușită. Vă rugăm să vă autentificați.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        # Logica pentru trimiterea mesajului, cum ar fi trimiterea unui email
        return redirect(url_for('index'))
    return render_template('contact.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)