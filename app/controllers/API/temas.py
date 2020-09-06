from app import app,db
from flask import jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import Temas
from app.models.marshmallow import TemaSchema
import json


@app.route("/api/temas",methods=["GET"])
@login_required
@admin_required()
def temas_get():
    temas = Temas.query.all()
    formatado = mallowList(TemaSchema,temas)
    return jsonify(formatado)



@app.route("/api/temas",methods=["POST"])
@login_required
@admin_required()
@fields_required(["tema"])
def temas_post(fields):
    temas = Temas.query.filter_by(tema=fields["tema"]).all()
    if not temas:
        tema = Temas(fields["tema"])
        db.session.add(tema)
        db.session.commit()
        return json.loads(TemaSchema().dumps(tema))
    else:
        return "Tema ja existente!",400