import unittest
from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash

from flask_login import login_required, current_user
from app import craete_app
from app.forms import TodoForm, DeleteTodoForm, UpdateTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo


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


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    #login_form = LoginForm()
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()
    update_form = UpdateTodoForm()
    username = current_user.id
    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        #'login_form':login_form,
        'username': username,
        'todo_form':todo_form,
        'delete_form': delete_form,
        'update_form': update_form,
    }
    if todo_form.validate_on_submit():
        put_todo(user_id=username,descripcion=todo_form.description.data)
        flash ('Tu tarea se creo con exito ')
        return redirect(url_for('hello'))
    return render_template('hello.html', **context)


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id,todo_id=todo_id)
    return redirect(url_for('hello'))


@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id=user_id, todo_id=todo_id, done=done)
    return redirect(url_for('hello'))
