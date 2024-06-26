var MOUSE_PRESSIONADO   = false
var MODO_EDICAO         = false
var EDITAR_SALDO_VIRADA = false
var EDITAR_PRODUTIVIADE = false
var NOVO_VALOR_SALDO = ""
var NOVO_VALOR          = ""
var PARAMETROS_EDITADOS = {
    "TERMINAL": "",
    "DATA_ARQ": "",
    "FERROVIA": "",
    "PRODUTO" : "",
    "CELULAS" : [],
    "VALOR"   : 0
}

let SENTIDO_SELECAO = ""

let NOVA_SELECAO = []

//#region PARA AO ATUALIZAR NAO VOLTAR AO INICIO DA PAGINA

window.addEventListener('load', function() {

    const conteudoNavegacao = document.getElementById('conteudo__navegacao');

    // Checking if there's a saved scroll position
    if (localStorage.getItem('scrollX') && localStorage.getItem('scrollY')) {

        conteudoNavegacao.scrollLeft = localStorage.getItem('scrollX');
        conteudoNavegacao.scrollTop = localStorage.getItem('scrollY');
        
    }

    // Save scroll position before page unloads
    window.addEventListener('beforeunload', function() {

        localStorage.setItem('scrollX', conteudoNavegacao.scrollLeft);
        localStorage.setItem('scrollY', conteudoNavegacao.scrollTop);

    });

});

//#endregion

//#region FUNCOES INTERNAS
function LIMPAR_SELECOES(){


    var CELULAS_SELECIONADAS    = document.querySelectorAll('.CELULA_SELECIONADA');
    var CELULAS_PRIMEIRA        = document.querySelectorAll('.PRIMEIRA');
    var CELULAS_ULTIMA          = document.querySelectorAll('.ULTIMA');
    
    CELULAS_PRIMEIRA.forEach(function(CELULA)       {CELULA.classList.remove('PRIMEIRA');});
    CELULAS_ULTIMA.forEach(function(CELULA)         {CELULA.classList.remove('ULTIMA');});
    CELULAS_SELECIONADAS.forEach(function(CELULA)   {CELULA.classList.remove('CELULA_SELECIONADA');});

    /*PARAMETROS_EDITADOS = {
        "TERMINAL": "",
        "DATA_ARQ": "",
        "CELULAS" : [],
        "VALOR"   : 0
    }*/


    let LINHA_PRODUTIVIDADE = document.getElementById('LINHA_EM_EDICAO')
    if (LINHA_PRODUTIVIDADE !== null) {LINHA_PRODUTIVIDADE.removeAttribute('id')}

    NOVO_VALOR         = ""
}

function DESENHAR_BORDA(CELULAS_INCICES){
    
    /*var CELULAS_SELECIONADAS = document.querySelectorAll('.CELULA_SELECIONADA');

    var CELULAS_PRIMEIRA = document.querySelectorAll('.PRIMEIRA');
    
    CELULAS_PRIMEIRA.forEach(function(CELULA) {
        CELULA.classList.remove('PRIMEIRA');
    });
    
    var CELULAS_ULTIMA   = document.querySelectorAll('.ULTIMA');

    CELULAS_ULTIMA.forEach(function(CELULA) {
        CELULA.classList.remove('ULTIMA');
    });

    CELULAS_SELECIONADAS.forEach(function(CELULA) {
        CELULA.classList.remove('CELULA_SELECIONADA');
    });*/

    CELULAS_INCICES.forEach(function(INDICE) {
        
        let CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ INDICE }"]` )

        if (CELULA) {
            CELULA.classList.remove('CELULA_SELECIONADA');
            CELULA.classList.remove('PRIMEIRA');
            CELULA.classList.remove('ULTIMA');
        } 

    });

    CELULAS_INCICES.forEach(function(INDICE) {
        let CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ INDICE }"]` )
        if (CELULA) {CELULA.classList.add('CELULA_SELECIONADA');} 
    });

    let INDICE_PRIMEIRA = Math.min(...CELULAS_INCICES);
    let PRIMEIRA_CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ INDICE_PRIMEIRA }"]` )


    let INDICE_ULTIMA = Math.max(...CELULAS_INCICES);
    let ULTIMA_CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ INDICE_ULTIMA }"]` )
    
    try{
        PRIMEIRA_CELULA.classList.add('PRIMEIRA');
        ULTIMA_CELULA.classList.add('ULTIMA');
    }
    catch{
        return
    }
}
//#endregion

let ctrlPressed = false

