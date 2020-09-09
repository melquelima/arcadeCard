from app import app,db
from flask import jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import Maquinas,Temas,SysUser,LogMaquinas
from app.models.marshmallow import MaquinasSchema,LogMSchema
from secrets import token_urlsafe
from werkzeug.security import generate_password_hash as GPH
import json
import jwt

@app.route("/api/maquinas",methods=["GET"])
@admin_required()
def Maquinas_fnc():
    cliUsr = Maquinas.query.all()
    formatado = mallowList(MaquinasSchema,cliUsr)
    return jsonify(formatado)


@app.route("/api/maquinas",methods=["POST"])
@login_required
@admin_required()
@fields_required({"id_tema":int,"id_sys_user":int,"nome":str,"descricao":str,"preco":float,"ativa":bool,"free":bool})
def Maquinas_post(fields):
    if fields["nome"] == "": return "O campo 'nome' não pode estar em branco",400

    maquina = Maquinas.query.filter_by(nome=fields["nome"]).all()
    if not maquina:
        sys_user = SysUser.query.get(fields["id_sys_user"])
        if sys_user:
            tema = Temas.query.get(fields["id_tema"])
            if tema:
                maq = Maquinas(**fields)
                maq.save()
                return "OK"
            else:
                return "Tema não encontrado!",400
        else:
            return "Locador não encontrado!",400
    else:
        return "Maquina já existente!",400


@app.route("/api/maquinas",methods=["PUT"])
@login_required
@admin_required()
@fields_required({"id":int,"id_tema":int,"id_sys_user":int,"nome":str,"descricao":str,"preco":float,"ativa":bool,"free":bool})
def Maquinas_put(fields):
    if fields["nome"] == "": return "O campo 'nome' não pode estar em branco",400

    maquina = Maquinas.query.get(fields["id"])
    if maquina:
        sys_user = SysUser.query.get(fields["id_sys_user"])
        if sys_user:
            tema = Temas.query.get(fields["id_tema"])
            if tema:
                maquina.id_sys_user = fields["id_sys_user"]
                maquina.nome = fields["nome"]
                maquina.id_tema = fields["id_tema"]
                maquina.descricao = fields["descricao"]
                maquina.preco = fields["preco"]
                maquina.ativa = fields["ativa"]
                maquina.free = fields["free"]
                db.session.commit()
                return "OK"
            else:
                return "Tema não encontrado!",400
        else:
            return "Locador não encontrado!",400
    else:
        return "Maquina não existente!",400


@app.route("/api/updateToken",methods=["POST"])
@login_required
@admin_required()
@fields_required({"id":int})
def updateToken(fields):
    maquina = Maquinas.query.get(fields["id"])
    if maquina:
        token = jwt.encode({'id_maquina':maquina.id,'control_str':token_urlsafe(8)},app.config['SECRET_KEY']).decode('UTF-8')
        hashed_tkn = GPH(token,method="sha256")
        maquina.token = hashed_tkn
        db.session.commit()
        return token
    else:
        return "Maquina não existente!",400

@app.route("/api/logMaquinas",methods=["GET"])
@login_required
def Logmaquinas():
    if current_user.is_admin: #se for admin mostra todos os Logs se nao, mostra apenas os logs do usuario
        logs = LogMaquinas.query.all()
    else:
        logs = LogMaquinas.query.filter(LogMaquinas.cli_user.has(id_sys_user=current_user.id)).all()
        # logs = LogMaquinas.query.filter(LogMaquinas.sysUser.has(id=current_user.id)).all()

    formatado = mallowList(LogMSchema,logs)
    return jsonify(formatado)



@app.route("/api/maquinas/status",methods=["POST"])
@login_required
@fields_required({"id":int,"status":bool})
def change_status(fields):

    maquina = Maquinas.query.get(fields["id"])
    if maquina:
        if maquina.sysUser.id == current_user.id:
            maquina.ativa = fields["status"]
            db.session.commit()
            return "OK"
        else:
            return "Esta máquina não pertence a este usuário!",400
    else:
        return "Máquina não encontrada!",400

    formatado = mallowList(LogMSchema,logs)
    return jsonify(formatado)


