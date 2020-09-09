from flask import request,render_template,redirect,url_for
from functools import wraps
import json
from flask_login import current_user
from datetime import datetime as dt,date
from sqlalchemy import Date, cast

import jwt
from app import app,db
from app.models.tables import Maquinas,CliUsers
from werkzeug.security import check_password_hash as CPH

def fields_required(lista,methods="*",out="fields"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            xstr = lambda s: s or ""
            contentJson = "json" in xstr(request.headers.get("Content-Type"))

            if methods == "*" or request.method in methods:
                if request.method == "GET":
                    fields = request.args.to_dict()
                elif request.method in ["POST","PUT","DELETE","DEL","CREDIT"]:
                    data = request.get_json(force=True) or request.get_json() or request.form.to_dict()
                    fields =  request.json if contentJson else data
                
                lista2 = lista if isinstance(lista,list) else list(lista.keys())

                notfound = [x for x in lista2 if not x in fields]
                if notfound:
                    return "campos nao encontrados!:\n\t" + "\n\t".join(notfound),400
                
                if isinstance(lista,dict):
                    for k,v in lista.items():
                        
                        if v == float and isinstance(fields[k],int):
                            fields[k] = float(fields[k])

                        if not isinstance(fields[k],v):
                            tipo = str(v).split("'")[1]
                            return f"o campo '{k}' nao corresponde ao tipo ({tipo})",400


                kwargs[out] = fields
                result = function(*args, **kwargs)
                return result
            else:
                kwargs[out] = []
                return function(*args, **kwargs)

        return wrapper
    return decorator

def ponto_required():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.admin: #senão for admin...
                registro_ponto = Ponto.query.filter_by(id_ponto=current_user.id_ponto).filter(cast(Ponto.entrada,Date) == date.today()).first()
                if not registro_ponto:
                    registro = Mural.query.filter(cast(Mural.validade,Date) >= date.today()).all()
                    return render_template("baterPonto.html" ,user=current_user,mural=registro) #retorna a página de bater ponto se a entrada nao existir

            return function(*args, **kwargs) # vai pra proxima função

        return wrapper
    return decorator

def admin_required(methods="*"):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.is_admin:
                if methods == "*":
                    return "Usuario nao permitido para fazer este tipo de requisição",400
                else:
                    if request.method in methods:
                        return "Usuario nao permitido para fazer este tipo de requisição",400

            return function(*args, **kwargs) # vai pra proxima função
        return wrapper
    return decorator

def mallowList(schema,lista):#coverte dados da api para formtado jdson
    sc = schema()
    return [json.loads(sc.dumps(x)) for x in lista if sc.dumps(x) != '{}']

def validate(date_text,formt): #valida formato de data
    try:
        dt.strptime(date_text, formt)
        return True,dt.strftime(formt,date_text)
    except ValueError:
        return  False,""

def token_required(ignore=False): #deixa passar quando tiver * no banco
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            token = None
            fields = request.args.to_dict()

            if 'token' in fields:
                token = fields['token']
            
            if not token:
                return "Token is missing!",400
            try:
                data = jwt.decode(token,app.config['SECRET_KEY'])
                maquina = Maquinas.query.get(data['id_maquina'])
                if maquina.token == "*":
                    if not ignore: raise
                else:
                    if not CPH(maquina.token, token): raise

                kwargs["maquina"] = maquina
                return function(*args, **kwargs)
                #current_user = User.query.filter_by(publicId=data['publicId']).first()
            except:
                return "Token inválido!",400
           
        return wrapper
    return decorator

def admin_required_route():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            if not current_user.is_admin:
                return redirect(url_for("index"))

            return function(*args, **kwargs) # vai pra proxima função
        return wrapper
    return decorator




def valida_transacao():
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            fields = kwargs["fields"]
            mch = kwargs['maquina']
            if mch:
                if mch.ativa:
                    cliUsr = CliUsers.query.filter_by(numero_cartao = fields["tag"]).first()
                    if cliUsr:
                        if cliUsr.ativo:
                            if cliUsr.sysUser.ativo:
                                if cliUsr.credito >= mch.preco or cliUsr.has_free_time:
                                    kwargs["maquina"]   = mch 
                                    kwargs["cli_user"]  = cliUsr 
                                    return function(*args, **kwargs)
                                else:
                                    return "Saldo Insuficiente",400
                            else:
                                return "Locador inativo!",400
                        else:
                            return "Usuário inativo!",400
                    else:
                        return "Usuario nao encontrado!",400
                else:
                    return "Maquina inativa!",400
            else:
                return "Maquina nao encontrada!",400
        return wrapper
    return decorator
