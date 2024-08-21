
function corrigirSintaxeJSON(stringComErro) {
    // Remover apóstrofos desnecessários das chaves e nomes de string
    let stringCorrigida = stringComErro
        .replace(/'/g, '"')  // Substitui todos os apóstrofos por aspas duplas
        .replace(/([{,]\s*)([A-Za-z0-9_]+)\s*:/g, '$1"$2":');  // Adiciona aspas duplas em nomes de chave

    return stringCorrigida;
}
function LIMPAR_SELECOES(){


    var CELULAS_SELECIONADAS    = document.querySelectorAll('.CELULA_SELECIONADA');
    var CELULAS_PRIMEIRA        = document.querySelectorAll('.PRIMEIRA');
    var CELULAS_ULTIMA          = document.querySelectorAll('.ULTIMA');
    
    CELULAS_PRIMEIRA.forEach(function(CELULA)       {CELULA.classList.remove('PRIMEIRA');});
    CELULAS_ULTIMA.forEach(function(CELULA)         {CELULA.classList.remove('ULTIMA');});
    CELULAS_SELECIONADAS.forEach(function(CELULA)   {CELULA.classList.remove('CELULA_SELECIONADA');});

    let LINHA_PRODUTIVIDADE = document.getElementById('LINHA_EM_EDICAO')
    if (LINHA_PRODUTIVIDADE !== null) {LINHA_PRODUTIVIDADE.removeAttribute('id')}

    NOVO_VALOR         = ""
}

function ATUALIZAR_DESCARGA(DESCARGAS){

    for (let i = 0; i < DESCARGAS.length; i++){
        
        LIMPAR_SELECOES()

        let TERMINAL        = DESCARGAS[i]["TERMINAL"]
        let DATA_ARQ        = DESCARGAS[i]["DATA"]
        let TABELA_DESCARGA = document.getElementById(`${ TERMINAL }_${ DATA_ARQ }`)
       
        // SEXTA 13:45 

        if(TABELA_DESCARGA){

            let DESCARGAS_ATIVAS = JSON.parse(corrigirSintaxeJSON(TABELA_DESCARGA.querySelector(`#DESCARGAS_ATIVAS`).value))
        
            //#region REMOVENDO O QUE NAO ESTA ATIVO
            for (let CHAVE in DESCARGAS_ATIVAS) {
                if (DESCARGAS_ATIVAS[CHAVE].length == 0){ delete DESCARGAS[i]["DESCARGAS"][CHAVE]; delete DESCARGAS_ATIVAS[CHAVE];}
            }
            //#endregion

            //#region INSERINDO A LINHA DA PEDRA
            for (let k = 0; k < 24; k++){
                let FILTRO_PEDRA         = `td[headers="${k}"][name="LINHA_PEDRA"]`

                let ELEMENTO_PEDRA       = TABELA_DESCARGA.querySelector(FILTRO_PEDRA);
                if (Number(DESCARGAS[i]["PEDRA"][k]) !== 0) {ELEMENTO_PEDRA.innerText = DESCARGAS[i]["PEDRA"][k]}
                else                                        {ELEMENTO_PEDRA.innerText = ""}
            }
            //#endregion
      
            //#region INSERINDO TOTAIS

            let TOTAL_SALDO = TABELA_DESCARGA.querySelector("#TOTAL_SALDO")

            if (Number(DESCARGAS[i]["INDICADORES"]["TOTAL_SALDO"]) !== 0)
            {TOTAL_SALDO.innerText = DESCARGAS[i]["INDICADORES"]["TOTAL_SALDO"]}
            
            
            let TOTAL_PEDRA = TABELA_DESCARGA.querySelector("#TOTAL_PEDRA")
            if (Number(DESCARGAS[i]["INDICADORES"]["TOTAL_PEDRA"]) !== 0)
            {TOTAL_PEDRA.innerText = DESCARGAS[i]["INDICADORES"]["TOTAL_PEDRA"]}

            let PEDRAS = {
                "RUMO":  {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "MRS":   {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "VLI":   {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "TOTAL": {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
            }

            let ELEMENTO_RUMO_P1       = TABELA_DESCARGA.querySelector(`td[data-periodo="1"].TOTAL_FERROVIA_RUMO`);
            let ELEMENTO_RUMO_P2       = TABELA_DESCARGA.querySelector(`td[data-periodo="2"].TOTAL_FERROVIA_RUMO`);
            let ELEMENTO_RUMO_P3       = TABELA_DESCARGA.querySelector(`td[data-periodo="3"].TOTAL_FERROVIA_RUMO`);
            let ELEMENTO_RUMO_P4       = TABELA_DESCARGA.querySelector(`td[data-periodo="4"].TOTAL_FERROVIA_RUMO`);

            let ELEMENTO_MRS_P1       = TABELA_DESCARGA.querySelector(`td[data-periodo="1"].TOTAL_FERROVIA_MRS`);
            let ELEMENTO_MRS_P2       = TABELA_DESCARGA.querySelector(`td[data-periodo="2"].TOTAL_FERROVIA_MRS`);
            let ELEMENTO_MRS_P3       = TABELA_DESCARGA.querySelector(`td[data-periodo="3"].TOTAL_FERROVIA_MRS`);
            let ELEMENTO_MRS_P4       = TABELA_DESCARGA.querySelector(`td[data-periodo="4"].TOTAL_FERROVIA_MRS`);

            let ELEMENTO_VLI_P1       = TABELA_DESCARGA.querySelector(`td[data-periodo="1"].TOTAL_FERROVIA_VLI`);
            let ELEMENTO_VLI_P2       = TABELA_DESCARGA.querySelector(`td[data-periodo="2"].TOTAL_FERROVIA_VLI`);
            let ELEMENTO_VLI_P3       = TABELA_DESCARGA.querySelector(`td[data-periodo="3"].TOTAL_FERROVIA_VLI`);
            let ELEMENTO_VLI_P4       = TABELA_DESCARGA.querySelector(`td[data-periodo="4"].TOTAL_FERROVIA_VLI`);

            let ELEMENTO_TOTAIS_P1       = TABELA_DESCARGA.querySelector(`td[data-periodo="1"].TITLO_TOTAIS`);
            let ELEMENTO_TOTAIS_P2       = TABELA_DESCARGA.querySelector(`td[data-periodo="2"].TITLO_TOTAIS`);
            let ELEMENTO_TOTAIS_P3       = TABELA_DESCARGA.querySelector(`td[data-periodo="3"].TITLO_TOTAIS`);
            let ELEMENTO_TOTAIS_P4       = TABELA_DESCARGA.querySelector(`td[data-periodo="4"].TITLO_TOTAIS`);

            ELEMENTO_RUMO_P1.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["RUMO"]["P1"]
            ELEMENTO_RUMO_P2.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["RUMO"]["P2"]
            ELEMENTO_RUMO_P3.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["RUMO"]["P3"]
            ELEMENTO_RUMO_P4.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["RUMO"]["P4"]
            
            ELEMENTO_MRS_P1.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["MRS"]["P1"]
            ELEMENTO_MRS_P2.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["MRS"]["P2"]
            ELEMENTO_MRS_P3.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["MRS"]["P3"]
            ELEMENTO_MRS_P4.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["MRS"]["P4"]
            
            ELEMENTO_VLI_P1.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["VLI"]["P1"]
            ELEMENTO_VLI_P2.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["VLI"]["P2"]
            ELEMENTO_VLI_P3.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["VLI"]["P3"]
            ELEMENTO_VLI_P4.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["VLI"]["P4"]
            
            ELEMENTO_TOTAIS_P1.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["TOTAL"]["P1"]
            ELEMENTO_TOTAIS_P2.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["TOTAL"]["P2"]
            ELEMENTO_TOTAIS_P3.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["TOTAL"]["P3"]
            ELEMENTO_TOTAIS_P4.innerText = DESCARGAS[i]["INDICADORES"]["PEDRAS"]["TOTAL"]["P4"]

            //#endregion

            for (let FERROVIA in DESCARGAS_ATIVAS){
                
                for (let j = 0; j < DESCARGAS_ATIVAS[FERROVIA].length; j++){
                    
                    let PRODUTO = DESCARGAS_ATIVAS[FERROVIA][j]
                    
                    //#region INSERINDO SALDO DE VIRADA

                    let FILTRO_SALDO_VIRADA         = `td[data-ferrovia="${FERROVIA}"][data-produto="${PRODUTO}"][headers="SALDO_VIRADA"]`

                    let ELEMENTO_SALDO_VIRADA       = TABELA_DESCARGA.querySelector(FILTRO_SALDO_VIRADA);

                    ELEMENTO_SALDO_VIRADA.innerText = DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"]

                    //#endregion

                    //#region INSERINDO TOTAL PRODUTIVIDADE 

                    let FILTRO_TOTAL_PRODUTIVIDADE  = `td[data-ferrovia="${FERROVIA}"][data-produto="${PRODUTO}"][name="TOTAL_PRODUTIVIDADE"]`

                    let ELEMENTO_TOTAL_PRODUTIVIDADE       = TABELA_DESCARGA.querySelector(FILTRO_TOTAL_PRODUTIVIDADE);
           
                    ELEMENTO_TOTAL_PRODUTIVIDADE.innerText = DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["TOTAL_PRODUTIVIDADE"]

                    //#endregion

                    for (let k = 0; k < 24; k++){

                        //#region INSERINDO A LINHA DA PRODUTIVIDADE

                        let FILTRO_PRODUTIVIDADE         = `td[data-ferrovia="${FERROVIA}"][data-produto="${PRODUTO}"][headers="${k}"][name="PRODUTIVIDADE"]`

                        let ELEMENTO_PRODUTIVIDADE       = TABELA_DESCARGA.querySelector(FILTRO_PRODUTIVIDADE);
                        if (Number(DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"][k]) !== 0) {ELEMENTO_PRODUTIVIDADE.innerText = DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"][k]}
                        else                                                                                {ELEMENTO_PRODUTIVIDADE.innerText = ""}
                        //#endregion

                        //#region INSERINDO A LINHA DO SALDO

                        let FILTRO_SALDO         = `td[data-ferrovia="${FERROVIA}"][data-produto="${PRODUTO}"][headers="${k}"][name="SALDO"]`

                        let ELEMENTO_SALDO       = TABELA_DESCARGA.querySelector(FILTRO_SALDO);
                        if (Number(DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["SALDO"][k]) !== 0)
                        {ELEMENTO_SALDO.innerText = DESCARGAS[i]["DESCARGAS"][FERROVIA][PRODUTO]["SALDO"][k]}
                        else                                        {ELEMENTO_SALDO.innerText = ""}
                        //#endregion
                    
                    }
                }
            }      
        }    
    }
}