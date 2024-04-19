import pandas as pd
import json


def ABRIR_TERMINAIS_ATIVOS():

    DATAFRAME = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.CSV", sep=";", index_col=0)

    with open(f"previsao_trens/src/DICIONARIOS/PRODUTOS_E_TERMINAIS.json") as ARQUIVO_DESCARGA:
        dict_PRODUTOS_TERMINAIS = json.load(ARQUIVO_DESCARGA)

    SAIDAS = {}

    FERROVIAS = ["RUMO", "MRS", "VLI"]

    for PRODUTO, TERMINAIS in dict_PRODUTOS_TERMINAIS.items():
        SAIDAS[PRODUTO] = {}

        for TERMINAL in TERMINAIS:

            SAIDAS[PRODUTO][TERMINAL] = {}

            for FERROVIA in FERROVIAS:
                SAIDAS[PRODUTO][TERMINAL][FERROVIA] = DATAFRAME.loc[TERMINAL, f"{FERROVIA}_{PRODUTO}"]
    
    return  SAIDAS
    