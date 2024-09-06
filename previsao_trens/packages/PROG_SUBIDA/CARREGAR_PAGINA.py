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
        # queryset = TremVazio.objects.filter(
        #             previsao__year=HOJE.year,
        #             previsao__month=HOJE.month,
        #             previsao__day=HOJE.day,
        #             margem=MARGEM
        #         ).order_by('previsao')
        queryset = TremVazio.objects
        if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
            TABELAS[MARGEM] = queryset

    return TremVazio.objects.all() #TABELAS
    
def CARREGAR_PROG_SUBIDA_OLD():

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

def CARREGAR_PROG_SUBIDA():

    SAIDA = {
        "D": {
            "DATA_ARQ": "",
            "LINHA_4K": "",
            "TERMINAIS": {

                "PCX": [],
                "PCZ": [],
                "PST": [],
                "PMC": []
            },
            "BUFFER":      {},
            "CONDENSADOS": {}
        },
        "D1": {
            "DATA_ARQ": "",
            "LINHA_4K": "",
            "TERMINAIS": {

                "PCX": [],
                "PCZ": [],
                "PST": [],
                "PMC": []
            },
            "BUFFER":      {},
            "CONDENSADOS": {}
        }

    }

    TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/SUBIDA/PARAMETROS/TERMINAIS_ATIVOS.csv",    encoding='utf-8-sig', sep=';', index_col=0)
    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",            encoding='utf-8-sig', sep=';', index_col=0)
    
    lst_TERMINAIS_ATIVOS = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)
    

    with open(f"previsao_trens/src/SUBIDA/PARAMETROS/TERMINAIS_ESPECIAIS.json") as ARQUIVO:
        TERMINAIS_ESPECIAIS = json.load(ARQUIVO)

    TERMINAIS_ADAPTADOS = (os.listdir("previsao_trens/src/SUBIDA/TERMINAIS_ADAPTADOS"))
    
    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO:
        INFOS_TERMINAIS = json.load(ARQUIVO)


    with open(f"previsao_trens/src/SUBIDA/PARAMETROS/LINHAS.json") as ARQUIVO:
        INFOS_LINHAS = json.load(ARQUIVO)
    
    #TERMINAIS_DESCONDIDERADOS = TERMINAIS_ESPECIAIS["DESCONSIDERAR"]["VIZUALICACAO"]
    #lst_TERMINAIS_ATIVOS = [item for item in lst_TERMINAIS_ATIVOS if item not in TERMINAIS_DESCONDIDERADOS]
    
    DIAS_LOGISTICOS = ["D", "D+1"]
    CHAVES          = ["D", "D1"]
    
    for i, DIA_LOGISTICO in enumerate(DIAS_LOGISTICOS):
        
       
        PERIODO_VIGENTE = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
        DATA_ARQ        = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO].iloc[0]['DATA_ARQ']
        
        SAIDA[CHAVES[i]]["DATA_ARQ"] = DATA_ARQ
        print(DATA_ARQ)
        
        #region ABRINDO TERMINAIS   [rgb(255,77,197, 0.1)]
        for TERMINAL in lst_TERMINAIS_ATIVOS:
            
            FERROVIAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
           
            
            with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{ TERMINAL }/subida_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:
                jsSUBIDA = json.load(ARQUIVO_DESCARGA)

            PATIO = jsSUBIDA["PATIO"]
            #APENAS COLOCA NA DESCARGA A INFORMACAO DO QUE ESTA ATIVO NO TERMINAL (FERROVIA E PRODUTO)        
            jsSUBIDA["SUBIDA"] = {chave: valor for chave, valor in jsSUBIDA["SUBIDA"].items() if chave in FERROVIAS_ATIVAS}
            
            FERROVIAS = list(jsSUBIDA["SUBIDA"].keys())

            #region INSERINDO MIN E MAX  [rgb(255,77,197, 0.2)]
            for FERROVIA in FERROVIAS:

                SEGMENTOS = list(jsSUBIDA["SUBIDA"][FERROVIA].keys())
                for SEGMENTO in SEGMENTOS:
                    
                    if TERMINAL in TERMINAIS_ADAPTADOS:
                        
                        

                        #region TERMINAIS ESPECIAIS [rgb(255,77,197, 0.3)]
                        for ITEM in TERMINAIS_ESPECIAIS:
                            
                            if not (ITEM == "REMOVER" or ITEM == "DESCONSIDERAR"):

                                for TERMINAL_ESPECIAL in TERMINAIS_ESPECIAIS[ITEM]:

                                    if TERMINAL_ESPECIAL == TERMINAL:

                                        jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["SATURACAO_VAZIO"]["MIN"] = TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL_ESPECIAL]["SAIDA"]["SATURACAO_VAZIO"][FERROVIA]["MIN"]
                                        jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["SATURACAO_VAZIO"]["MAX"] = TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL_ESPECIAL]["SAIDA"]["SATURACAO_VAZIO"][FERROVIA]["MAX"]

                        #endregion

                    else:    
                        
                        jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["SATURACAO_VAZIO"]["MIN"] = INFOS_TERMINAIS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MIN"]
                        jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["SATURACAO_VAZIO"]["MAX"] = INFOS_TERMINAIS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MAX"]


            #endregion
            
            SAIDA[CHAVES[i]]["TERMINAIS"][PATIO].append(jsSUBIDA)  
        #endregion 

        #region ABRINDO CONDENSADOS [rgb(255,77,197, 0.2)]
        
        with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{DATA_ARQ}.json") as ARQUIVO:
                jsCONDENSADO = json.load(ARQUIVO)
        
        SAIDA[CHAVES[i]]["CONDENSADOS"] = jsCONDENSADO

        #endregion 

        #region ABRINDO LINHA 4K    [rgb(255,77,197, 0.2)]

        with open(f"previsao_trens/src/SUBIDA/LINHAS/LINHA_4K/linha_4k_{DATA_ARQ}.json") as ARQUIVO:
                jsLINHA_4K = json.load(ARQUIVO)
        
        SEGMENTOS = INFOS_LINHAS["LINHA_4K"]["SEGMENTOS"]
        for SEGMENTO in SEGMENTOS:
            for FERROVIA in INFOS_LINHAS["LINHA_4K"]["FERROVIAS"]:
                jsLINHA_4K["SUBIDA"][FERROVIA][SEGMENTO]["SATURACAO_VAZIO"] = INFOS_LINHAS["LINHA_4K"]["SATURACAO_VAZIO"][FERROVIA]

        SAIDA[CHAVES[i]]["LINHA_4K"] = jsLINHA_4K

        #endregion

        #region ABRINDO BUFFER      [rgb(255,77,197, 0.2)]

        with open(f"previsao_trens/src/SUBIDA/BUFFER/buffer_{DATA_ARQ}.json") as ARQUIVO:
                jsCONDENSADO = json.load(ARQUIVO)

        SAIDA[CHAVES[i]]["BUFFER"] = jsCONDENSADO
        #endregion

    return SAIDA