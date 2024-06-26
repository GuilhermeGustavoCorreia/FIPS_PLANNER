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
  
  var TIPO          = null
  var DIA_LOGISTICO = null

  var PARAMETROS_BUFFER = {}
function celula_modo_edicao(celula_selecionada){

    //console.log(`EDITANDO CÉLULA: ${editando_celula} CELULA SELECIONADA: ${celula_selecionada.getAttribute('name')}`)

    if ((editando_celula === false) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_VAZIO_TERMINAL")) {

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

let MARGEM = ""
let HORA   = ""

function MOSTRAR_VAGOES_FORMULARIO(MARGEM, FERROVIA, HORA){

    let NAME    = `CONDENSADOS_${FERROVIA}`;
    let CELULAS = document.querySelectorAll(`[name="${NAME}"]`);

    let CELULAS_FILTRADAS = Array.from(CELULAS).filter(CELULA => CELULA.dataset.margem === MARGEM && CELULA.dataset.hora === HORA);
    

    let CELULA_GRAO = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "GRAO");
    if (CELULA_GRAO)    {document.getElementById("FRM_QT_GRAO").innerHTML = CELULA_GRAO.innerHTML;} 
    else                {document.getElementById("FRM_QT_GRAO").innerHTML = 0 }

    let CELULA_FERT = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "FERTILIZANTE");
    if (CELULA_FERT)    {document.getElementById("FRM_QT_FERTILIZANTE").innerHTML = CELULA_FERT.innerHTML;} 
    else                {document.getElementById("FRM_QT_FERTILIZANTE").innerHTML = 0 }

    let CELULA_CELU = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "CELULOSE");
    if (CELULA_CELU)    {document.getElementById("FRM_QT_CELULOSE").innerHTML = CELULA_CELU.innerHTML;} 
    else                {document.getElementById("FRM_QT_CELULOSE").innerHTML = 0 }
    
    let FRM_QT_ACUCAR = CELULAS_FILTRADAS.find(CELULA => CELULA.dataset.segmento === "ACUCAR");
    if (FRM_QT_ACUCAR)  {document.getElementById("FRM_QT_ACUCAR").innerHTML = FRM_QT_ACUCAR.innerHTML;} 
    else                {document.getElementById("FRM_QT_ACUCAR").innerHTML = 0 } 

    //console.log(`NOME: ${NAME} - MARGEM: ${MARGEM} HORA: ${HORA}`)
    //console.log(`CELULAS:           ${CELULAS}`)
    
    /*console.log(`CELULAS FILTRADAS: ${CELULAS_FILTRADAS}`)
    console.log(`EXEMPLO: ${CELULAS[0]}`)
    console.log(CELULAS[0].tagName); // Retorna a tag do elemento (no caso, "TD" ou "TH" para células de tabela)
    console.log(CELULAS[0].colSpan); // Retorna o número de colunas que a célula ocupa em uma tabela
    console.log(CELULAS[0].rowSpan); // Retorna o número de linhas que a célula ocupa em uma tabela
    console.log(CELULAS[0].classList);*/

    /*console.log(`GRAOS:         ${CELULA_GRAO}`)
    console.log(`FERTILIZANTE:  ${CELULA_FERT}`)
    console.log(`CELULOSE:      ${CELULA_CELU}`)
    console.log(`ACUCAR:        ${FRM_QT_ACUCAR}`)*/

}   

const modal = document.querySelector(".DIALOG_TREM_VAZIO");
function criar_trem_subida(event) {
    
    let TITULO          = document.getElementById("TITULO_MODAL")
    let COLUNA          = event.target.dataset.hora;
    let ACAO            = document.getElementById("ACAO_FORMULARIO_TREM_VAZIO");
    let DIA_LOGISTICO   = document.getElementById("DIA_LOGISTICO_FORM");
    let HORA_FRM                = document.getElementById("HORA_FORM");
    let MARGEM_FRM      = document.getElementById("MARGEM_FORM");

    

    DIA_LOGISTICO.value = event.target.dataset.dia;
    ACAO.value          = "CRIAR_TREM_SUBIDA";
    MARGEM              = event.target.dataset.margem;
    HORA_FRM.value          = COLUNA;
    HORA                    = COLUNA;
    MARGEM_FRM.value    = MARGEM;
    TITULO.textContent  = `${ MARGEM } -> ${ COLUNA }h`

    BTN_CRIAR_TREM_SUBIDA.disabled = true

    MOSTRAR_VAGOES_FORMULARIO(MARGEM, "RUMO", COLUNA)
    modal.showModal()

}

function ATUALIZAR_VAGOES() {
    let FERROVIA = document.querySelector('input[name="ferrovia"]:checked').value;
    MOSTRAR_VAGOES_FORMULARIO(MARGEM, FERROVIA, HORA)
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

//#region EDITAR BUFFER



//#endregion