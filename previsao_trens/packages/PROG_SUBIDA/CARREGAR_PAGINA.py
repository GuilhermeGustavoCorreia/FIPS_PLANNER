import pandas as pd
import json
import os
from previsao_trens.models  import TremVazio
from datetime               import datetime

def CARREGAR_PREVISAO_SUBIDA():

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    PERIODO_VIGENTE = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)

    HOJE = PERIODO_VIGENTE.loc[PERIODO_VIGENTE['NM_DIA'] == 'D', 'DATA_ARQ'].values[0]
    HOJE = datetime.strptime(HOJE, '%Y-%m-%d')
    MARGENS = ["DIREITA", "ESQUERDA"]
    
    TABELAS = {}
    for MARGEM in MARGENS:
        queryset = TremVazio.objects.filter(
                    previsao__year=HOJE.year,
                    previsao__month=HOJE.month,
                    previsao__day=HOJE.day,
                    margem=MARGEM
                ).order_by('previsao')
        if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
            TABELAS[MARGEM] = queryset

    return TABELAS
    
def CARREGAR_PROG_SUBIDA():

    TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
    
    DIRETORIO_TABELA_VAZIOS = "previsao_trens/src/OPERACAO/TABELAS_VAZIOS"
    
    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        INFOS_TERMINAIS = json.load(ARQUIVO_DESCARGA)

    with open(f"previsao_trens/src/OPERACAO/LINHAS.json") as ARQUIVO_LINHA:
        dict_LINHAS = json.load(ARQUIVO_LINHA)

    SAIDAS = {
        "D":{  
            "SATURACAO": {},
            "DESCARGAS": {},
            "LINHAS"   : {},
        }
        # , 
        # "D+1":{  
        #     "MARGENS": {},
        #     "DESCARGAS": {}
        # }
    
    #     "D+2":{  
    #         "MARGENS": {},
    #         "DESCARGAS": {}
    #     }
    }

    lst_TERMINAIS_ATIVOS = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    lst_LINHAS           = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()

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
            
            #INSERINDO A CHAVE SATURACAO_VAZIOS NO JSON
            for FERROVIA in json_DESCARGA["DESCARGAS"].keys():
                for PRODUTO in json_DESCARGA["DESCARGAS"][FERROVIA].keys():
                    json_DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["SATURACAO_VAZIO"] = INFOS_TERMINAIS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]

            SAIDAS[DIA_LOGISTICO]["DESCARGAS"][MARGEM][PATIO].append(json_DESCARGA)
            #A
            
    for LINHA in dict_LINHAS.keys():

        for DIA_LOGISTICO in SAIDAS.keys():

            DATA_ARQ = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO].iloc[0]['DATA_ARQ']

            with open(f"previsao_trens/src/OPERACAO/LINHAS_VAZIOS/{LINHA}/subida_{ DATA_ARQ }.json") as ARQUIVO_SUBIDA:
                json_SUBIDA = json.load(ARQUIVO_SUBIDA)


            #region REMOVENDO AS FERROVIAS DO VALONGO QUE NAO SAO UTILIZADAS
            
            if LINHA == "LINHA_VALONGO":
                del json_SUBIDA["FERROVIAS"]["MRS"]


            if LINHA == "LINHA_VALONGO_MRS":
                del json_SUBIDA["FERROVIAS"]["VLI"]
                del json_SUBIDA["FERROVIAS"]["RUMO"]

            #endregion

        SAIDAS[DIA_LOGISTICO]["LINHAS"][LINHA] = json_SUBIDA
    


    for DIA_LOGISTICO in SAIDAS.keys():

        DATA_ARQ = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO].iloc[0]['DATA_ARQ']
        with open(os.path.join(DIRETORIO_TABELA_VAZIOS, f'GERACAO_VAZIO_{DATA_ARQ}.json')) as ARQUIVO_SUBIDA:
                SAIDAS[DIA_LOGISTICO]["DESCARGAS"] = json.load(ARQUIVO_SUBIDA)
    
    return SAIDAS