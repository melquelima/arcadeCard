$(document).ready(function(){
    $('#date').mask('00/00/0000');
    
});

var app = angular.module('myApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('[{');
    $interpolateProvider.endSymbol('}]');
});

app.factory('svc', function () {
    var msg="original...";
    return {
        setMessage: function(x) {
            alert(x)
        },
        getMessage: function() {
            return msg;
        }
    };
});

app.service('api_service', ['$q','$http',function($q,$http){  

    Temas = function(method,data){
        parameters = {url: "/api/temas",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Maquinas = function(method,data){
        parameters = {url: "/api/maquinas",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Locadores = function(method,data){
        parameters = {url: "/api/locador",method: method,data:data}
        return $http(parameters).then(success,error)
    };
    Usuarios = function(method,data){
        parameters = {url: "/api/usuarios",method: method,data:data}
        return $http(parameters).then(success,error)
    };

    this.getTemas = () => Temas("GET")
    this.postTemas = data => Temas("POST",data)
    this.getMaquina = () => Maquinas("GET")
    this.putMaquina = data => Maquinas("PUT",data)
    this.postMaquina = data => Maquinas("POST",data)
    this.getLocadores = () => Locadores("GET")
    this.postLocadores = data => Locadores("POST",data)
    this.putLocadores = data => Locadores("PUT",data)
    this.getLocadores2 = () => Locadores("FILTER")
    this.getUsuarios = () => Usuarios("GET")
    this.postUsuarios = data => Usuarios("POST",data)
    this.putUsuarios = data => Usuarios("PUT",data)
    this.creditUsuarios = data => Usuarios("CREDIT",data)
    
    this.gerarToken = function(data){
        parameters = {url: "/api/updateToken",method: "POST",data:data}
        return $http(parameters).then(success,error)
    };  

    this.salvarStatus = function(data){
        parameters = {url: "/api/maquinas/status",method: "POST",data:data}
        return $http(parameters).then(success,error)
    }
    this.getLogs = function(){
        parameters = {url: "/api/logMaquinas",method: "GET"}
        return $http(parameters).then(success,error)
    }
    this.getDocs = function(){
        parameters = {url: "/api/documentos",method: "GET"}
        return $http(parameters).then(success,error)
    }
    this.getLogsFiltered = function(data){
        parameters = {url: "/api/logMaquinasFilter",method: "POST",data:data}
        return $http(parameters).then(success,error)
    }
    this.getMaquinaId = function(data){
        data = data==null?"": "/" + data
        parameters = {url: "/api/maquinas"+data,method: "GET"}
        return $http(parameters).then(success,error)
    }

    

    
    

    success = (response)=> response.data
    error = (response)=> {toastr.error(response.data);return $q.reject(response.data)}

}]);

app.service('tema_svc', ['api_service',function(api_service){  

    this.cadastraTema = novoTema=>{
        
        if(novoTema == undefined){
            return toastr.warning('o campo nao pode estar vazio');
        }
        
        if(novoTema.trim() == ''){
            return toastr.warning('o campo nao pode estar vazio');
        }

        data = {tema:novoTema}
        return api_service.postTemas(data)
    }

}]);

app.service('locador_svc', ['api_service',function(api_service){  

    this.validaLocador = locador => {
        obj = JSON.parse(JSON.stringify(locador));
        
        notEmpty = ["nome","telefone","numero_documento","email","local","endereco","user_name","senha","senha2"]
        for(var i=0;i<notEmpty.length;i++){
            if(obj[notEmpty[i]] == null || obj[notEmpty[i]].trim() == ''){
                toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
                return false
            }
        }
        if(obj.id_doc_type == null){
            toastr.warning('o campo tipo_do_documento não pode estar vazio');
            return false
        }
        obj.id_doc_type = obj.id_doc_type.id

        if(obj.senha.trim() != obj.senha2.trim()){
            toastr.warning('as senhas não conferem');
            return false
        }
        return true
    }

    this.cadastraLocador = locador => {
        if (this.validaLocador(locador)){
            return api_service.postLocadores(obj)
        }
    }
    this.salvaLocador = locador => {
        if (this.validaLocador(locador)){
            return api_service.putLocadores(obj)
        }
    }

}]);


INCLUDES = ['$scope','$filter','$http','$sce','api_service']
TESTE = null

app.controller('TodasCtrl', INCLUDES.concat(['tema_svc',function (sc, $filter,$http,$sce,api_service,tema_svc){
    sc.idLista = FROMBACKEND.id
    sc.lista = []//FROMBACKEND.lista
    sc.Selected = {ativa:false}
    sc.temas = []
    sc.locadores = []
    sc.loadingSalvar = false
    sc.loadingTema = false
    sc.loadingToken = false
    

    api_service.getMaquinaId(sc.idLista).then((r)=>sc.lista = r)

    sc.gerarToken = ()=>{
        sc.loadingToken = true

        data = {id:sc.Selected.id}
        api_service.gerarToken(data).then((r)=>{
            sc.loadingToken = false
            sc.token = r
        }).catch(()=>sc.loadingToken = false)
    }

    sc.cadastraTema = (novoTema)=>{
        sc.loadingTema = true
        tema_svc.cadastraTema(novoTema).then((r)=>{
            sc.loadingTema = false
            sc.temas.push(r)
            toastr.success('Tema Cadastrado com sucesso!');
            sc.NovoTemaValue = ""
            $("#modal-novoTema").modal('hide')
        }).catch(()=>sc.loadingTema = false)
    }

    sc.select = (item)=>{
        print(item)
        sc.Selected = item
        sc.Selected.id_tema = sc.temas.filter((i)=>{if(i.id == item.Tema.id)return i})[0]
        sc.Selected.id_sys_user = sc.locadores.filter((i)=>{if(i.id == item.sysUser.id)return i})[0]
        $('#toggle-demo').bootstrapToggle(item.ativa?'on':'off')
        $('#toggle-demo2').bootstrapToggle(item.free?'on':'off')
        sc.token = ""
        $("#modal-editar").modal("show")

    }

    sc.editarStatus = (item)=>{
        sc.Selected = item
        $('#toggle-demo2').bootstrapToggle(item.ativa?'on':'off')
        $("#modal-status").modal("show")
    }

    sc.salvarStatus = ()=>{
        sc.loadingSalvar = true
        obj = {id:sc.Selected.id,status:sc.Selected.ativa}
        api_service.salvarStatus(obj).then((r)=>{
            sc.loadingSalvar = false
            toastr.success('Dados salvos com sucesso!')
        }).catch(()=>sc.loadingSalvar = false)
    }

    sc.AlterarMaquina = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Selected));

        if(obj.nome.trim() == ''){
            toastr.warning('o campo "Nome" não pode estar vazio');
            return
        }
        if(obj.id_tema == null){
            toastr.warning('o campo "Tema" não pode estar vazio');
            return
        }
        if(obj.preco == null | obj.preco == ""){
            toastr.warning('o campo "Valor" não pode estar vazio');
            return
        }
        if(obj.id_sys_user == null){
            toastr.warning('o campo "Local" não pode estar vazio');
            return
        }

        obj.id_sys_user = obj.id_sys_user.id
        obj.id_tema = obj.id_tema.id
        console.log(typeof obj.preco)
        obj.preco = parseFloat(obj.preco);

        sc.loadingSalvar = true
        api_service.putMaquina(obj).then((r)=>{
            sc.loadingSalvar = false
            toastr.success('Dados salvos com sucesso!')
        }).catch(()=>sc.loadingSalvar = false)
    }

    sc.openModal = ()=>$('#modal-novoTema').modal('show')

    

    if (FROMBACKEND.admin){
        api_service.getTemas().then((r)=>sc.temas = r)
        api_service.getLocadores().then((r)=>sc.locadores = r)
    }

}]));

app.controller('NovaCtrl', INCLUDES.concat(['tema_svc',function (sc, $filter,$http,$sce,api_service,tema_svc){
    sc.temas = []
    sc.novaMaquina = {nome:"",id_tema:null,id_sys_user:null,preco:null,descricao:"",ativa:false,free:false}
    sc.locadores = []
    sc.loading = false
    sc.loadingTema = false

    api_service.getTemas().then((r)=>sc.temas = r)
    api_service.getLocadores().then((r)=>{
        sc.locadores = r
    })


    sc.cadastraMaquina = (novaMaquina)=>{
        obj = JSON.parse(JSON.stringify(novaMaquina));

        if(obj.nome.trim() == ''){
            toastr.warning('o campo "Nome" não pode estar vazio');
            return
        }
        if(obj.id_tema == null){
            toastr.warning('o campo "Tema" não pode estar vazio');
            return
        }
        if(obj.preco == null){
            toastr.warning('o campo "Valor" não pode estar vazio');
            return
        }
        if(obj.id_sys_user == null){
            toastr.warning('o campo "Local" não pode estar vazio');
            return
        }

        obj.id_sys_user = obj.id_sys_user.id
        obj.id_tema = obj.id_tema.id
        console.log(typeof obj.preco)
        obj.preco = parseFloat(obj.preco);

        sc.loading = true
        api_service.postMaquina(obj).then((r)=>{
            sc.loading = false
            toastr.success('Maquina Cadastrado com sucesso!');
            sc.novaMaquina = {nome:"",id_tema:null,preco:null,descricao:null,ativa:false,free:false}
        }).catch(()=>sc.loading = false)
    }

    sc.cadastraTema = (novoTema)=>{
        sc.loadingTema = true
        tema_svc.cadastraTema(novoTema).then((r)=>{
            sc.loadingTema = false
            sc.temas.push(r)
            toastr.success('Tema Cadastrado com sucesso!');
            sc.NovoTemaValue = ""
            $("#modal-novoTema").modal('hide')
        }).catch(()=>sc.loadingTema = false)
    }

}]));

app.controller('LogsCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.logs = []
    sc.locadores = []
    sc.selectedLocador = null
    sc.loading = false
    sc.selectedData = null
    sc.selectedData = getDate()

    //api_service.getLogs().then((r)=>sc.logs = r)
    api_service.getLocadores().then((r)=>sc.locadores = r)

    sc.filterLogs = ()=>{
        data = {
            data:sc.selectedData == null?"": sc.selectedData,
            id_locador:sc.selectedLocador ==null?0:sc.selectedLocador.id,
            documento_cli:sc.selectedDocumento ==null?"":sc.selectedDocumento,
        }
        sc.loading = true
        api_service.getLogsFiltered(data).then((r)=>{
            sc.logs = r
            sc.loading = false
        }).catch(()=>sc.loading = false)
        
        
    }


}]));