document.body.addEventListener('mousedown', async function(event) {
   
    MOUSE_PRESSIONADO = true
    let CELULA_SELECIONADA = event.target;

    let LINHA_PRODUTIVIDADE = CELULA_SELECIONADA.parentNode

    EDITAR_SALDO_VIRADA = false
    EDITAR_PRODUTIVIADE = false

    //CLICANDO NA CÉLULA DE PRODUTIVIDADE   
    if (CELULA_SELECIONADA.getAttribute('name') === "PRODUTIVIDADE" && ctrlPressed === false){

        LIMPAR_SELECOES()

        MODO_EDICAO = true
        let ID_TABELA = LINHA_PRODUTIVIDADE.parentNode.parentNode.id.split("_")
        let FERROVIA_PRODUTO = LINHA_PRODUTIVIDADE.getElementsByTagName("td")[1].id.split("_")

        PARAMETROS_EDITADOS["TERMINAL"] = ID_TABELA[0]
        PARAMETROS_EDITADOS["DATA_ARQ"] = ID_TABELA[1]

        PARAMETROS_EDITADOS["PRODUTO"]  = FERROVIA_PRODUTO[0]
        PARAMETROS_EDITADOS["FERROVIA"] = FERROVIA_PRODUTO[1]
        
        PARAMETROS_EDITADOS["CELULAS"] = []
        PARAMETROS_EDITADOS["CELULAS"][0] = CELULA_SELECIONADA.getAttribute('headers')

        NOVA_SELECAO = [CELULA_SELECIONADA.getAttribute('headers')]
        

        LINHA_PRODUTIVIDADE.id = 'LINHA_EM_EDICAO';  
        
        DESENHAR_BORDA(NOVA_SELECAO)

    }

    else if(CELULA_SELECIONADA.getAttribute('name') === "PRODUTIVIDADE" && ctrlPressed === true){

        let POSICAO_CELULA = CELULA_SELECIONADA.getAttribute('headers')
        PARAMETROS_EDITADOS["CELULAS"].push(POSICAO_CELULA);


        NOVA_SELECAO = [POSICAO_CELULA];
        DESENHAR_BORDA(NOVA_SELECAO)

    }

    else if(CELULA_SELECIONADA.getAttribute('name') === "SALDO_DE_VIRADA_D"){

        EDITAR_SALDO_VIRADA = true
        NOVO_VALOR_SALDO = ""
        
        LIMPAR_SELECOES()
        DESENHAR_BORDA(PARAMETROS_EDITADOS["CELULAS"])

        let ID_TABELA           = CELULA_SELECIONADA.parentNode.parentNode.parentNode.id.split("_")

        PARAMETROS_EDITADOS["TERMINAL"] = ID_TABELA[0]
        PARAMETROS_EDITADOS["DATA_ARQ"] = ID_TABELA[1]

        PARAMETROS_EDITADOS["PRODUTO"]  = CELULA_SELECIONADA.dataset.produto
        PARAMETROS_EDITADOS["FERROVIA"] = CELULA_SELECIONADA.dataset.ferrovia
        
        PARAMETROS_EDITADOS["CELULAS"][0] = ""

        CELULA_SELECIONADA.classList.add('CELULA_SELECIONADA');
        CELULA_SELECIONADA.classList.add('ULTIMA');
        CELULA_SELECIONADA.classList.add('PRIMEIRA');
  
    }

    else if(CELULA_SELECIONADA.getAttribute('name') === "EDITAR_CONSTANTE_PRODUTIVIDADE"){
        
        EDITAR_PRODUTIVIADE = true
        NOVO_VALOR_SALDO = ""

        LIMPAR_SELECOES()
        DESENHAR_BORDA(PARAMETROS_EDITADOS["CELULAS"])

        let ID_TABELA           = CELULA_SELECIONADA.parentNode.parentNode.parentNode.id.split("_")

        PARAMETROS_EDITADOS["TERMINAL"] = ID_TABELA[0]
        PARAMETROS_EDITADOS["DATA_ARQ"] = ID_TABELA[1]

        PARAMETROS_EDITADOS["PRODUTO"]  = CELULA_SELECIONADA.dataset.produto
        PARAMETROS_EDITADOS["FERROVIA"] = CELULA_SELECIONADA.dataset.ferrovia

        PARAMETROS_EDITADOS["CELULAS"][0] = ""

        CELULA_SELECIONADA.classList.add('CELULA_SELECIONADA');
        CELULA_SELECIONADA.classList.add('ULTIMA');
        CELULA_SELECIONADA.classList.add('PRIMEIRA');
        
    }

    else{ 

        LIMPAR_SELECOES(); 
        MODO_EDICAO = false; 
        DESENHAR_BORDA(PARAMETROS_EDITADOS["CELULAS"]) 

    }   //NÃO É CÉLULA DE PRODUTIVIDADE

})

