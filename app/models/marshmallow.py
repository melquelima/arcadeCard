
from app import ma
from marshmallow import Schema, fields
from datetime import datetime as dt, timedelta as td


class DocumentoSchema(ma.Schema):
    id                  = fields.Integer()
    tipo           = fields.String()

class PessoaSchema(ma.Schema):
    id                  = fields.Integer()
    nome                = fields.String()      
    telefone            = fields.String()    
    email               = fields.String() 
    numero_documento     = fields.String()
    documento           = fields.Nested(DocumentoSchema)


class SysUserSchema(ma.Schema):
    id                  = fields.Integer()    
    local               = fields.String()    
    endereco            = fields.String() 
    username            = fields.String()
    senha               = fields.String()
    descricao           = fields.String()
    is_admin            = fields.Boolean()
    ativo               = fields.Boolean()
    pessoa              = fields.Nested(PessoaSchema)

class CliUserSchema(ma.Schema):
    id                  = fields.Integer()
    numero_cartao       = fields.String()      
    credito             = fields.Float()    
    ativo               = fields.Boolean()    
    freeplay_data_exp   = fields.DateTime()
    free_time           = fields.Function(lambda obj:strfdelta(obj.free_time,"{hours}:{minutes}"))
    pessoa              = fields.Nested(PessoaSchema)
    sysUser             = fields.Nested(SysUserSchema)


class TemaSchema(ma.Schema):
    id          = fields.Integer()
    tema        = fields.String()

class MaquinasSchema(ma.Schema):
    id          = fields.Integer()
    nome        = fields.String()      
    descricao   = fields.String()      
    preco       = fields.Float()    
    ativa       = fields.Boolean() 
    free        = fields.Boolean() 
    Tema        = fields.Nested(TemaSchema)
    sysUser     = fields.Nested(SysUserSchema)

class LogMSchema(ma.Schema):
    id          = fields.Integer()
    data        = fields.DateTime(format='%d/%m/%y %H:%M')       
    preco       = fields.Float()
    cli_user    = fields.Nested(CliUserSchema)
    maquina     = fields.Nested(MaquinasSchema)


class SysUserListMSchema(ma.Schema):
    id                  = fields.Integer()    
    local               = fields.String()    
    endereco            = fields.String() 
    username            = fields.String()
    senha               = fields.String()
    descricao           = fields.String()
    is_admin            = fields.Boolean()
    ativo               = fields.Boolean()
    pessoa              = fields.Nested(PessoaSchema)
    maquinas            = fields.List(fields.Nested(MaquinasSchema()))




def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)