app.controller('NovoLocadorCtrl', INCLUDES.concat(['locador_svc',function (sc, $filter,$http,$sce,api_service,locador_svc){
    sc.documentos = []
    sc.locador = {nome:null,telefone:null,email:null,id_doc_type:null,numero_documento:null, local:null,endereco:null,descricao:null,user_name:null,senha:null,ativo:false}
    

    api_service.getDocs().then((r)=>sc.documentos = r)

    sc.cadastraLocador = ()=>{
        locador_svc.cadastraLocador(sc.locador).then((r)=>{
            toastr.success('Locador cadastrado com sucesso!');
            sc.locador = {nome:null,telefone:null,email:null,id_doc_type:null,numero_documento:null, local:null,endereco:null,descricao:null,user_name:null,senha:null,ativo:false}
        })
    }

}]));

app.controller('LocadoresCtrl', INCLUDES.concat(['locador_svc',function (sc, $filter,$http,$sce,api_service,locador_svc){
    sc.documentos = []
    sc.lista = FROMBACKEND.lista
    sc.Selected = {}
    sc.temas = []
    sc.locadores = []

    sc.select = (item)=>{
        sc.Selected = item
        sc.Selected.senha2 =  sc.Selected.senha
        sc.Selected.pessoa.documento = sc.documentos.filter((i)=>{if(i.id == item.pessoa.documento.id)return i})[0]
        // sc.Selected.id_sys_user = sc.locadores.filter((i)=>{if(i.id == item.sysUser.id)return i})[0]
        $('#toggle-demo').bootstrapToggle(item.ativo?'on':'off')
        // sc.token = ""
        $("#modal-editar").modal("show")
        print(item)
    }

    sc.salvaLocador = ()=>{
        novo = {
            id:sc.Selected.id,
            nome:sc.Selected.pessoa.nome,
            telefone:sc.Selected.pessoa.telefone,
            numero_documento:sc.Selected.pessoa.numero_documento,
            email:sc.Selected.pessoa.email,
            local:sc.Selected.local,
            endereco:sc.Selected.endereco,
            user_name:sc.Selected.username,
            senha:sc.Selected.senha,
            senha2:sc.Selected.senha2,
            id_doc_type:sc.Selected.pessoa.documento,
            ativo:sc.Selected.ativo,
            descricao:sc.Selected.descricao
        }
        console.log(novo)
        locador_svc.salvaLocador(novo).then((r)=>{
            toastr.success('Locador alterado com sucesso!');
        })
    }

    sc.openModal = ()=>$('#modal-novoTema').modal('show')

    api_service.getLocadores2().then((r)=>sc.locadores = r)
    api_service.getDocs().then((r)=>sc.documentos = r)

}]));

