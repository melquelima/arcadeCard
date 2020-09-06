from app import app,db
from datetime import timedelta
import sys
from flask import render_template,url_for,request,jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import *
from app.models.marshmallow import *
from datetime import datetime as dt,timedelta
from werkzeug.security import generate_password_hash as GPH, check_password_hash as CPH
from secrets import token_urlsafe
from random import randint


@app.route("/")
@login_required
def index():
    return render_template("index.html",title="DashBoard",OBJ=[])


@app.route("/login2")
def login2():
    return render_template("login2.html")


@app.route("/api/cliUsers",methods=["GET"])
def cliUsers():
    cliUsr = CliUsers.query.all()
    formatado = mallowList(CliUserSchema,cliUsr)
    return jsonify(formatado)

@app.route("/api/updateToken2",methods=["GET"])
@token_required(ignore=True)
def updateToken2(maquina):

    token = jwt.encode({'id_maquina':maquina.id,'control_str':token_urlsafe(8)},app.config['SECRET_KEY']).decode('UTF-8')
    hashed_tkn = GPH(token,method="sha256")
    maquina.token = hashed_tkn

    db.session.commit()
    return token

    
