
//#region TOOGLES
$(document).ready(function(){
    $("#SECAO_DESCARGAS_ATIVAS").click(function(){

      $("#CONTEUDO_DESCARGAS_ATIVAS").slideToggle();

    });
});

$(document).ready(function(){
  $("#SECAO_INSERIR_PREVISAO").click(function(){

    $("#CONTEUDO_INSERIR_PREVISAO").slideToggle();

  });
});

$(document).ready(function(){
  $("#SECAO_SUBIDAS_ATIVAS").click(function(){

    $("#CONTEUDO_SUBIDAS_ATIVAS").slideToggle();

  });
});

$(document).ready(function(){
  $("#SECAO_EDITAR_PXO").click(function(){

    $("#CONTEUDO_EDITAR_PXO").slideToggle();

  });
});

$(document).ready(function(){
  $("#SECAO_DOWNLOADS").click(function(){

    $("#CONTEUDO_DOWNLOADS").slideToggle();

  });
});

$(document).ready(function(){
  $("#SECAO_INTEGRACAO").click(function(){

    $("#CONTEUDO_INTEGRACAO").slideToggle();

  });
});
//#endregion

class mudarElemento {

  constructor(elemento) {

      this.elemento       = elemento
      this.valor_original = elemento.textContent
      this.posicao_coluna = elemento.cellIndex
  }

  para_textBox() {
      
      var textBox = document.createElement('input');
      
      textBox.className = 'INPUT';
      textBox.id = this.elemento.id;
      textBox.type = 'text';
      textBox.placeholder = this.valor_original;
      
      this.elemento.classList.add("BORDA_VERDE");

      this.elemento.innerHTML = '';
      this.elemento.appendChild(textBox);

      return textBox

  }

  voltar_ao_nomral() {
      this.elemento.classList.remove("BORDA_VERDE");
      this.elemento.innerHTML = this.valor_original;
  }

}

var editando_celula       = false;
var elementoTransformado  = null;
var tbEdicao              = null
var celula_selecionada    = null;
var ACAO                  = null;

var NOVO_VALOR = null

var TIPO_PXO = null;
var FERROVIA = null;
var TERMINAL = null;

function celula_modo_edicao(celula_selecionada){

  //#region DESCARGAS_ATIVAS
  if      ((editando_celula === false) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "DESCARGAS_ATIVAS"))
  {
      ACAO = "DESCARGAS_ATIVAS"
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();
      tbEdicao.focus();
      editando_celula = true;
  }
  else if ((editando_celula === true) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "DESCARGAS_ATIVAS"))  
  {
      ACAO = "DESCARGAS_ATIVAS"
      tbEdicao = elementoTransformado.voltar_ao_nomral();
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();

  }
  //#endregion

  //#region RESTRICOES_ATIVAS
  else if ((editando_celula === false) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "RESTRICOES_ATIVAS"))
  {
    ACAO = "RESTRICOES_ATIVAS"
    elementoTransformado = new mudarElemento(celula_selecionada);
    tbEdicao = elementoTransformado.para_textBox();
    tbEdicao.focus();
    editando_celula = true;
  }
  else if ((editando_celula === true) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "RESTRICOES_ATIVAS"))  
  {
    ACAO  = "RESTRICOES_ATIVAS"
    tbEdicao = elementoTransformado.voltar_ao_nomral();
    elementoTransformado = new mudarElemento(celula_selecionada);
    tbEdicao = elementoTransformado.para_textBox();
  }
  //#endregion

  //#region SUBIDAS_ATIVAS
  else if ((editando_celula === false) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "SUBIDAS_ATIVAS"))
  {
      ACAO = "SUBIDAS_ATIVAS"
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();
      tbEdicao.focus();
      editando_celula = true;

      FERROVIA = celula_selecionada.dataset.ferrovia
      TERMINAL = celula_selecionada.dataset.terminal
  }
  else if ((editando_celula === true) && (celula_selecionada.tagName !== "INPUT") )  
  {
      ACAO = null
      tbEdicao = elementoTransformado.voltar_ao_nomral();
      editando_celula = false;

  }
  //#endregion

  //#region PxO
  else if ((editando_celula === false) && (celula_selecionada.tagName === "TD") && (celula_selecionada.getAttribute('name') === "PXO"))
  {
      ACAO = "PXO"
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();
      tbEdicao.focus();
      editando_celula = true;

      TIPO_PXO = celula_selecionada.headers
      TERMINAL = celula_selecionada.id
  }
  
  else if ((editando_celula === true) && (celula_selecionada.tagName !== "INPUT"))  
  {
      ACAO = null
      tbEdicao = elementoTransformado.voltar_ao_nomral();
      editando_celula = false;
  }
  //#endregion

}

document.body.addEventListener('click', async function(event) {

  celula_selecionada = event.target;
  celula_modo_edicao(celula_selecionada);

});


