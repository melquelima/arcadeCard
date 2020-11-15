
from app import app
from flask import render_template,jsonify
from app.models.tables import Maquinas
from app.models.uteis import mallowList,admin_required_route
from app.models.marshmallow import MaquinasSchema
from flask_login import current_user,login_required

@app.route("/nova")
@login_required
@admin_required_route()
def nova():
    return render_template("maquinas/novaMaquina.html",title="Nova Máquina",OBJ=[])



@app.route("/maquinas/<int:id_locador>/<int:id_maquina>")
@app.route("/maquinas/*/<int:id_maquina>")
@app.route("/maquinas/<int:id_locador>")
@app.route("/maquinas")

@login_required
def maquinas(id_locador=None,id_maquina=None):
    data = {"id_locador":id_locador,"id_maquina":id_maquina,"id_usuarioAtual":current_user.id,"admin":current_user.is_admin}
    return render_template("maquinas/maquinas.html",title="Máquinas",OBJ=data)


@app.route("/logs")
@login_required
def logs():
    return render_template("maquinas/logs.html",title="Logs",OBJ=[])