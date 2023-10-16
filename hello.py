from flask import Flask, render_template, request, redirect, url_for
from function import valid_login

app = Flask(__name__)

@app.get("/")
def hello_world():
    return render_template('hello.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None

    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return redirect(url_for('profile', username=request.form['username']))
        else:
            error = 'Invalid username/password'

    return render_template('login.html', error=error)


@app.get('/profile/<string:username>')
def profile(username):
    return render_template('profile.html', name=username)


if __name__ == '__main__':
    app.run()
