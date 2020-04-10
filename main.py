from flask import Flask, request, make_response

app = Flask(__name__)


@app.route('/')
def index():
    user_ip = request.remote_addr
    response = make_response(redirect('/hello'))
    response.set_cookie('user_ip','user_ip')
    return response


@app.route('/')
def hello():
    user_ip = request.cookies.get('user_ip')
    return 'Hello work flask, tu ip es {}'.format(user_ip)