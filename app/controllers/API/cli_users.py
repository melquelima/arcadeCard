from app import app,db
from flask import jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import CliUsers,Pessoa,LogVendas
from app.models.marshmallow import CliUserSchema
from sqlalchemy import or_
from datetime import datetime as dt
import json


@app.route("/api/usuarios",methods=["GET"])
@login_required
def usuarios_get():
    if current_user.is_admin:
        users = CliUsers.query.all()
    else:
        users = CliUsers.query.filter_by(id_sys_user = current_user.id).all()
    
    formated = mallowList(CliUserSchema,users)
    return jsonify(formated)


@app.route("/api/usuarios",methods=["POST"])
@login_required
@fields_required({"nome":str,"telefone":str,"email":str,"id_doc_type":int,"numero_documento":str,"numero_cartao":str,"freeplay_data_exp":str,"ativo":bool})
def usuarios_post(fields):
    try:
        #valid = validate(fields["freeplay_data_exp"],"%d/%m/%y %H:%M")
        #if (not valid[0]) and fields["freeplay_data_exp"] != "": return "o campo freeplay_data_exp contem um formato inválido",400

        #fields["freeplay_data_exp"] = valid[1] if valid[0] else None 

        p = Pessoa.query.filter(or_(Pessoa.nome==fields["nome"],Pessoa.numero_documento == fields["numero_documento"])).first()
        if not p:
            cliu_ser = CliUsers.query.filter_by(numero_cartao = fields["numero_cartao"]).first()
            if not cliu_ser:
                p = Pessoa(fields["nome"],fields["telefone"],fields["email"],fields["id_doc_type"],fields["numero_documento"])
                p.save()
                c = CliUsers(current_user.id,p.id,fields["numero_cartao"],0,None,fields["ativo"])
                c.save()
                return json.loads(CliUserSchema().dumps(c))
            else:
                return f"Já existe um usuario com este cartao '{fields['numero_cartao']}'",400
        else:
            if p.nome == fields["nome"]:
                return f"Já existe um usuario com o nome de {fields['nome']}",400
            else:
                return f"Já existe um usuario com o documento {fields['numero_documento']}",400
    except:
        if c: c.delete()
        if p: p.delete()
        raise


@app.route("/api/usuarios",methods=["PUT"])
@login_required
@fields_required({"nome":str,"telefone":str,"email":str,"id_doc_type":int,"numero_documento":str,"numero_cartao":str,"ativo":bool})
def usuarios_put(fields):
 
    #valid = validate(fields["freeplay_data_exp"],"%d/%m/%y %H:%M")
    #if (not valid[0]) and fields["freeplay_data_exp"] != "": return "o campo freeplay_data_exp contem um formato inválido",400

    #fields["freeplay_data_exp"] = valid[1] if valid[0] else None 

    cliu_ser = CliUsers.query.filter(CliUsers.pessoa.has(numero_documento = fields["numero_documento"])).first()
    if cliu_ser:
        cliu_ser.pessoa.nome                      = fields["nome"]
        cliu_ser.pessoa.telefone                  = fields["telefone"]
        cliu_ser.pessoa.email                     = fields["email"]
        cliu_ser.pessoa.id_doc_type               = fields["id_doc_type"]
        cliu_ser.pessoa.numero_documento          = fields["numero_documento"]
        cliu_ser.numero_cartao                    = fields["numero_cartao"]
        cliu_ser.freeplay_data_exp                = None#fields["freeplay_data_exp"]
        cliu_ser.ativo                            = fields["ativo"]

        db.session.commit()
        return json.loads(CliUserSchema().dumps(cliu_ser))
    else:
        return "Usuário não encontrado!",400

@app.route("/api/usuarios",methods=["CREDIT"])
@login_required
@fields_required({"id_user":int,"credito":float,"free_play_days":int})
def usuarios_credit(fields):
    #valid = validate(fields["freeplay_data_exp"],"%d/%m/%y %H:%M")
    #if (not valid[0]) and fields["freeplay_data_exp"] != "": return "o campo freeplay_data_exp contem um formato inválido",400
    #fields["freeplay_data_exp"] = valid[1] if valid[0] else None
    if fields["credito"] <= 0: return "valor inválido!",400

    cli_user = CliUsers.query.get(fields["id_user"])
    if cli_user:
        cli_user.credito += fields["credito"]
        logvendas = LogVendas(dt.now(),current_user.id,cli_user.id,fields["credito"], fields["free_play_days"],False)
        logvendas.save()
        return "Creditos inseridos com sucesso!"
    else:
        return f"Cliente não encontrado!",400




