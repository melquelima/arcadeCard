from app import app
from flask import render_template,request,jsonify
from flask_login import current_user,login_required


@app.route("/novoUsuario")
@login_required
def new_user():
    return render_template("usuarios/novoUsuario.html",title="Novo Usuario",OBJ=[])


@app.route("/usuarios")
@app.route("/usuarios/<int:id_locador>")
@app.route("/usuarios/<int:id_locador>/<int:id_user>")
@app.route("/usuarios/*/<int:id_user>")
@login_required
def users(id_locador=None,id_user=None):
    data = {
        "id_locador":id_locador,
        "id_user":id_user,
        "admin":current_user.is_admin,
        "id_usuarioAtual":current_user.id
        }
    return render_template("usuarios/usuarios.html",title="Usuarios",OBJ=data)


@app.route("/carregar")
@login_required
def users_carregar():
    return render_template("usuarios/carregar.html",title="Carregar",OBJ=[])
