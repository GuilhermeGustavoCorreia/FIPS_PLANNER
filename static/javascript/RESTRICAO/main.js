
function TOOGLE_FORMULARIO(TIPO=null){


    let TITULO_FORMULARIO   = document.getElementById("TITULO_FORMULARIO");
    let OVERLAY             = document.getElementById("OVERLAY");
    let FORMULARIO          = document.getElementById("FORMULARIO_RESTRICAO");
    let TIPO_FORMULARIO     = document.getElementById("TIPO_FORMULARIO");
    
    if (TIPO === "CRIAR_RESTRICAO"){

        TITULO_FORMULARIO.textContent = "Criar Restrição"
        TIPO_FORMULARIO.value = "CRIAR"
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

function ENVIAR_FORMULARIO(TIPO, CRSF_TOKEN){

    event.preventDefault();

}