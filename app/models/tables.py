from app import db
from sqlalchemy import Float,Column,Integer,String,ForeignKey,DateTime,Time,Boolean
from datetime import datetime,date,timedelta
from app.models.uteis2 import strfdelta

class Temas(db.Model):
    __tablename__ = "temas"

    id      = Column(Integer(),primary_key=True)
    tema    = Column(String(),unique=True)
  
    def __init__(self,tema):
        self.tema = tema

    def __repr__(self):
        return "<Tema %r>" % self.tema

class Maquinas(db.Model):
    __tablename__ = "maquinas"

    id          = Column(Integer(),primary_key=True)
    id_tema     = Column(Integer(),ForeignKey('temas.id'),nullable=False)
    id_sys_user = Column(Integer(),ForeignKey('sys_usuarios.id'),nullable=False)
    nome        = Column(String(),unique=True,nullable=False)
    descricao   = Column(String())
    preco       = Column(Float(),nullable=False)
    ativa       = Column(Boolean(),nullable=False)
    free        = Column(Boolean(),nullable=False)
    token       = Column(String(),nullable=False)
    Tema        = db.relationship("Temas",foreign_keys=id_tema)
    sysUser     = db.relationship("SysUser",foreign_keys=id_sys_user)

    def __init__(self,id_tema,id_sys_user,nome,descricao,preco,ativa,free=False,token="*"):
        self.id_tema        =  id_tema
        self.id_sys_user    = id_sys_user
        self.nome           =  nome
        self.descricao      =  descricao
        self.preco          =  preco
        self.ativa          =  ativa
        self.free           =  free
        self.token          =  token

    def __repr__(self):
        return "<Maq %r>" % self.nome

    def save(self):
        db.session.add(self)
        db.session.commit()

class Documentos(db.Model):
    __tablename__ = "documentos"

    id      = Column(Integer(),primary_key=True)
    tipo    = Column(String(),nullable=False)
   
    def __init__(self,tipo):
        self.tipo =  tipo

    def __repr__(self):
        return "<Doc %r>" % self.tipo

class Pessoa(db.Model):
    __tablename__ = "pessoas"

    id                  = Column(Integer(),primary_key=True)
    nome                = Column(String(),nullable=False)
    telefone            = Column(String(),nullable=False)
    email               = Column(String(),nullable=False)
    id_doc_type         = Column(Integer,ForeignKey('documentos.id'))
    numero_documento    = Column(String(),nullable=False,unique=True)
    documento           = db.relationship("Documentos",foreign_keys=id_doc_type)

    def __init__(self,nome,telefone,email,id_doc_type,numero_documento):
        self.nome               = nome
        self.telefone           = telefone
        self.email              = email
        self.id_doc_type        = id_doc_type
        self.numero_documento   = numero_documento

    def __repr__(self):
        return "<Pessoa %r>" % self.nome

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.rollback()
        db.session.delete(self)
        db.session.commit()

class CliUsers(db.Model):
    __tablename__ = "cli_usuarios"

    id                  = Column(Integer(),primary_key=True)
    id_sys_user         = Column(Integer(),ForeignKey('sys_usuarios.id'),nullable=False)
    id_pessoa           = Column(Integer(),ForeignKey('pessoas.id'),unique=True)
    numero_cartao       = Column(String(),unique=True,nullable=False)
    credito             = Column(Float(),nullable=False)
    freeplay_data_exp   = Column(DateTime())
    ativo               = Column(Boolean(),nullable=False)

    pessoa              = db.relationship("Pessoa",foreign_keys=id_pessoa)
    sysUser             = db.relationship("SysUser",foreign_keys=id_sys_user)

    def __init__(self,id_sys_user,id_pessoa,numero_cartao,credito,freeplay_data_exp,ativo):
        self.id_pessoa          = id_pessoa 
        self.id_sys_user        = id_sys_user
        self.numero_cartao      = numero_cartao 
        self.credito            = credito 
        self.freeplay_data_exp  = freeplay_data_exp 
        self.ativo              = ativo 

    def __repr__(self):
        return "<CliUser %r>" % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    
    def free_time(self,formated=False):
        tm = timedelta() if not self.freeplay_data_exp else self.freeplay_data_exp - datetime.now()
        tm = timedelta() if tm.total_seconds() <= 0 else tm
        return tm if not formated else strfdelta(tm,"{hours}:{minutes}")

    def has_free_time(self):
        return self.free_time().total_seconds() > 0

