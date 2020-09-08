from app import app
from flask import request
from random import randint
from flask import url_for


@app.context_processor
def tag_property():
    def func(tag,value): 
        v = value.replace(" ",' ') #nao é vazio e sim alt+255
        v = f'{tag}={v}'
        
        return v if value else ""
    return dict(tagProp=func)


@app.template_filter()
def url_to(text):
    return url_for('static', filename=text)


@app.context_processor
def random_Js():
    func = lambda jsFile: jsFile + "?u=" + str(randint(0, 100000))
    return dict(randomJs=func)


@app.context_processor
def utility_processor():
    activeMenu = lambda text: "active" if text in request.url_rule.rule else ""
    return dict(activeMenu=activeMenu)


@app.context_processor
def u_p():
    activeMenu2 = lambda lst: "menu-open" if request.url_rule.rule.replace("/","") in lst else ""
    return dict(activeMenu2=activeMenu2)


@app.context_processor
def utility_processor():
    activeMenu3 = lambda text: "active2" if text == request.url_rule.rule else ""
    return dict(activeMenu3=activeMenu3)