app.controller('UsuariosCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.lista = []
    sc.Selected = {}
    sc.usuarios = []
    sc.documentos = []

    api_service.getDocs().then((r)=>sc.documentos = r)
    api_service.getUsuarios().then((r)=>sc.usuarios = r)

    sc.select = (item)=>{
        sc.Selected = item

        if(item.pessoa.documento)
        sc.Selected.pessoa.documento = sc.documentos.filter((i)=>{if(i.id == item.pessoa.documento.id)return i})[0]
        
        $('#toggle-demo').bootstrapToggle(item.ativo?'on':'off')
        
        $("#modal-editar").modal("show")

    }


    sc.salvaUsuario = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Selected));
        
        notEmpty = ["pessoa.nome","pessoa.telefone","pessoa.numero_documento","pessoa.email","numero_cartao"]
        for(var i=0;i<notEmpty.length;i++){
            ob = eval("obj." + notEmpty[i])
            if(ob == null || ob.trim() == ''){
                return toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
            }
        }
        
        if(obj.pessoa.documento == null){
            return toastr.warning('o campo tipo_do_documento não pode estar vazio');
        }

        obj2 = {
            nome:obj.pessoa.nome,
            telefone:obj.pessoa.telefone,
            email:obj.pessoa.email,
            numero_cartao:obj.numero_cartao,
            id_doc_type:obj.pessoa.documento.id,
            numero_documento:obj.pessoa.numero_documento,
            freeplay_data_exp:obj.freeplay_data_exp == null?"":obj.freeplay_data_exp,
            ativo:obj.ativo
        }
        console.log(obj2)
        
        api_service.putUsuarios(obj2).then(r =>{
            toastr.success('Usuario atualizado com sucesso!');
        })
    }
    

}]));

