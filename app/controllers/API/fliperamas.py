
from app import app,db
from flask_login import current_user,login_required
from datetime import datetime as dt
from app.models.uteis import *
from app.models.tables import LogMaquinas


@app.route("/api/validate",methods=["GET"])
@token_required()
@fields_required(["tag"])
@valida_transacao()
def validate(fields,maquina,cli_user):

    cli_user.credito -= maquina.preco
    
    id_sys_user = maquina.sysUser.id

    log = LogMaquinas(dt.now(),id_sys_user,cli_user.id,maquina.id,maquina.preco)
    log.save()

    return "OK"