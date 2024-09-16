import pandas as pd
import json
import os

def ABRIR_TERMINAIS_ATIVOS():

    DATAFRAME           = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",     sep=";", index_col=0)
    RESTRICOES_ATIVAS   = pd.read_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv",    sep=";", index_col=0)

    with open(f"previsao_trens/src/DICIONARIOS/PRODUTOS_E_TERMINAIS.json") as ARQUIVO_DESCARGA:
        dict_PRODUTOS_TERMINAIS = json.load(ARQUIVO_DESCARGA)

    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        jsTERMINAIS = json.load(ARQUIVO_DESCARGA)

    SAIDAS = {
        "DESCARGAS_ATIVAS"  : {},
        "SUBIDAS_ATIVAS"    : {},
        "TERMINAIS"         : jsTERMINAIS
    }

    FERROVIAS = ["RUMO", "MRS", "VLI"]

    for PRODUTO, TERMINAIS in dict_PRODUTOS_TERMINAIS.items():
        SAIDAS["DESCARGAS_ATIVAS"][PRODUTO] = {}

        for TERMINAL in TERMINAIS:
            SAIDAS["DESCARGAS_ATIVAS"][PRODUTO][TERMINAL] = {}

            for FERROVIA in FERROVIAS:
                SAIDAS["DESCARGAS_ATIVAS"][PRODUTO][TERMINAL][FERROVIA] = DATAFRAME.loc[TERMINAL, f"{FERROVIA}_{PRODUTO}"]

            SAIDAS["DESCARGAS_ATIVAS"][PRODUTO][TERMINAL]["RESTRICAO"] = RESTRICOES_ATIVAS.loc[TERMINAL, PRODUTO]  
    
    SUBIDAS_ATIVAS = pd.read_csv("previsao_trens/src/SUBIDA/PARAMETROS/TERMINAIS_ATIVOS.csv", sep=";", index_col=0)
    
    SAIDAS["SUBIDAS_ATIVAS"] = SUBIDAS_ATIVAS.to_json(orient='index', indent=4)
    SAIDAS["SUBIDAS_ATIVAS"] = json.loads(SAIDAS["SUBIDAS_ATIVAS"])

    SAIDAS["RESTRICOES_ATIVAS"] = RESTRICOES_ATIVAS.to_json(orient='index', indent=4)
    SAIDAS["RESTRICOES_ATIVAS"] = json.loads(SAIDAS["RESTRICOES_ATIVAS"])

    return  SAIDAS
    