app.controller('NovoUsuarioCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.documentos = []
    sc.Usuario = {nome:null,telefone:null,email:null,numero_cartao:null,id_doc_type:null,numero_documento:null,ativo:false}
    sc.loading = false

    api_service.getDocs().then((r)=>sc.documentos = r)

    sc.cadastraUsuario = ()=>{
        obj = JSON.parse(JSON.stringify(sc.Usuario));
        
        notEmpty = ["nome","telefone","numero_documento","email","numero_cartao"]
        for(var i=0;i<notEmpty.length;i++){
            if(obj[notEmpty[i]] == null || obj[notEmpty[i]].trim() == ''){
                return toastr.warning('o campo ' + notEmpty[i] +  ' não pode estar vazio');
            }
        }
        if(obj.id_doc_type == null){
            return toastr.warning('o campo tipo_do_documento não pode estar vazio');
        }
        obj.id_doc_type = obj.id_doc_type.id

        sc.loading = true
        api_service.postUsuarios(obj).then((r)=>{
            sc.loading = false
            sc.Usuario = {nome:null,telefone:null,email:null,numero_cartao:null,id_doc_type:null,numero_documento:null,ativo:false}
            toastr.success('Usuario cadastrado com sucesso!');
        }).catch(()=>sc.loading = false)
    }

}]));

app.controller('CarregarCtrl', INCLUDES.concat([function (sc, $filter,$http,$sce,api_service){
    sc.usuarios = []
    sc.valor = null
    sc.selected = null
    sc.loading = false
    sc.free = null

    api_service.getUsuarios().then((r)=>sc.usuarios = r)


    sc.carregar = ()=>{

        if(!(sc.valor || sc.free)){
            return toastr.error("valor inválido");
        }

        sc.valor += 0 //transforma null em 0
        sc.free += 0 //transforma null em 0
        console.log(sc.free)

        sc.loading = true //logo carregando e desabilita o botao
        data={id_user:sc.selected.id,credito:sc.valor,free_play_days:sc.free}
        api_service.creditUsuarios(data).then((r)=>{
            toastr.success(r);
            sc.selected.credito += sc.valor
            sc.loading = false //logo carregando e habilita o botao
            sc.selected = null
        }).catch(()=>sc.loading = false)
    }

    sc.$watch('documento', function(newValue, oldValue) {
        if(newValue!==oldValue) {
            sc.selected = sc.usuarios.filter(item=>{
                if(item.pessoa.numero_documento == newValue)return item
            })
            sc.selected = sc.selected.length?sc.selected[0]:null
        } 
     });
   

}]));



app.filter('filterJson', function () {

    var x = function (original, campo,valor) {
        lst = original.filter(function(a){if(eval("a." + campo) == valor){return eval("a." + campo)}})
        return lst;
    };
    return x;
});


app.directive("editarMaquina", function() {
    function link (scope, element, attrs) {
        scope.t = "hehe"
    }
    return {
        restrict: 'E',
        link: link,
        templateUrl: 'static/angularJs/diretivas/editarMaquina/editarMaquina.html'
    };
});



function removeItemArrray(arr, value) {
    var index = arr.indexOf(value);
    var arr2 = arr.slice()
    if (index > -1) {
    arr2.splice(index, 1);
    }
    return arr2;
    }
    
    function closeModal(){
    document.querySelector("#myTab>li>a").click()
    }

print = (x)=>console.log(x)


function getDate(){
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = dd + '/' + mm + '/' + yyyy;
    return today
}
