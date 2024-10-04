class mudarElemento {

    constructor(elemento) {
  
        this.elemento       = elemento
        this.valor_original = elemento.textContent
        this.posicao_coluna = elemento.cellIndex
    }
  
    para_textBox() {
  
        var textBox = document.createElement('input');
        
        textBox.className = 'INPUT_SALDO_VIRADA';
        textBox.id = 'tbEditarSaldoVirada';
        textBox.type = 'text';
        textBox.placeholder = this.valor_original;
        
        this.elemento.classList.add("BORDA_VERDE")
        
        this.elemento.innerHTML = '';
        this.elemento.appendChild(textBox)
  
        return textBox
  
    }
  
    voltar_ao_nomral(){
        this.elemento.classList.remove("BORDA_VERDE")
        this.elemento.innerHTML = this.valor_original;
    }
  
}
  
  var editando_celula       = false;
  var elementoTransformado  = null;
  var tbEdicao              = null
  var celula_selecionada    = null;
  var NOVO_VALOR            = null
  
  var SEGMENTO = null
  var FERROVIA = null
  var TERMINAL = null
  var MARGEM   = null

  var TIPO          = null
  var DIA_LOGISTICO = null

  var PARAMETROS_BUFFER = {}
  
function celula_modo_edicao(celula_selecionada){

      //#region CONDENSADOS 

    if ((editando_celula === false) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_CONDENSADOS")) {
        
        TIPO     = "SALDO_CONDENSADOS"

        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        MARGEM   = celula_selecionada.dataset.margem

        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
        tbEdicao.focus();
        editando_celula = true;

    }

    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_CONDENSADOS"))  {

        TIPO     = "SALDO_CONDENSADOS"

        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        TERMINAL = celula_selecionada.dataset.terminal

        tbEdicao = elementoTransformado.voltar_ao_nomral();
        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
  
    }
    //#endregion

    //#region SALDO_VIRADA_VAZIO_TERMINAL 
    else if ((editando_celula === false) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_VAZIO_TERMINAL")) {

        TIPO     = "SALDO_TERMINAL"
        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        TERMINAL = celula_selecionada.dataset.terminal

        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
        tbEdicao.focus();
        editando_celula = true;

    }

    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_VAZIO_TERMINAL"))  {

        TIPO     = "SALDO_TERMINAL"
        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        TERMINAL = celula_selecionada.dataset.terminal

        tbEdicao = elementoTransformado.voltar_ao_nomral();
        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
  
    }
    //#endregion
    
    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') !== "INPUT"))   {
        
        tbEdicao = elementoTransformado.voltar_ao_nomral();
        editando_celula = false;
  
    }

    else if ((editando_celula === false) && (celula_selecionada.getAttribute('name') === "BUFFER")){
        
        TIPO            = "BUFFER"
        FERROVIA        = celula_selecionada.dataset.ferrovia
        HORA            = celula_selecionada.dataset.hora
        MARGEM          = celula_selecionada.dataset.margem
        DIA_LOGISTICO   = celula_selecionada.dataset.dia

        

        elementoTransformado    = new mudarElemento(celula_selecionada);
        tbEdicao                = elementoTransformado.para_textBox();
        tbEdicao.focus();
        editando_celula         = true;

    }

    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') === "BUFFER")){

        TIPO            = "BUFFER"
        FERROVIA        = celula_selecionada.dataset.ferrovia
        HORA            = celula_selecionada.dataset.hora
        MARGEM          = celula_selecionada.dataset.margem
        DIA_LOGISTICO   = celula_selecionada.dataset.dia

        tbEdicao = elementoTransformado.voltar_ao_nomral();
        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
  
    }

}

document.body.addEventListener('click', async function(event) {

    celula_selecionada = event.target;
    celula_modo_edicao(celula_selecionada);

});

//#region CRIAR TREM

const CELULAS_PREFIXO       = document.querySelectorAll('[name="CRIAR_TREM_SUBIDA"]');
const BTN_CRIAR_TREM_SUBIDA = document.getElementById("BTN_CRIAR_TREM_SUBIDA");

// Adiciona o evento de clique a cada elemento selecionado
CELULAS_PREFIXO.forEach(CELULA => {
    CELULA.addEventListener('click', criar_trem_subida);
});


let HORA   = ""

