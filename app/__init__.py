from flask import Flask
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
import os

app = Flask(__name__)
app.config.from_object('config')
cors = CORS(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
lm.needs_refresh_message = (u"Session timedout, please re-login")

from app.models.filters import *

from app.controllers.routes import default,maquinas,locadores,usuarios,login
from app.controllers.API.temas import *
from app.controllers.API.maquinas import *
from app.controllers.API.documentos import *
from app.controllers.API.sys_user import *
from app.controllers.API.fliperamas import *
from app.controllers.API.cli_users import *


