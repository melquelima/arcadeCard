function editarMaquina() {
    function link (scope, element, attrs) {
        scope.t = "hehe"
    }

    return {
        restrict: 'E',
        link: link,
        templateUrl: 'static/angularJs/diretivas/editarMaquina/editarMaquina.html'
    };
}