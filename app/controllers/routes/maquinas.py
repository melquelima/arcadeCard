
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


@app.route("/maquinas")
@app.route("/maquinas/<int:id>")
@login_required
def maquinas(id=None):
    if not id is None:
        if current_user.is_admin:
            itens = Maquinas.query.filter(Maquinas.sysUser.has(id=id)).all()
        else:
            itens = []
    else:
        if current_user.is_admin: #se for admin mostra todos os Logs se nao, mostra apenas os logs do usuario
            itens = Maquinas.query.all()
        else:
            itens = Maquinas.query.filter(Maquinas.sysUser.has(id=current_user.id)).all()

    itens = mallowList(MaquinasSchema,itens)
    data = {"lista":itens,"admin":current_user.is_admin}
    return render_template("maquinas/maquinas.html",title="Máquinas",OBJ=data)


@app.route("/logs")
@login_required
def logs():
    return render_template("maquinas/logs.html",title="Logs",OBJ=[])