document.body.addEventListener('mouseover', async function(event) {
    
    let CELULA_SELECIONADA  = event.target;
    let LINHA_PRODUTIVIDADE = CELULA_SELECIONADA.parentNode
    let ESTA_NA_MESMA_LINHA = document.getElementById('LINHA_EM_EDICAO') === LINHA_PRODUTIVIDADE 
        
    let CELULA_DE_PRODUTIVIDADE = CELULA_SELECIONADA.getAttribute('name') === "PRODUTIVIDADE"

    if(MOUSE_PRESSIONADO && MODO_EDICAO && ESTA_NA_MESMA_LINHA && CELULA_DE_PRODUTIVIDADE){
        
        let POSICAO_CELULA = CELULA_SELECIONADA.getAttribute('headers')

        //DEFININDO O SENTIDO DA SELEÇÃO [ESQUERDA OU DIREITA]
        if (PARAMETROS_EDITADOS["CELULAS"].length === 1){
            
            if (PARAMETROS_EDITADOS["CELULAS"][0] >  POSICAO_CELULA) {SENTIDO_SELECAO = "ESQUERDA";}
            else                                                     {SENTIDO_SELECAO = "DIREITA"; }
        }
        
        if (SENTIDO_SELECAO === `DIREITA`){

            if (POSICAO_CELULA == Math.max(...NOVA_SELECAO) + 1){

                PARAMETROS_EDITADOS["CELULAS"].push(POSICAO_CELULA);
                NOVA_SELECAO.push(POSICAO_CELULA)

                DESENHAR_BORDA(NOVA_SELECAO)
            }


            if (POSICAO_CELULA == Math.max(...NOVA_SELECAO) - 1){ //REMOVER ULTIMA CELULA POIS VOLTAMOS UMA CÉLULA PARA TRÁS
            

                var POSICAO_ULTIMA_CELULA = Math.max(...NOVA_SELECAO);
                
                let POSICAO_ULTIMA_CELULA_PARAM = PARAMETROS_EDITADOS["CELULAS"].indexOf(POSICAO_ULTIMA_CELULA);
                let POSICAO_ULTIMA_CELULA_NOVA  = NOVA_SELECAO.indexOf(POSICAO_ULTIMA_CELULA);

                //REMOVENDO ITEM DA LISTA  
                NOVA_SELECAO.splice(POSICAO_ULTIMA_CELULA_NOVA, 1); 
                PARAMETROS_EDITADOS["CELULAS"].splice(POSICAO_ULTIMA_CELULA_PARAM, 1); 

                //REMOVENDO BORDA 
                let ULTIMA_CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ POSICAO_ULTIMA_CELULA }"]` )
                ULTIMA_CELULA.classList.remove('CELULA_SELECIONADA');
                ULTIMA_CELULA.classList.remove('ULTIMA');

                
                DESENHAR_BORDA(NOVA_SELECAO)
            }
        
        }

        if(SENTIDO_SELECAO === `ESQUERDA`){

            if (POSICAO_CELULA == Math.min(...PARAMETROS_EDITADOS["CELULAS"]) - 1){
    

                PARAMETROS_EDITADOS["CELULAS"].push(POSICAO_CELULA);
                DESENHAR_BORDA(PARAMETROS_EDITADOS["CELULAS"])

            }
            if (POSICAO_CELULA == Math.min(...PARAMETROS_EDITADOS["CELULAS"]) + 1){
            
                var POSICAO_ULTIMA_CELULA =  Math.min(...PARAMETROS_EDITADOS["CELULAS"]);

                let POSICAO_ULTIMA_CELULA_PARAM = PARAMETROS_EDITADOS["CELULAS"].indexOf(POSICAO_ULTIMA_CELULA);
                let POSICAO_ULTIMA_CELULA_NOVA  = NOVA_SELECAO.indexOf(POSICAO_ULTIMA_CELULA);

                //REMOVENDO ITEM DA LISTA  
                NOVA_SELECAO.splice(POSICAO_ULTIMA_CELULA_NOVA, 1); 
                PARAMETROS_EDITADOS["CELULAS"].splice(POSICAO_ULTIMA_CELULA_PARAM, 1); 

                //REMOVENDO BORDA 
                let ULTIMA_CELULA = document.querySelector(`#LINHA_EM_EDICAO td[headers="${ POSICAO_ULTIMA_CELULA }"]` )
                ULTIMA_CELULA.classList.remove('CELULA_SELECIONADA');
                ULTIMA_CELULA.classList.remove('PRIMEIRA');


                DESENHAR_BORDA(PARAMETROS_EDITADOS["CELULAS"])
    
            }
        }
    }
})

document.body.addEventListener('mouseup', function() {
    
    if(MOUSE_PRESSIONADO){MOUSE_PRESSIONADO = false}
  
});

document.addEventListener('keydown', async function (event) {
  
    
    let CELULAS_SELECIONADAS = document.querySelectorAll('.CELULA_SELECIONADA');

    //AO DIGITAR ALGUM NUMERO
    if (event.key >= '0' && event.key <= '9') {
      
      NOVO_VALOR +=  event.key

      CELULAS_SELECIONADAS.forEach(function(elemento) {
        elemento.innerText = "";
      });

      CELULAS_SELECIONADAS.forEach(function(elemento) {
        elemento.innerText = NOVO_VALOR;
  
      });
    }

    //AO APAGAR UM DIGITO
    if (event.key === 'Backspace') {

        NOVO_VALOR = NOVO_VALOR.slice(0, -1)
        
        CELULAS_SELECIONADAS.forEach(function(elemento) {
            elemento.innerText = "";
        });

        CELULAS_SELECIONADAS.forEach(function(elemento) {
            elemento.innerText = NOVO_VALOR;
        });

    }
  
    if (event.key === "Escape") { LIMPAR_SELECOES()  }
    if ( event.ctrlKey )        { ctrlPressed = true }
  
});

document.addEventListener('keyup', function(event) {
    
    if (!event.ctrlKey) { ctrlPressed = false }

})