function MOSTRAR_VAGOES_FORMULARIO(MARGEM, FERROVIA, HORA, DIA_LOGISTICO){

    let NAME    = `CONDENSADOS_${FERROVIA}`;
    let CELULAS = document.querySelectorAll(`[name="${NAME}"]`);

    let CELULAS_FILTRADAS = Array.from(CELULAS).filter(CELULA => CELULA.dataset.margem === MARGEM && CELULA.dataset.hora === HORA && CELULA.dataset.dia === DIA_LOGISTICO);
    
    let CELULA_GRAO = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "GRAO");
    if (CELULA_GRAO)    { document.getElementById("FRM_QT_GRAO").innerHTML = CELULA_GRAO.innerHTML; } 
    else                { document.getElementById("FRM_QT_GRAO").innerHTML = 0 }

    let CELULA_FERT = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "FERTILIZANTE");
    if (CELULA_FERT)    { document.getElementById("FRM_QT_FERTILIZANTE").innerHTML = CELULA_FERT.innerHTML; } 
    else                { document.getElementById("FRM_QT_FERTILIZANTE").innerHTML = 0 }

    let CELULA_CELU = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "CELULOSE");
    if (CELULA_CELU)    { document.getElementById("FRM_QT_CELULOSE").innerHTML = CELULA_CELU.innerHTML; } 
    else                { document.getElementById("FRM_QT_CELULOSE").innerHTML = 0 }
    
    let FRM_QT_ACUCAR = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "ACUCAR");
    if (FRM_QT_ACUCAR)  { document.getElementById("FRM_QT_ACUCAR").innerHTML = FRM_QT_ACUCAR.innerHTML; } 
    else                { document.getElementById("FRM_QT_ACUCAR").innerHTML = 0 } 

}   

const modal = document.querySelector(".DIALOG_TREM_VAZIO");

function formartar_hora(data){

        const year      = data.getFullYear();
        const month     = String(data.getMonth() + 1).padStart(2, '0');
        const day       = String(data.getDate()).padStart(2, '0');
        const hours     = String(data.getHours()).padStart(2, '0');
        const minutes   = String(data.getMinutes()).padStart(2, '0');
        const seconds   = String(data.getSeconds()).padStart(2, '0');


        return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}`
}

function criar_trem_subida(event) {
    
    let TITULO          = document.getElementById("TITULO_MODAL")
    let COLUNA          = event.target.dataset.hora;
    let ACAO            = document.getElementById("ACAO_FORMULARIO_TREM_VAZIO");
    let lbl_DIA_LOGISTICO   = document.getElementById("DIA_LOGISTICO_FORM");
    let HORA_FRM        = document.getElementById("HORA_FORM");
    let MARGEM_FRM      = document.getElementById("margem_form_subida");

    document.getElementById("id_ferrovia_0").checked = true

    let previsao = new Date(`${event.target.parentNode.dataset.data_arq}T00:00:00`);   
    previsao.setHours(Number(COLUNA));
    DIA_LOGISTICO = event.target.dataset.dia
    document.getElementById('id_previsao').value = formartar_hora(previsao);
    document.getElementById('id_margem').value   = MARGEM;

    lbl_DIA_LOGISTICO.value     = DIA_LOGISTICO;
    ACAO.value              = "CRIAR_TREM_SUBIDA";
    MARGEM                  = event.target.dataset.margem;
    HORA_FRM.value          = COLUNA;
    HORA                    = COLUNA;
    MARGEM_FRM.value    = MARGEM;
    TITULO.textContent  = `${ MARGEM } -> ${ COLUNA }h`

    BTN_CRIAR_TREM_SUBIDA.disabled = true

    MOSTRAR_VAGOES_FORMULARIO(MARGEM, "RUMO", COLUNA, DIA_LOGISTICO)
    modal.showModal()

}

function ATUALIZAR_VAGOES() {
    
    let FERROVIA = document.querySelector('input[name="ferrovia"]:checked').value;
    MOSTRAR_VAGOES_FORMULARIO(MARGEM, FERROVIA, HORA, DIA_LOGISTICO)

}

document.querySelector('dialog').addEventListener('mousedown', event => {

    if (event.target === event.currentTarget) {
        event.currentTarget.close()
    }
    
})

//SOBRE OS INPUTS DE VAGOES 
function VALIDAR_QUANTIDADE(INPUT){

    let VALOR       = parseFloat(INPUT.value);  
    let SEGMENTO    = INPUT.dataset.segmento;
    let VALOR_MAX   = parseFloat(document.getElementById(`FRM_QT_${ SEGMENTO }`).innerHTML);

    if (VALOR > VALOR_MAX){
        BTN_CRIAR_TREM_SUBIDA.disabled = true
    }else{
        BTN_CRIAR_TREM_SUBIDA.disabled = false
    }

}

//#endregion

//#region MANTER A ABA ATUAL AO RECARREGAR A PAGINA

document.addEventListener('DOMContentLoaded', function() {
    var abaAtiva = localStorage.getItem('abaAtiva');
    if (abaAtiva) {
        document.querySelector(`[onclick="abrirAba(event, '${abaAtiva}')"]`).click();
    }
    
    var subAbaAtiva = localStorage.getItem('subAbaAtiva');
    if (subAbaAtiva) {
        document.querySelector(`[onclick="abrirSubAba(event, '${subAbaAtiva}')"]`).click();
    }
});

//#endregion



//#region DESATIVAR BOTAO FORM NOVO TREM VAZIO AO ENVIAR FORMULARIO

function disableButton() {
    document.getElementById('BTN_CRIAR_TREM_SUBIDA').disabled = true;
    document.getElementById('BTN_CRIAR_TREM_SUBIDA').innerText = 'Salvando...';
}

//#endregion
