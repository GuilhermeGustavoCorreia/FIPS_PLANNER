import json
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
from django.conf import settings

def ATUALIZAR_DESCARGA():

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    PATH_MODELO_DESCARGA = "previsao_trens/src/DICIONARIOS/MODELO_DESCARGA.json"
    DIRETORIO_DESCARGAS  =  "previsao_trens/src/DESCARGAS"

    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        dict_TERMINAIS = json.load(ARQUIVO_DESCARGA)


    #ATUALIZAR PERIODO VIGENTE
    PERIODO_VIGENTE = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    PERIODO_VIGENTE['DATA_ARQ'] = PERIODO_VIGENTE['DIA_LOGISTICO'].apply(lambda x: (datetime.now() + timedelta(days=x)).strftime("%Y-%m-%d"))
    PERIODO_VIGENTE.to_csv(PATH_PERIODO_VIGENTE, sep=";")
    
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()
    ARQUIVOS_ATUALIZADOS = [f'descarga_{data}.json' for data in LISTA_DATA_ARQ]
    #ATUALIZANDO AS DESCARGAS

    #VAMOS COPIAR O MODELO DE DESCARGA
    with open(PATH_MODELO_DESCARGA) as ARQUIVO_DESCARGA:
        MODELO_DESCARGA = json.load(ARQUIVO_DESCARGA)

    #REMOVER A DESCARGA
    
    UMA_DESCARGA = MODELO_DESCARGA["DESCARGAS"]["FERROVIA"]["PRODUTO"]

    del MODELO_DESCARGA["DESCARGAS"]["FERROVIA"]

    #INSERIR EM CADA DERMINAL CONFOME SUAS DESCARGAS
    for TERMINAL in dict_TERMINAIS:
        DESCARGA_TERMINAL = {}
        DESCARGA_TERMINAL = MODELO_DESCARGA

        for FERROVIA in dict_TERMINAIS[TERMINAL]["FERROVIA"]:
            DESCARGA_TERMINAL["DESCARGAS"][FERROVIA] = {}

            for PRODUTO in dict_TERMINAIS[TERMINAL]["PRODUTOS"]:                          
                DESCARGA_TERMINAL["DESCARGAS"][FERROVIA][PRODUTO] = UMA_DESCARGA


            
        DIRETORIO_TERMINAL = f'{DIRETORIO_DESCARGAS}\{TERMINAL}'            
        if not os.path.exists(DIRETORIO_TERMINAL):
            os.mkdir(DIRETORIO_TERMINAL)

        DESCARGAS_NA_PASTA_DO_TEMRINAL = (os.listdir(DIRETORIO_TERMINAL))

        for ARQUIVO in DESCARGAS_NA_PASTA_DO_TEMRINAL:
            if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   

                ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_TERMINAL, ARQUIVO)
                os.remove(ARQUIVO_EXCEDENTE)  

        for ARQUIVO in ARQUIVOS_ATUALIZADOS:
            if ARQUIVO not in DESCARGAS_NA_PASTA_DO_TEMRINAL:

                DESCARGA_TERMINAL["TERMINAL"] = TERMINAL
                DESCARGA_TERMINAL["DATA"]     = ARQUIVO.split("_")[1].split(".")[0]
            
                with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
                    json.dump(DESCARGA_TERMINAL, ARQUIVO_NOME)





                     
