from app import app
from flask import render_template,request,jsonify
from flask_login import current_user,login_required


@app.route("/novoUsuario")
@login_required
def new_user():
    return render_template("usuarios/novoUsuario.html",title="Novo Usuario",OBJ=[])


@app.route("/usuarios")
@login_required
def users():
    return render_template("usuarios/usuarios.html",title="Usuarios",OBJ=[])


@app.route("/carregar")
@login_required
def users_carregar():
    return render_template("usuarios/carregar.html",title="Carregar",OBJ=[])
