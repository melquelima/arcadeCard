
from app import app
from flask import render_template,jsonify
from app.models.tables import SysUser
from app.models.uteis import mallowList,admin_required_route
from flask_login import current_user,login_required

@app.route("/novoLocador")
@login_required
@admin_required_route()
def novoLocador():
    return render_template("locadores/novoLocador.html",title="Novo Locador",OBJ=[])

@app.route("/Locadores")
@app.route("/Locadores/<int:id_locador>")
@login_required
@admin_required_route()
def Locadores(id_locador = None):
    data = {"id_locador":id_locador}
    return render_template("locadores/locadores.html",title="Locadores",OBJ=data)




