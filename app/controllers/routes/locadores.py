
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
@login_required
@admin_required_route()
def Locadores():
    return render_template("locadores/Locadores.html",title="Locadores",OBJ=[])




