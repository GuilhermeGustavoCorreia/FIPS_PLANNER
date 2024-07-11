import pandas as pd
import json
import copy

def CARREGAR_RELATORIO_DETALHE():


    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
    TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    lst_TERMINAIS_ATIVOS  = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)    
    
    #ESTOU REMOVENDO O D-1 DO CÁLCULO PARA VER NO QUE VAI DAR
    PERIODO_VIGENTE = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0]) 
    LISTA_DATA_ARQ  = PERIODO_VIGENTE["DATA_ARQ"].tolist()
    
    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        INFOS = json.load(ARQUIVO_DESCARGA)

    RELATORIO_DETALHE = {

        "PRINCIPAL":    {},
        "RUMO":         {}
    }

    #OBTENDO OS VALORES DA DETALHADA
    for TERMINAL in lst_TERMINAIS_ATIVOS:  #CADA TERMINAL
        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL] = {}

        MARGEM = "PCZ"
        if INFOS[TERMINAL]["MARGEM"] == "DIREITA": MARGEM = "PSN"
        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MARGEM"] = MARGEM

        DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()   

        for DESCARGAS in DESCARGAS_ATIVAS: #CADA DESCARGA

            FERROVIA, PRODUTO = DESCARGAS.split("_")

            if not FERROVIA in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]:
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA] = {}

            if not PRODUTO in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA]:   
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO] = {}

            for DIA_LOGISTICO, DATA_ARQ in enumerate(LISTA_DATA_ARQ): #CADA DIA
                
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO] = {}
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"] = {}
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"] = {} 
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["SALDOS"] = {}
                
                with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:
                    DESCARGA = json.load(ARQUIVO_DESCARGA)

                try: #['SALDO_DE_VIRADA_VAZIOS', 'SALDO_DE_VIRADA', 'PRODUTIVIDADE', 'RECEBIMENTOS', 'PEDRA']

                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["SALDOS"]["P1"] = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"]

                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"]["P1"]  = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][0]
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"]["P2"]  = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][1]
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"]["P3"]  = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][2]
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"]["P4"]  = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][3]

                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"]["P1"] = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][0]
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"]["P2"] = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][1]
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"]["P3"] = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][2]        
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"]["P4"] = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][3]

                    for i in range(2, 5):
                        
                        REC = RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"][f"P{i-1}"]
                        PD  = RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"][f"P{i-1}"]
                        SD  = RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["SALDOS"][f"P{i-1}"] 

                        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["SALDOS"][f"P{i}"] =    REC + SD - PD


                    TOTAL_PEDRA  = 0
                    TOTAL_OFERTA = 0

                    for i in range (1, 5):
                    

                        TOTAL_PEDRA  = TOTAL_PEDRA  + RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["PEDRA"][f"P{i}"]
                        TOTAL_OFERTA = TOTAL_OFERTA + RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["RECEBIMENTOS"][f"P{i}"]
                    

                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["TT_OF"] = TOTAL_OFERTA + RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["SALDOS"]["P1"]  
                    RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["TT_PD"] = TOTAL_PEDRA
    
                except: 
                        pass
    

    #AJUSTANDO OS TERMINAIS DE ACUCAR
    TERMINAIS_ACUCAR = []

    TERMINAIS_DO_RELATORIO = list(RELATORIO_DETALHE["PRINCIPAL"].keys())

    for TERMINAL in TERMINAIS_DO_RELATORIO:
        
        try:
            TERMINAL_ORIGINAL = TERMINAL.split(" ")[0]

            if TERMINAL.split(" ")[1] == "ACUCAR":
                TERMINAIS_ACUCAR.append(TERMINAL) 
                for FERROVIA in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]:
                    if FERROVIA != "MARGEM":
                        if not TERMINAL_ORIGINAL in RELATORIO_DETALHE["PRINCIPAL"]:
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL_ORIGINAL] = {}

                        if not FERROVIA in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL_ORIGINAL]:
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL_ORIGINAL][FERROVIA] = {} 

                        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL_ORIGINAL][FERROVIA]["ACUCAR"] = RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA]["ACUCAR"]  


                MARGEM = "PCZ"
                if INFOS[TERMINAL]["MARGEM"] == "DIREITA": MARGEM = "PSN"
                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL_ORIGINAL]["MARGEM"] = MARGEM
        except:
            pass

    #EXCLUINDO TERMINAIS DE ACUCAR
    for TERMINAL in TERMINAIS_ACUCAR:

        del RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]
    
    for TERMINAL in RELATORIO_DETALHE["PRINCIPAL"].keys():
 
        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"] = {}

        for FERROVIA in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]:

            if FERROVIA != "TOTAL" and FERROVIA != "MARGEM":

                for PRODUTO in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA]:

                    for DIA_LOGISTICO, DATA_ARQ in enumerate(LISTA_DATA_ARQ):

                        if not DIA_LOGISTICO in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"]:
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO] = {}

                        COLUNAS = ["SALDOS", "RECEBIMENTOS", "PEDRA"]
                        
                        for COLUNA in COLUNAS:
                            
                            if not COLUNA in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]:

                                RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO][COLUNA] = {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
                                                      
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO][COLUNA]["P1"]
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO][COLUNA]["P2"]
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO][COLUNA]["P3"]
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO][COLUNA]["P4"]
                
                        if not "TT_OF" in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]:
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]["TT_OF"] = 0

                        if not "TT_PD" in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]:
                            RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]["TT_PD"] = 0

                        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]["TT_OF"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["TT_OF"]
                        RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["TOTAL"][DIA_LOGISTICO]["TT_PD"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL][FERROVIA][PRODUTO][DIA_LOGISTICO]["TT_PD"] 


    #OBTENDO OS TOTAIS DE GRÃOS (RUMO, MRS E VLI)

    #[RELATORIO] [RUMO] [MRS] [VLI] [RUMO GRAOS]    


    LINHA_DETALHE = {  
        0: {
            'RECEBIMENTOS'	: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'PEDRA'			: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'SALDOS'		: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'TT_OF'			: 0, 
            'TT_PD'			: 0
        }, 
        1: {
            'RECEBIMENTOS'	: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'PEDRA'			: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'SALDOS'		: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'TT_OF'			: 0, 
            'TT_PD'			: 0
        }, 
        2: {
            'RECEBIMENTOS'	: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'PEDRA'			: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0},
            'SALDOS'		: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'TT_OF'			: 0, 
            'TT_PD'			: 0
        }, 
        3: {
            'RECEBIMENTOS'	: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'PEDRA'			: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'SALDOS'		: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'TT_OF'			: 0,
            'TT_PD'			: 0
        }, 
        4: {
            'RECEBIMENTOS'	: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'PEDRA'			: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'SALDOS'		: {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0}, 
            'TT_OF'			: 0,
            'TT_PD'		    : 0
        }
    }
    
    TOTAIS = {
        "RUMO" :{
            "GRAOS":  {
                "PCZ"           : copy.deepcopy(LINHA_DETALHE), 
                "PSN"           : copy.deepcopy(LINHA_DETALHE), 
                "TOTAL_GRAO"    : copy.deepcopy(LINHA_DETALHE)
            }, 
            "ACUCAR":  {
                "PCZ"           : copy.deepcopy(LINHA_DETALHE), 
                "PSN"           : copy.deepcopy(LINHA_DETALHE), 
                "TOTAL_ACUCAR"  : copy.deepcopy(LINHA_DETALHE), 
            },
            "RESUMO_GRAOS": {
                "FARELO"        : copy.deepcopy(LINHA_DETALHE), 
                "SOJA"          : copy.deepcopy(LINHA_DETALHE), 
                "MILHO"         : copy.deepcopy(LINHA_DETALHE)
            },
            "TOTAO_GRAO_ACUCAR" : copy.deepcopy(LINHA_DETALHE)
        },
        "TOTAIS": {
            "GRAO_ACUCAR"       : copy.deepcopy(LINHA_DETALHE),
            "GERAL"             : copy.deepcopy(LINHA_DETALHE),
            "PSN"               : copy.deepcopy(LINHA_DETALHE),
            "PCZ"               : copy.deepcopy(LINHA_DETALHE)
        }
    }
          


    #CRIANDO OS TOTAIS DA RUMO

    #OS CALCULOS ABAIXO MNÃO SAO COMPLEXOS, OS SEPAREI POR SOMAS DE LINHAS, ALGUNS FOR´S TEM MAIS BLOCOS DE SOMA QUE OUTROS POIS PARTICIPAM DE MAIS TOTAIS
    #SEPAREI AS FERROVIAS EM IF´s DIFERENTES, POIS CADA TABELA DE FERRPVOA POSSUI LINHAS DIFERENTES
    COLUNAS         = ["RECEBIMENTOS", "SALDOS", "PEDRA"]
    FERTILIZANTES   = ["KCL", "UREIA", "OUTROS"]
    GRAOS           = ["FARELO", "SOJA", "MILHO"]

    for TERMINAL in RELATORIO_DETALHE["PRINCIPAL"].keys():   
        
        MARGEM = RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MARGEM"]
        
        if "RUMO" in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]: 

            for PRODUTO in list(RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"].keys()):
                
                if PRODUTO in GRAOS:

                    for i in range(5):
                        for COLUNA in COLUNAS:
                                                                          
                            TOTAIS["RUMO"]["GRAOS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["GRAOS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["GRAOS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["GRAOS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL
                            TOTAIS["RUMO"]["GRAOS"]["TOTAL_GRAO"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["GRAOS"]["TOTAL_GRAO"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["GRAOS"]["TOTAL_GRAO"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["GRAOS"]["TOTAL_GRAO"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA RUMO TOTAL GRAO + ACUCAR
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]


                            #LINHA TOTAIS GRAOS RUMO
                            TOTAIS["RUMO"]["RESUMO_GRAOS"][PRODUTO][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["RESUMO_GRAOS"][PRODUTO][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["RESUMO_GRAOS"][PRODUTO][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["RESUMO_GRAOS"][PRODUTO][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]
      
                if PRODUTO == "ACUCAR":

                    for i in range(5):
                        for COLUNA in COLUNAS:
                            
                            TOTAIS["RUMO"]["ACUCAR"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["ACUCAR"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["ACUCAR"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["ACUCAR"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL
                            TOTAIS["RUMO"]["ACUCAR"]["TOTAL_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["ACUCAR"]["TOTAL_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["ACUCAR"]["TOTAL_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["ACUCAR"]["TOTAL_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRAO + ACUCAR
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]
                
                if PRODUTO == "CELULOSE" and MARGEM == "PSN":

                    if not "CELULOSE" in TOTAIS["RUMO"]: 
                        TOTAIS["RUMO"]["CELULOSE"] = {"PSN": copy.deepcopy(LINHA_DETALHE), "TOTAL_CELULOSE": copy.deepcopy(LINHA_DETALHE)}


                    for i in range(5):
                        for COLUNA in COLUNAS:
                            
                            TOTAIS["RUMO"]["CELULOSE"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["CELULOSE"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["CELULOSE"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["CELULOSE"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL
                            TOTAIS["RUMO"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["RUMO"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["RUMO"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["RUMO"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]
                            
                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]
                
                if PRODUTO in FERTILIZANTES:
                    for i in range(5):

                        for COLUNA in COLUNAS:
 
                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]
                            
                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["RUMO"][PRODUTO][i][COLUNA]["P4"]


        if "VLI" in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]:

            if not "VLI" in TOTAIS: 

                TOTAIS["VLI"] = {}
                TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"] = copy.deepcopy(LINHA_DETALHE)
        
            for PRODUTO in list(RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"].keys()):
                
                if PRODUTO in GRAOS:

                    if not "GRAOS"  in TOTAIS["VLI"]:           TOTAIS["VLI"]["GRAOS"] = {}
                    if not MARGEM   in TOTAIS["VLI"]["GRAOS"]:  TOTAIS["VLI"]["GRAOS"][MARGEM] = copy.deepcopy(LINHA_DETALHE)

                    for i in range(5):
                        for COLUNA in COLUNAS:
                                                                            
                            TOTAIS["VLI"]["GRAOS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["VLI"]["GRAOS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["VLI"]["GRAOS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["VLI"]["GRAOS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRAO + ACUCAR
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                if PRODUTO == "ACUCAR":
                     
                    if not "ACUCAR" in TOTAIS["VLI"]:               TOTAIS["VLI"]["ACUCAR"] = {}
                    if not MARGEM   in TOTAIS["VLI"]["ACUCAR"]:     TOTAIS["VLI"]["ACUCAR"][MARGEM] = copy.deepcopy(LINHA_DETALHE)

                    for i in range(5):
                        for COLUNA in COLUNAS:

                            TOTAIS["VLI"]["ACUCAR"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["VLI"]["ACUCAR"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["VLI"]["ACUCAR"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["VLI"]["ACUCAR"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL VLI GRAO + ACUCAR
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]
                    
                if PRODUTO in FERTILIZANTES:
                    for i in range(5):

                        for COLUNA in COLUNAS:
                            
                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]
                            
                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["VLI"][PRODUTO][i][COLUNA]["P4"]


        if "MRS" in RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]:

            if not "MRS" in TOTAIS: 

                TOTAIS["MRS"] = {}
                TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"] = copy.deepcopy(LINHA_DETALHE)


            for PRODUTO in list(RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"].keys()):

                if PRODUTO in GRAOS:

                    if not "GRAOS"  in TOTAIS["MRS"]:           TOTAIS["MRS"]["GRAOS"] = {}
                    if not MARGEM   in TOTAIS["MRS"]["GRAOS"]:  TOTAIS["MRS"]["GRAOS"][MARGEM] = copy.deepcopy(LINHA_DETALHE)

                    for i in range(5):
                        for COLUNA in COLUNAS:
                                                                            
                            TOTAIS["MRS"]["GRAOS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["GRAOS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["GRAOS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["GRAOS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRAO + ACUCAR
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]


                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]
                
                if PRODUTO == "ACUCAR":
                     
                    if not "ACUCAR" in TOTAIS["MRS"]:               TOTAIS["MRS"]["ACUCAR"] = {}
                    if not MARGEM   in TOTAIS["MRS"]["ACUCAR"]:     TOTAIS["MRS"]["ACUCAR"][MARGEM] = copy.deepcopy(LINHA_DETALHE)

                    for i in range(5):
                        for COLUNA in COLUNAS:

                            TOTAIS["MRS"]["ACUCAR"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["ACUCAR"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["ACUCAR"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["ACUCAR"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRAO + ACUCAR
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRÃO + AÇÚCAR
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GRAO_ACUCAR"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]
                            
                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                if PRODUTO == "CELULOSE" and MARGEM == "PSN":

                    if not "CELULOSE" in TOTAIS["MRS"]: 
                        TOTAIS["MRS"]["CELULOSE"] = {"PSN": copy.deepcopy(LINHA_DETALHE), "TOTAL_CELULOSE": copy.deepcopy(LINHA_DETALHE)}


                    for i in range(5):
                        for COLUNA in COLUNAS:
                            
                            TOTAIS["MRS"]["CELULOSE"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["CELULOSE"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["CELULOSE"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["CELULOSE"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL
                            TOTAIS["MRS"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["CELULOSE"]["TOTAL_CELULOSE"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                if PRODUTO == "CONTEINER":
                     
                    if not "CONTEINER" in TOTAIS["MRS"]:               TOTAIS["MRS"]["CONTEINER"] = {"TOTAL_CONTEINER": copy.deepcopy(LINHA_DETALHE)}
                    if not MARGEM   in TOTAIS["MRS"]["CONTEINER"]:     TOTAIS["MRS"]["CONTEINER"][MARGEM] = copy.deepcopy(LINHA_DETALHE)

                    for i in range(5):
                        for COLUNA in COLUNAS:

                            TOTAIS["MRS"]["CONTEINER"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["CONTEINER"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["CONTEINER"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["CONTEINER"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GRAO + CONTEINER
                            TOTAIS["MRS"]["CONTEINER"]["TOTAL_CONTEINER"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["MRS"]["CONTEINER"]["TOTAL_CONTEINER"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["MRS"]["CONTEINER"]["TOTAL_CONTEINER"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["MRS"]["CONTEINER"]["TOTAL_CONTEINER"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]

                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]
                
                if PRODUTO in FERTILIZANTES:
                    for i in range(5):
                        for COLUNA in COLUNAS:
                            
                            #LINHA TOTAL MARGENS
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"][MARGEM][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]
                            
                            #LINHA TOTAL GERAL FERROVIAS
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P1"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P1"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P2"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P2"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P3"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P3"]
                            TOTAIS["TOTAIS"]["GERAL"][i][COLUNA]["P4"] += RELATORIO_DETALHE["PRINCIPAL"][TERMINAL]["MRS"][PRODUTO][i][COLUNA]["P4"]


    #calculando os TOTAIS PD E O OF

    # TOTAIS = {
    #     "RUMO" :{
    #         "GRAOS":  {
    #             "PCZ"           : copy.deepcopy(LINHA_DETALHE), 
    #             "PSN"           : copy.deepcopy(LINHA_DETALHE), 
    #             "TOTAL_GRAO"    : copy.deepcopy(LINHA_DETALHE)
    #         }, 
    #         "ACUCAR":  {
    #             "PCZ"           : copy.deepcopy(LINHA_DETALHE), 
    #             "PSN"           : copy.deepcopy(LINHA_DETALHE), 
    #             "TOTAL_ACUCAR"  : copy.deepcopy(LINHA_DETALHE), 
    #         },
    #         "RESUMO_GRAOS": {
    #             "FARELO"        : copy.deepcopy(LINHA_DETALHE), 
    #             "SOJA"          : copy.deepcopy(LINHA_DETALHE), 
    #             "MILHO"         : copy.deepcopy(LINHA_DETALHE)
    #         },
    #         "TOTAO_GRAO_ACUCAR" : copy.deepcopy(LINHA_DETALHE)
    #     },
    #     "TOTAIS": {
    #         "GRAO_ACUCAR"       : copy.deepcopy(LINHA_DETALHE),
    #         "GERAL"             : copy.deepcopy(LINHA_DETALHE),
    #         "PSN"               : copy.deepcopy(LINHA_DETALHE),
    #         "PCZ"               : copy.deepcopy(LINHA_DETALHE)
    #     }
 
    #region TOTAIS DOS RESUMOS

    #region CALCULANDO OS TOTAIS DO RESUMO RUMO GRAOS
    for LINHA_RELATORIO in list(TOTAIS["RUMO"]["GRAOS"]):
    
        for i in range(5):
            TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
            TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] = 0
            
            for J in range(1, 5):
                TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["RUMO"]["GRAOS"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
    #endregion

    #region CALCULANDO OS TOTAIS DO RESUMO RUMO ACUCAR
    for LINHA_RELATORIO in list(TOTAIS["RUMO"]["ACUCAR"]):
    
        for i in range(5):
            TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
            TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] = 0
            
            for J in range(1, 5):
                TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["RUMO"]["ACUCAR"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
    #endregion

    #region CALCULANDO OS TOTAIS DO RESUMO RUMO GRÃO + ACUCAR
    for i in range(5):
        TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] = TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["SALDOS"]["P1"]
        TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] = 0
        
        for J in range(1, 5):
            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] += TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["RECEBIMENTOS"][f"P{J}"]
            TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] += TOTAIS["RUMO"]["TOTAO_GRAO_ACUCAR"][i]["PEDRA"][f"P{J}"]
    #endregion

    #region CALCULANDO OS TOTAIS DO RESUMO RUMO GRAOS
    for LINHA_RELATORIO in list(TOTAIS["RUMO"]["RESUMO_GRAOS"]):
    
        for i in range(5):
            TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
            TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["TT_PD"] = 0
            
            for J in range(1, 5):
                TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["RUMO"]["RESUMO_GRAOS"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
    #endregion


    if "VLI" in TOTAIS:

        #region CALCULANDO OS TOTAIS DO RESUMO VLI GRAOS
        if "GRAOS" in TOTAIS["VLI"]:
            for LINHA_RELATORIO in list(TOTAIS["VLI"]["GRAOS"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
            
                for i in range(5):
                    TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["VLI"]["GRAOS"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion

        #region CALCULANDO OS TOTAIS DO RESUMO VLI ACUCAR
        if "ACUCAR" in TOTAIS["VLI"]:
            for LINHA_RELATORIO in list(TOTAIS["VLI"]["ACUCAR"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
            
                for i in range(5):
                    TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["VLI"]["ACUCAR"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion

        #region CALCULANDO OS TOTAIS DO RESUMO VLI TOTAL
        if "TOTAO_GRAO_ACUCAR" in TOTAIS["VLI"]:
            for LINHA_RELATORIO in list(TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
            
                for i in range(5):
                    TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] = TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["SALDOS"]["P1"]
                    TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] += TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] += TOTAIS["VLI"]["TOTAO_GRAO_ACUCAR"][i]["PEDRA"][f"P{J}"]
        #endregion

    if "MRS" in TOTAIS:   

        #region CALCULANDO OS TOTAIS DO RESUMO MRS GRAOS
        if "GRAOS" in TOTAIS["MRS"]:
            for LINHA_RELATORIO in list(TOTAIS["MRS"]["GRAOS"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
            
                for i in range(5):
                    TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["MRS"]["GRAOS"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion 

        #region CALCULANDO OS TOTAIS DO RESUMO MRS ACUCAR
        if "ACUCAR" in TOTAIS["MRS"]:
            for LINHA_RELATORIO in list(TOTAIS["MRS"]["ACUCAR"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
            
                for i in range(5):
                    TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["MRS"]["ACUCAR"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion

        #region CALCULANDO OS TOTAIS DO RESUMO MRS TOTAL
        if "TOTAO_GRAO_ACUCAR" in TOTAIS["MRS"]:
                for LINHA_RELATORIO in list(TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"]): #MARGENS DO PRODUTO PCX OU PSN GRAOS
                
                    for i in range(5):
                        TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] = TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["SALDOS"]["P1"]
                        TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] = 0
                        
                        for J in range(1, 5):
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["TT_OF"] += TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["RECEBIMENTOS"][f"P{J}"]
                            TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["TT_PD"] += TOTAIS["MRS"]["TOTAO_GRAO_ACUCAR"][i]["PEDRA"][f"P{J}"]
        #endregion

        #region CALCULANDO OS TOTAIS DO RESUMO MRS CELULOSE
        if "CELULOSE" in TOTAIS["MRS"]:
            for LINHA_RELATORIO in list(TOTAIS["MRS"]["CELULOSE"]): #MARGENS DO PRODUTO PCX OU PSN CELULOSE
            
                for i in range(5):
                    TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["MRS"]["CELULOSE"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion 

        #region CALCULANDO OS TOTAIS DO RESUMO MRS CONTEINER
        if "CONTEINER" in TOTAIS["MRS"]:
            for LINHA_RELATORIO in list(TOTAIS["MRS"]["CONTEINER"]): #MARGENS DO PRODUTO PCX OU PSN CONTEINER
            
                for i in range(5):
                    TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
                    TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["TT_PD"] = 0
                    
                    for J in range(1, 5):
                        TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                        TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["MRS"]["CONTEINER"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
        #endregion

    #region CALCULANDO OS TOTAIS GERAIS
    for LINHA_RELATORIO in list(TOTAIS["TOTAIS"]):
    
        for i in range(5):
            TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["TT_OF"] = TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["SALDOS"]["P1"]
            TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["TT_PD"] = 0
            
            for J in range(1, 5):
                TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["TT_OF"] += TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["RECEBIMENTOS"][f"P{J}"]
                TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["TT_PD"] += TOTAIS["TOTAIS"][LINHA_RELATORIO][i]["PEDRA"][f"P{J}"]
    #endregion




    #endregion

    RELATORIO_DETALHE["RUMO"]   = TOTAIS
    RELATORIO_DETALHE["TOTAIS"] = TOTAIS["TOTAIS"]
    if "VLI" in TOTAIS: RELATORIO_DETALHE["VLI"]    = TOTAIS["VLI"]
    if "MRS" in TOTAIS: RELATORIO_DETALHE["MRS"]    = TOTAIS["MRS"]
   

    return RELATORIO_DETALHE 