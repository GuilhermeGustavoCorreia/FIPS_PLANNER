
function TOOGLE_FORMULARIO(TIPO=null, ID_RESTRICAO=null){


    let TITULO_FORMULARIO   = document.getElementById("TITULO_FORMULARIO");
    let OVERLAY             = document.getElementById("OVERLAY");
    let FORMULARIO          = document.getElementById("FORMULARIO_RESTRICAO");
    let TIPO_FORMULARIO     = document.getElementById("TIPO_FORMULARIO");
    let ID_EDICAO           = document.getElementById("ID_EDICAO");

    if (TIPO === "CRIAR_RESTRICAO"){

        TITULO_FORMULARIO.textContent   = "Criar Restrição"
        TIPO_FORMULARIO.value           = "CRIAR"
        FORMULARIO.action               = "criar_restricao"
    }
    if (TIPO === "EDITAR_RESTRICAO"){

        TITULO_FORMULARIO.textContent = "Editar Restrição"
        TIPO_FORMULARIO.value = "EDITAR"
        ID_EDICAO.value = ID_RESTRICAO
    }

    let ELEMENTOS = [FORMULARIO, OVERLAY]

    for (i = 0; i < ELEMENTOS.length; i++){

        if (ELEMENTOS[i].style.display === "none" || ELEMENTOS[i].style.display === "") {
            ELEMENTOS[i].style.display = "block";

        } else {
            ELEMENTOS[i].style.display = "none";
            
        }
    }
}


function updateTerminals() {

    var SELECT_MERCADORIAS = document.getElementById("id_mercadoria");
    var SELECT_TERMINAL    = document.getElementById('id_terminal');
    var MERCADORIA_SELECIONADA = SELECT_MERCADORIAS.value;

    // Limpa as opções existentes
    SELECT_TERMINAL.innerHTML = '';

    // Adiciona novas opções
    if (MERCADORIA_SELECIONADA in MERCADORIAS) {
        MERCADORIAS[MERCADORIA_SELECIONADA].forEach(function(terminal) {
            var option = document.createElement('option');
            option.value = terminal;
            option.textContent = terminal;
            SELECT_TERMINAL.appendChild(option);
        });
    }
}

function PREENCHER_OPCOES(PARAMETROS, INPUTS) {
        
    let LISTA_MERCADORIAS = PARAMETROS.PRODUTOS;
    let LISTA_TERMINAIS   = PARAMETROS.TERMINAIS;

    LISTA_MERCADORIAS.unshift(PARAMETROS.ITENS_SELECIONADOS.PRODUTO);
    LISTA_TERMINAIS.unshift(PARAMETROS.ITENS_SELECIONADOS.TERMINAL);
    
    INPUTS.PRODUTOS.onchange = function() {ATUALIZAR_TERMINAIS( INPUTS )}
    
    INPUTS.PRODUTOS.innerHTML  = '';
    INPUTS.TERMINAIS.innerHTML = '';
    
    // Adiciona novas opções
    for (let i = 0; i < LISTA_MERCADORIAS.length; i++) {

        const option = document.createElement('option');
        option.value = LISTA_MERCADORIAS[i];
        option.textContent = LISTA_MERCADORIAS[i];
        INPUTS.PRODUTOS.appendChild(option);
    }

    for (let i = 0; i < LISTA_TERMINAIS.length; i++) {

        const option = document.createElement('option');
        option.value = LISTA_TERMINAIS[i];
        option.textContent = LISTA_TERMINAIS[i];
        INPUTS.TERMINAIS.appendChild(option);
    }   
}

window.addEventListener('load', function(){


    let PARAMETROS = {
                        
        PRODUTOS:   Object.keys(MERCADORIAS),
        TERMINAIS:  MERCADORIAS["ACUCAR"],
        
        ITENS_SELECIONADOS: {
            PRODUTO: ["ACUCAR"], 
            TERMINAL: ["TAC ACUCAR"]
        }   

    }

    let INPUTS = {
        PRODUTOS:  document.getElementById("mercadoria_01"),
        TERMINAIS: document.getElementById("terminal_01")
    }



    PREENCHER_OPCOES(PARAMETROS, INPUTS)

   

});

var ID_RESTRICAO_EDICAO = 0
function EDITAR_RESTRICAO(ID_RESTRICAO){

    ID_RESTRICAO_EDICAO = ID_RESTRICAO

    $.ajax({
        url: `/restricao/editar/${ ID_RESTRICAO_EDICAO }/`,
        type: 'GET',
        data: {},
        success: function(response) {

            $('#id_mercadoria').val(response.mercadoria);
            updateTerminals()
            
            $('#id_terminal').val(response.terminal);
            $('#id_comeca_em').val(response.comeca_em);
            $('#id_termina_em').val(response.termina_em);

            $('#id_porcentagem').val(response.porcentagem);
            $('#id_motivo').val(response.motivo);
            $('#id_comentario').val(response.comentario);

            // Abrir o modal de edição
            TOOGLE_FORMULARIO('EDITAR_RESTRICAO', ID_RESTRICAO_EDICAO);
        },
        error: function(xhr) {
            alert("ERRO")
        }
    });
}


