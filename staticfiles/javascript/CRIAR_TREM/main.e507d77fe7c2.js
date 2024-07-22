




function TOOGLE_COMENTARIO(){

    var COMENTARIOS = document.querySelectorAll('.CONTEUDO_COMENTARIO');
    var ICONES = document.querySelectorAll('.ICONE');
    var COLUNA_BOTOES = document.getElementById("COLUNA_BOTOES")  

    ICONES.forEach(function(ICONE) {
        ICONE.classList.toggle('DESATIVADO');
    });

    
    COMENTARIOS.forEach(function(COMENTARIOS) {
        COMENTARIOS.classList.toggle('DESATIVADO');
    });

    COLUNA_BOTOES.classList.toggle('DESATIVADO');

}





