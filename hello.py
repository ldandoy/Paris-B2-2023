from flask import Flask, render_template, request, redirect, url_for, session
from function import valid_login
from pprint import pprint

app = Flask(__name__)
app.secret_key = "test"


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
    return "test"


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('profile'))
        else:
            error = 'Invalid username/password'

    return render_template('auth/login.html', error=error)


@app.get('/profile')
def profile():
    if 'username' in session:
        return render_template('profile.html', name=session['username'])
    else:
        return redirect(url_for('login'))


@app.get('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
