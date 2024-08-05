import os
import pandas as pd
import json


def TRANSFORMAR_EM_HTML(ARQUIVO_DESCARGA):

    pass


def DESCARGA(TERMINAL, DATA_ARQ):

    pass


def DIA_COMPLETO(DIA_LOGISTICO):
    
    pass



def PAGINA_COMPLETA():

    

    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
    TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    RESTRICOES_ATIVAS = pd.read_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv", encoding='utf-8-sig', sep=';', index_col=0)

    def CARREGAR_CHEGADA_MARGENS(DATA_ARQ):

        #PARA OS CASOS QUE SE REPETEM CHEGADA NA MESMA HORA, SERA CONSIDERADO O PRIMIERO
        with open("previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
                DICT_TERMINAIS = json.load(ARQUIVO_DESCARGA)

        CHEGADAS = {
            "ESQUERDA" : [0]*24,    
            "DIREITA"  : [0]*24
        }

        for TERMINAL in lst_TERMINAIS_ATIVOS:

            INFOS_TERMINAL = DICT_TERMINAIS[TERMINAL]

            with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:
                DESCARGA = json.load(ARQUIVO_DESCARGA)

            TRENS_TERMINAL = [(i, valor) for i, valor in enumerate(DESCARGA["PREFIXO"]) if valor != 0]


            for TREM in TRENS_TERMINAL: 
              
                if CHEGADAS[INFOS_TERMINAL["MARGEM"]][TREM[0]] == 0:
                    CHEGADAS[INFOS_TERMINAL["MARGEM"]][TREM[0]] = TREM[1][0]

        
        return CHEGADAS

    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        TERMINAIS_INFOS = json.load(ARQUIVO_DESCARGA)
  
    lst_TERMINAIS_ATIVOS    = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    TERMINAIS_COM_RESTRICAO = RESTRICOES_ATIVAS[RESTRICOES_ATIVAS['RESTRICAO'] > 0].index.tolist()

    SAIDAS = {
        "HEADER":{
            "TERMINAIS": [],
            "DIAS_LOGISTICOS": []
            },
        "CONTEUDO":{
            "D"     :{  
                "MARGENS"   : {},
                "DESCARGAS" : []
            }, 
            "D+1"   :{  
                "MARGENS"   : {},
                "DESCARGAS" : []
            }, 
            "D+2"   :{  
                "MARGENS"   : {},
                "DESCARGAS" : []
            },
             "D+3"   :{  
                "MARGENS"   : {},
                "DESCARGAS" : []
            },
             "D+4"   :{  
                "MARGENS"   : {},
                "DESCARGAS" : []
            }
        }
    }

    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True) #ESTA COLUNA NAO SERÁ NECESSÁRIA E NOS ATRAPALHARÁ

    if len(lst_TERMINAIS_ATIVOS) == 0:
        
        return
    
    SAIDAS["HEADER"]["TERMINAIS"]       = json.dumps(lst_TERMINAIS_ATIVOS)
    SAIDAS["HEADER"]["DIAS_LOGISTICOS"] = json.dumps(list(SAIDAS["CONTEUDO"].keys()))

    for TERMINAL in lst_TERMINAIS_ATIVOS:

        DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
        DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]

        STATUS_RESTRICAO = TERMINAL in TERMINAIS_COM_RESTRICAO

        DESCARGAS_RESTRICOES    = RESTRICOES_ATIVAS.drop('RESTRICAO', axis=1)
        PRODUTO_RESTRICAO       = DESCARGAS_RESTRICOES.loc[TERMINAL][DESCARGAS_RESTRICOES.loc[TERMINAL] > 0].index.tolist()
        INFO_DO_TERMINAL        = TERMINAIS_INFOS[TERMINAL]
        
        FERROVIAS_ATIVAS = {
            "RUMO": [],
            "MRS" : [],
            "VLI" : []
        }

        for ATIVO in DESCARGAS_ATIVAS:

            for FERROVIA in FERROVIAS_ATIVAS:
                if ATIVO[0] == FERROVIA: FERROVIAS_ATIVAS[FERROVIA].append(ATIVO[1]) 
    

        for DIA in SAIDAS["CONTEUDO"].keys():

            DATA_ARQ = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA].iloc[0]['DATA_ARQ']
            
            SAIDAS["CONTEUDO"][DIA]["MARGENS"] = CARREGAR_CHEGADA_MARGENS(DATA_ARQ)
           
            with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:

                json_DESCARGA = json.load(ARQUIVO_DESCARGA)
                json_DESCARGA["POSSUI_RESTRICAO"] = STATUS_RESTRICAO
                
                #É PARA PEGAR UMA RESTRICAO
                FERROVIA_ALEATORA_DO_TERMINAL = next(iter(json_DESCARGA["DESCARGAS"]))

                if STATUS_RESTRICAO: 
                    json_DESCARGA["RESTRICAO_PCT"] = json_DESCARGA["DESCARGAS"][FERROVIA_ALEATORA_DO_TERMINAL][PRODUTO_RESTRICAO[0]]["RESTRICAO"]
                
                #APENAS COLOCA NA DESCARGA A INFORMACAO DO QUE ESTA ATIVO NO TERMINAL (FERROVIA E PRODUTO)
                for FERROVIA in FERROVIAS_ATIVAS:
                    json_DESCARGA["DESCARGAS"][FERROVIA] = {chave: valor for chave, valor in json_DESCARGA["DESCARGAS"][FERROVIA].items() if chave in FERROVIAS_ATIVAS[FERROVIA]}
                
                json_DESCARGA["DESCARGAS_ATIVAS"] = FERROVIAS_ATIVAS
                SAIDAS["CONTEUDO"][DIA]["DESCARGAS"].append(json_DESCARGA)


                #INSERE O VALOR DA PRODUTIVIDADE (POIS ELE VEM DE OUTRA TABELA)
                for FERROVIA in json_DESCARGA["DESCARGAS"]:
                    for PRODUTO in json_DESCARGA["DESCARGAS"][FERROVIA]:
                        json_DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PRODUTIVIDADE"] = INFO_DO_TERMINAL["PRODUTIVIDADE"][FERROVIA][PRODUTO]


    return SAIDAS

