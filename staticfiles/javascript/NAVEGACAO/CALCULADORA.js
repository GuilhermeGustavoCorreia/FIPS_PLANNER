

var shift_pressed = false
let CALCULADORA = document.getElementById("CALCULADORA")
let VALOR_SOMA  = document.getElementById("CALCULADORA_VALOR")
let MOUSE_PRESS = false

function mostrar_calculadora(abrir_calculadora){

    if (abrir_calculadora === true ){
        CALCULADORA.classList.remove("oculto")
    }
    else {
        
        var elementos = document.querySelectorAll('.item_somado' );
        elementos.forEach(function(elemento) {
          elemento.classList.remove('item_somado');
        });
        CALCULADORA.classList.add("oculto")
        
    }
}


document.addEventListener('keyup', async function (event) {
    
    if (!event.shiftKey) { 
        shift_pressed = false
        mostrar_calculadora(false)
        VALOR_SOMA.textContent = ""
    }

})


document.addEventListener('keydown', async function (event) {

    if (event.shiftKey) {  
        shift_pressed = true
        mostrar_calculadora(true)

    }

})


document.body.addEventListener('mousedown', async function(event) {
   
    if (shift_pressed === true){
        let ITEM_CLICADO = event.target.innerText
        
        if( !isNaN(ITEM_CLICADO))
        {
             MOUSE_PRESS = true
            event.target.classList.add("item_somado")
            VALOR_SOMA.textContent = Number(ITEM_CLICADO) + Number(VALOR_SOMA.textContent)
        }

    }
        

})
document.body.addEventListener('mouseup', async function(event) {
    MOUSE_PRESS = false
})

document.body.addEventListener('mouseover', async function(event) {
    
    if (shift_pressed === true && MOUSE_PRESS === true) {
        let ITEM_SELECIONADO = event.target.innerText

        if( !isNaN(ITEM_SELECIONADO))
            {
                
                event.target.classList.add("item_somado")
                VALOR_SOMA.textContent = Number(ITEM_SELECIONADO) + Number(VALOR_SOMA.textContent)
            }
    }

})