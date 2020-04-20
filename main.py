from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_bootstrap import Bootstrap
import unittest
from app import craete_app
from app.forms import LoginForm
from app.firestore_service import get_users


app = craete_app()

todos = ['Comprar Cafe', 'Solicitud de compra', 'entregar el produto',]

@app.cli.command()
def test():
    tests=unittest.TestLoader().discover('test')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error = error)


@app.errorhandler(505)
def internalt_server_error(error):
    return render_template('server_error.html', error = error)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    #response.set_cookie('user_ip', user_ip)
    session['user_ip']=user_ip
    return response


@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    #login_form = LoginForm()
    username = session.get('username')
    context = {
        'user_ip': user_ip,
        'todos': todos,
        #'login_form':login_form,
        'username': username
    }
    users = get_users()
    for user in users:
        print(user)
    return render_template('hello.html', **context)