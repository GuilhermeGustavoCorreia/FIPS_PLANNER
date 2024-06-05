class mudarElemento {

    constructor(elemento) {
  
        this.elemento       = elemento
        this.valor_original = elemento.textContent
        this.posicao_coluna = elemento.cellIndex
    }
  
    para_textBox() {
  
        var textBox = document.createElement('input');
        
        textBox.className = 'INPUT_SALDO_VIRADA';
        textBox.id = this.elemento.id;
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

function celula_modo_edicao(celula_selecionada){

    if ((editando_celula === false) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_VAZIO_TERMINAL"))
    {

        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        TERMINAL = celula_selecionada.dataset.terminal

        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
        tbEdicao.focus();
        editando_celula = true;

    }
    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') === "SALDO_VIRADA_VAZIO_TERMINAL"))  
    {

        SEGMENTO = celula_selecionada.dataset.segmento
        FERROVIA = celula_selecionada.dataset.ferrovia
        TERMINAL = celula_selecionada.dataset.terminal

        tbEdicao = elementoTransformado.voltar_ao_nomral();
        elementoTransformado = new mudarElemento(celula_selecionada);
        tbEdicao = elementoTransformado.para_textBox();
  
    }
    else if ((editando_celula === true) && (celula_selecionada.getAttribute('name') !== "INPUT") )  
    {
        
        tbEdicao = elementoTransformado.voltar_ao_nomral();
        editando_celula = false;
  
    }
  
}

document.body.addEventListener('click', async function(event) {

    celula_selecionada = event.target;
    celula_modo_edicao(celula_selecionada);

});




function modal_saldo_virada(botao){

    let OVERLAY = document.getElementById("OVERLAY")
    let MODAL   = document.getElementById("MODAL")
    let ACAO    = botao.dataset.acao
    let LINHA   = document.getElementById("NOME_DA_LINHA")
    let FERROVIA   = document.getElementById("FERROVIA_DA_LINHA")

    

    if (ACAO !== "FECHAR"){ 

        LINHA.value     = botao.dataset.linha
        FERROVIA.value  = botao.dataset.ferrovia

        let TITULO   = document.getElementById("TITULO_MODAL")
        TITULO.textContent = `${botao.dataset.linha} ${botao.dataset.ferrovia}`

    }

    
    let ELEMENTOS = [OVERLAY, MODAL]//, FORMULARIO

    for (i = 0; i < ELEMENTOS.length; i++){

        if (ELEMENTOS[i].style.display === "none" || ELEMENTOS[i].style.display === "") {
            ELEMENTOS[i].style.display = "block";
        } else {
            ELEMENTOS[i].style.display = "none";
        }
    }

}
