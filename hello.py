from flask import Flask, render_template, request, redirect, url_for, session, flash
from function import valid_login, reverse_word, calculate_tva, calcuate_letter
from pprint import pprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from models.user import User

app = Flask(__name__)
app.secret_key = "test"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost:3306/b2-paris'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt(app)

@app.get("/")
def index():
    return render_template('index.html')


@app.get('/about')
def about():
    return render_template('about.html')


@app.get('/register')
def register():
    return render_template('auth/register.html')


@app.post('/inscription')
def inscription():
    pprint(request.form)
    user = User(
        username=request.form['username'],
        password=bcrypt.generate_password_hash(request.form['password'])
    )

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        # Récupérer le User par son username
        user = db.session.execute(db.select(User).filter_by(username=request.form['username'])).scalar()

        if user is None:
            error = 'Invalid username/password'
        else:
            # Check si le mot de passe est egale à celui du formulaire
            if bcrypt.check_password_hash(user.password, request.form['password']):
                session['username'] = request.form['username']
                return redirect(url_for('profile'))
            else:
                error = 'Invalid username/password'

    return render_template('auth/login.html', error=error)


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'username' in session:
        # Vérifier qu'on est sur l'envoi du formulaire
        if request.method == 'POST':
            # Récupérer les infos du formulaire
            username = request.form['username']
            password = request.form['password']
            password_cf = request.form['password_cf']

            # Vérifier qu'elles ne sont pas vide et que les deux passwords correspondent
            if username is None or username == "" or password is None or password == "" or password != password_cf:
                flash('Les données ne sont pas valides')
            else:
                # Vérifier si le nouveau username existe déjà
                userOld = db.session.execute(db.select(User).filter_by(username=username)).scalar()

                if username != session['username'] and userOld is not None:
                    # renvoyer un flash message
                    flash('Ce username est déjà utilisé')
                else:
                    user = db.session.execute(db.select(User).filter_by(username=session['username'])).scalar()

                    # Mettre à jour la bdd et la session
                    user.username = username
                    user.password = bcrypt.generate_password_hash(password)
                    db.session.commit()

                    session['username'] = username

                    # Créer une message pour le user
                    flash('User bien mise à jour')


        return render_template('profile.html', username=session['username'])
    else:
        return redirect(url_for('login'))


@app.get('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)

    return redirect(url_for('login'))


@app.get('/sapin')
def sapin():
    return render_template('sapin.hml', taille=10)

@app.get('/transform/<word>')
def transform(word: str):
    return render_template('transform.html', reverseWord = reverse_word(word))


@app.route('/transform', methods=['POST', 'GET'])
def postTransform():
    word = ""

    if request.method == 'POST':
        word = request.form['word']

    return render_template('formTransform.html', transm_word=reverse_word(word))

@app.route('/tva', methods=['POST', 'GET'])
def tva():
    price = ""
    taux = ""
    total_tva = ""

    if request.method == 'POST':
        price = int(request.form['price'])
        taux = int(request.form['taux'])
        total_tva = calculate_tva(price, taux)

    return render_template('tva.html', price=price, total_tva=total_tva)

# calcuate_letter

@app.route('/calcuate', methods=['POST', 'GET'])
def calculate():
    word = ""

    if request.method == 'POST':
        word = request.form['word']

    return render_template('calculate.html', result = calcuate_letter(word))

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
