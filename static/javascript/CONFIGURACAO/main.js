

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

var editando_celula = false;
var elementoTransformado = null;
var tbEdicao = null
var celula_selecionada = null;

var NOVO_VALOR = null



function celula_modo_edicao(celula_selecionada){

  if      ((editando_celula === false) && (celula_selecionada.tagName === "TD"))
  {
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();
      tbEdicao.focus();
      editando_celula = true;
  }
  else if ((editando_celula === true) && (celula_selecionada.tagName === "TD"))  
  {
      tbEdicao = elementoTransformado.voltar_ao_nomral();
      elementoTransformado = new mudarElemento(celula_selecionada);
      tbEdicao = elementoTransformado.para_textBox();

  }
  else if ((editando_celula === true) && (celula_selecionada.tagName !== "INPUT") )  
  {
      tbEdicao = elementoTransformado.voltar_ao_nomral();
      editando_celula = false;

  }

}

document.body.addEventListener('click', async function(event) {

  celula_selecionada = event.target;
  celula_modo_edicao(celula_selecionada);

});


