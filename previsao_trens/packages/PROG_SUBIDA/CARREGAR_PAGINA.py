import pandas as pd
import json


def CARREGAR_PROG_SUBIDA():

    TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        INFOS_TERMINAIS = json.load(ARQUIVO_DESCARGA)
    SAIDAS = {
        "D":{  
            "MARGENS": {},
            "DESCARGAS": {}
        }}
    # , 
    #     "D+1":{  
    #         "MARGENS": {},
    #         "DESCARGAS": []
    #     }, 
    #     "D+2":{  
    #         "MARGENS": {},
    #         "DESCARGAS": []
    #     }
    

    lst_TERMINAIS_ATIVOS  = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    

    for TERMINAL in lst_TERMINAIS_ATIVOS:

        DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
        DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS]

        MARGEM = INFOS_TERMINAIS[TERMINAL]["MARGEM"]
        PATIO  = INFOS_TERMINAIS[TERMINAL]["PATIO"]

        FERROVIAS_ATIVAS = {
            "RUMO": [],
            "MRS" : [],
            "VLI" : []
        }

        for ATIVO in DESCARGAS_ATIVAS:
            for FERROVIA in FERROVIAS_ATIVAS:
                if ATIVO[0] == FERROVIA: FERROVIAS_ATIVAS[FERROVIA].append(ATIVO[1]) 

        for DIA_LOGISTICO in SAIDAS.keys():
            
            DATA_ARQ = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO].iloc[0]['DATA_ARQ']
            with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:

                json_DESCARGA = json.load(ARQUIVO_DESCARGA)

            for FERROVIA in FERROVIAS_ATIVAS:
                json_DESCARGA["DESCARGAS"][FERROVIA] = {chave: valor for chave, valor in json_DESCARGA["DESCARGAS"][FERROVIA].items() if chave in FERROVIAS_ATIVAS[FERROVIA]}


            if not MARGEM in SAIDAS[DIA_LOGISTICO]["DESCARGAS"]:
                SAIDAS[DIA_LOGISTICO]["DESCARGAS"][MARGEM] = {}

            if not PATIO in SAIDAS[DIA_LOGISTICO]["DESCARGAS"][MARGEM]:   
                SAIDAS[DIA_LOGISTICO]["DESCARGAS"][MARGEM][PATIO] = []

            SAIDAS[DIA_LOGISTICO]["DESCARGAS"][MARGEM][PATIO].append(json_DESCARGA)
    
    return SAIDAS