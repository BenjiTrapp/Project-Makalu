from flask import Flask, request, render_template, redirect, url_for, session, flash
from random import choice, random
from ServerSideSession import VolatileServerSideSessionInterface
from uuid import uuid4

import string

ORDER_ARTICLE_INITIAL_STEP = 1
ORDER_ARTICLE_WORKFLOW_STEPS = 4

uuid = uuid4

app = Flask(__name__)
app.session_interface = VolatileServerSideSessionInterface()

__users = {'user': 'hallo'}
__max_notes = 3
__articles = [(1, 'Article1'),
              (2, 'Article2'),
              (3, 'Article3')]


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if __is_login_session():
        return redirect(url_for('home'))

    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['user']

        try:
            password = __users[username]
        except KeyError:
            return render_template("login.html", message = "User " + username + " unknown!")

        if password == request.form['pwd']:
            session['user'] = username
            __create_new_csrf_token()
            if 'redirectto' in request.form:
                return redirect(url_for(request.form['redirectto']))
        else:
            return render_template("login.html", message = "Login failed!")


@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html", message = "You have successfully logged out.")


@app.route('/CSRFProtected', methods = ['POST', 'GET'])
def CSRFProtection():
    if not __is_login_session():
        return redirect(url_for('login', redirectto = 'CSRFProtection'))

    if request.method == 'GET':
        return render_template("CSRFForm.html")
    elif request.method == 'POST':
        if not __is_csrf_token_valid():
            return render_template("message.html", message = "CSRF validation failed!")
        else:
            return render_template("CSRFShow.html")


@app.route('/ProbabilisticLogout', methods = ['POST', 'GET'])
def ProbabilisticLogout():
    if not __is_login_session():
        return redirect(url_for('login', redirectto = 'ProbabilisticLogout'))

    if request.method == 'GET':
        return render_template("ProbForm.html", fields = list(string.ascii_lowercase))
    elif request.method == 'POST':
        if random() < 0.2:
            return logout()
        else:
            if __is_csrf_token_valid():
                return render_template("ProbShow.html", fields = list(string.ascii_lowercase))
            else:
                return render_template("message.html", message = "CSRF validation failed!")


@app.route('/OrderArticle/<int:step>', methods = ['POST', 'GET'])
def OrderArticle(step):
    if not __is_login_session():
        return redirect(url_for('login', redirectto = 'ProbabilisticLogout'))

    if 'step' not in session:
        session['step'] = ORDER_ARTICLE_INITIAL_STEP

    if session['step'] < step:
        return render_template("message.html", message = "Order Article request doesn't match the OrderArticle state!")

    if session['step'] != step:
        session['step'] = step

    if request.method == 'GET':
        return render_template("OrderArticle-Step{}.html".format(step), articles = __articles)
    elif request.method == 'POST':
        if not __is_csrf_token_valid():
            return render_template("message.html", message = "CSRF validation failed!")

        if step < ORDER_ARTICLE_WORKFLOW_STEPS:
            for param in request.form:
                session['wf_' + param] = request.form[param]

            session['step'] += 1
            return redirect(url_for('OrderArticle', step = session['step']))
        else:
            session['step'] = 1
            return render_template("message.html", message = "Thanks for your order! "
                                                             "Your article will be delivered soon!")


@app.route('/Notes', methods = ['POST', 'GET'])
def Notes():
    if not __is_login_session():
        return redirect(url_for('login', redirectto = 'Notes'))

    if 'notes' not in session:
        session['notes'] = dict()

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        if request.form['action'] == 'add':
            if len(session['notes']) >= __max_notes:
                flash("No more notes allowed!")
            else:
                note = {'subject': request.form['subject'], 'content': request.form['content']}
                session['notes'][str(uuid())] = note
                flash("Note was added")

        if request.form['action'] == 'delete':
            nid = request.form['id']
            if nid in session['notes']:
                subject = session['notes'][nid]['subject']
                del session['notes'][nid]
                flash("Note '%s' deleted" % (subject))
            else:
                flash("Note with id '%s' doesn\'t exists" % nid)

    return render_template("notes.html", notes = session['notes'])


def __is_login_session():
    return 'user' in session


def __is_csrf_token_valid():
    try:
        __session_token = session['csrftoken']
        __create_new_csrf_token()
        return __session_token == request.form['csrftoken']
    except:
        return False


def __create_new_csrf_token():
    session['csrftoken'] = "".join([choice(string.ascii_letters) for i in range(32)])



if __name__ == '__main__':
    app.run(port = 8001, debug = False)
