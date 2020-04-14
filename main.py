from flask import Flask, request, make_response, redirect, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


todos = ['Comprar Cafe', 'Solicitud de compra', 'entregar el produto',]

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
    response.set_cookie('user_ip', user_ip)
    return response


@app.route('/hello')
def hello():
    user_ip = request.cookies.get('user_ip')
    context = {
        'user_ip': user_ip,
        'todos': todos,
    }
    return render_template('hello.html', **context)