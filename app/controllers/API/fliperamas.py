
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
    preco = 0

    if not maquina.free: #quando a maquina não esta gratis
        if cli_user.has_free_time():
            msg = f"{cli_user.pessoa.nome}\nRestante:{cli_user.free_time(True)}"
        else:
            preco = maquina.preco
            cli_user.credito -= maquina.preco
            msg = f"{cli_user.pessoa.nome}\nSaldo: R${cli_user.credito:.2f}"
    else:
        preco = 0
        msg = f"{cli_user.pessoa.nome}\ngratis aproveite!"

    id_sys_user = maquina.sysUser.id

    log = LogMaquinas(dt.now(),id_sys_user,cli_user.id,maquina.id,preco)
    log.save()

    return msg