class LogMaquinas(db.Model):
    __tablename__ = "log_maquinas"

    id                  = Column(Integer(),primary_key=True)
    data                = Column(DateTime(),nullable = False)
    id_sys_user         = Column(Integer(),ForeignKey('sys_usuarios.id'))
    id_cli_user         = Column(Integer(),ForeignKey('cli_usuarios.id'))
    id_maquina          = Column(Integer(),ForeignKey('maquinas.id'))
    preco               = Column(Float(),nullable=False)

    sysUser             = db.relationship("SysUser",foreign_keys=id_sys_user)
    cli_user            = db.relationship("CliUsers",foreign_keys=id_cli_user)
    maquina             = db.relationship("Maquinas",foreign_keys=id_maquina)

    def __init__(self,data,id_sys_user,id_cli_user,id_maquina,preco):
        self.data           = data
        self.id_sys_user    = id_sys_user
        self.id_cli_user    = id_cli_user
        self.id_maquina     = id_maquina
        self.preco          = preco

    def __repr__(self):
        return "<LogM %r>" % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()

class SysUser(db.Model):
    __tablename__ = "sys_usuarios"

    id                  = Column(Integer,primary_key=True)
    id_pessoa           = Column(Integer,ForeignKey('pessoas.id'))
    local               = Column(String,nullable = False)
    endereco            = Column(String,nullable = False)
    username            = Column(String,nullable = False,unique=True)
    senha               = Column(String,nullable = False)
    is_admin            = Column(Boolean,nullable = False)
    ativo               = Column(Boolean,nullable = False)
    descricao           = Column(String)
    
    pessoa              = db.relationship("Pessoa",foreign_keys=id_pessoa)
    maquinas            = db.relationship("Maquinas", backref="sys_usuarios")

    def __init__(self,id_pessoa,local,endereco,username,senha,descricao,is_admin,ativo):
        self.id_pessoa       = id_pessoa     
        self.local           = local         
        self.endereco        = endereco      
        self.username        = username      
        self.senha           = senha         
        self.descricao       = descricao         
        self.is_admin        = is_admin      
        self.ativo           = ativo         

    def __repr__(self):
        return "<SysUser %r>" % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @property
    def is_authenticated(self):
        return True
    @property
    def is_active(self):
        return True
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)

class LogVendas(db.Model):
    __tablename__ = "log_vendas"

    id                  = Column(Integer,primary_key=True)
    data                = Column(DateTime,nullable = False)
    id_sys_user         = Column(Integer,ForeignKey('sys_usuarios.id'))
    id_cli_user         = Column(Integer,ForeignKey('cli_usuarios.id'))
    credito             = Column(Float,nullable=False)
    free_play_days      = Column(Integer)
    credito_pago        = Column(Boolean,nullable=False)

    sysUser             = db.relationship("SysUser",foreign_keys=id_sys_user)
    cli_user            = db.relationship("CliUsers",foreign_keys=id_cli_user)

    def __init__(self,data,id_sys_user,id_cli_user,credito,free_play_days,credito_pago):
        self.data           = data          
        self.id_sys_user    = id_sys_user   
        self.id_cli_user    = id_cli_user   
        self.credito        = credito       
        self.free_play_days = free_play_days
        self.credito_pago   = credito_pago  

    def __repr__(self):
        return "<LogV %r>" % self.id

    def save(self):
        db.session.add(self)
        db.session.commit()




