from app import app,db
from flask import jsonify
from flask_login import current_user,login_required
from app.models.uteis import *
from app.models.tables import Documentos
from app.models.marshmallow import DocumentoSchema

@app.route("/api/documentos",methods=["GET"])
@login_required
def documentos_get():
    docs = Documentos.query.all()
    formatado = mallowList(DocumentoSchema,docs)
    return jsonify(formatado)