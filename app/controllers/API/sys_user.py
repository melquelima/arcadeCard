from app import app,db
from flask import jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import SysUser,Pessoa
from app.models.marshmallow import SysUserSchema,SysUserListMSchema
from sqlalchemy import or_
import json


@app.route("/api/locador",methods=["GET"])
@login_required
def locador_get():
    if current_user.is_admin:
        sysusers = SysUser.query.all()
    else:
        sysusers = [current_user]
        
    formatado = mallowList(SysUserSchema,sysusers)
    return jsonify(formatado)

#com lista de maquinas
@app.route("/api/locador",methods=["FILTER"])
@app.route("/api/locador/<int:id_locador>",methods=["FILTER"])
@login_required
@admin_required()
def locador_get2(id_locador = None):
    if id_locador != None:
        sysusers = SysUser.query.filter_by(id = id_locador).all()
    else:
        sysusers = SysUser.query.all()
        
    formatado = mallowList(SysUserListMSchema,sysusers)
    return jsonify(formatado)


@app.route("/api/locador",methods=["POST"])
@login_required
@admin_required()
@fields_required({"nome":str,"telefone":str,"email":str,"id_doc_type":int,"numero_documento":str,"local":str,"endereco":str,"descricao":str,"user_name":str,"senha":str,"ativo":bool})
def locador_post(fields):
    p = Pessoa.query.filter(or_(Pessoa.nome==fields["nome"],Pessoa.numero_documento == fields["numero_documento"])).first()
    if not p:
        sysuser = SysUser.query.filter_by(username = fields["user_name"]).first()
        if not sysuser:
            p = Pessoa(fields["nome"],fields["telefone"],fields["email"],fields["id_doc_type"],fields["numero_documento"])
            p.save()
            l = SysUser(p.id,fields["local"],fields["endereco"],fields["user_name"],fields["senha"],fields["descricao"],False,fields["ativo"])
            l.save()
            return json.loads(SysUserSchema().dumps(l))
        else:
            return f"Já existe um usuario com o username '{fields['user_name']}'",400
    else:
        if p.nome == fields["nome"]:
            return f"Já existe um usuario com o nome de {fields['nome']}",400
        else:
            return f"Já existe um usuario com o documento {fields['numero_documento']}",400

@app.route("/api/locador",methods=["PUT"])
@login_required
@admin_required()
@fields_required({"id":int,"nome":str,"telefone":str,"email":str,"id_doc_type":int,"numero_documento":str,"local":str,"endereco":str,"descricao":str,"user_name":str,"senha":str,"ativo":bool})
def locador_put(fields):
    sysuser = SysUser.query.get(fields["id"])
    if sysuser:
        print(fields["id_doc_type"])
        sysuser.pessoa.nome             = fields["nome"]
        sysuser.pessoa.telefone         = fields["telefone"]
        sysuser.pessoa.email            = fields["email"]
        sysuser.pessoa.id_doc_type      = fields["id_doc_type"]
        sysuser.pessoa.numero_documento = fields["numero_documento"]
        sysuser.local                   = fields["local"]
        sysuser.endereco                = fields["endereco"]
        sysuser.username                = fields["user_name"]
        sysuser.senha                   = fields["senha"]
        sysuser.descricao               = fields["descricao"]
        sysuser.ativo                   = fields["ativo"]
        db.session.commit()

        return json.loads(SysUserSchema().dumps(sysuser))
    else:
        return f"Usuário não encontrado!",400