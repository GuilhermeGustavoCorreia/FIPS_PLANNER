import json
import pandas as pd


def CARREGAR_RELATORIO_OCUPACAO():

    
    SAIDAS = {
        "D"     : {

                    }, 
        "D1"   : {
            
        }, 
        "D2"   : {
            
        }
    }

    DIAS_LOGISTICOS = ["D", "D+1", "D+2"]

    #region ARQUIVOS NECESSÁRIOS [TERMINAIS_ATIVOS, PERIODO_VIGENTE, INFOS_TERMINAIS]
    PATH_TERMINAIS_ATIVOS = "previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv"
    PATH_PERIODO_VIGENTE  = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    PATH_DICT_TERMINAIS   = "previsao_trens/src/DICIONARIOS/TERMINAIS.json"

    TERMINAIS_ATIVOS        = pd.read_csv(PATH_TERMINAIS_ATIVOS,  encoding='utf-8-sig', sep=';', index_col=0)
    lst_TERMINAIS_ATIVOS    = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)  

    PERIODO_VIGENTE   = pd.read_csv(PATH_PERIODO_VIGENTE,   encoding='utf-8-sig', sep=';', index_col=0)

    with open(PATH_DICT_TERMINAIS) as ARQUIVO_DESCARGA:
        INFOS = json.load(ARQUIVO_DESCARGA)
    #endregion


    for i, DIA in enumerate(SAIDAS.keys()):

        #region DEFININDO O DATA_ARQ
        LINHA       = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIAS_LOGISTICOS[i]]
        DATA_ARQ    = LINHA['DATA_ARQ'].values[0]
        #endregion

        SAIDAS[DIA] = {
            "PSN": {}, 
            "PCZ": {}, 
            "TOTAIS"       : {"PLANO":{"OFERTA": 0, "PEDRA": 0}, "PXO": { "PRODUTIVIDADE": 0, "OCIOSIDADE": 0, "META_PRODUTIVIDADE": 0, "META_OCIOSIDADE": 0}, "FILA_MEDIA": 0, "CAPACIDADE": 0, "OPORTUNIDADE": 0},
            "TOTAIS_PSN"   : {"PLANO":{"OFERTA": 0, "PEDRA": 0}, "PXO": { "PRODUTIVIDADE": 0, "OCIOSIDADE": 0, "META_PRODUTIVIDADE": 0, "META_OCIOSIDADE": 0}, "FILA_MEDIA": 0, "CAPACIDADE": 0, "OPORTUNIDADE": 0},
            "TOTAIS_PCZ"   : {"PLANO":{"OFERTA": 0, "PEDRA": 0}, "PXO": { "PRODUTIVIDADE": 0, "OCIOSIDADE": 0, "META_PRODUTIVIDADE": 0, "META_OCIOSIDADE": 0}, "FILA_MEDIA": 0, "CAPACIDADE": 0, "OPORTUNIDADE": 0}
        }

        for TERMINAL in lst_TERMINAIS_ATIVOS:
            
            
            MARGEM = "PSN"
            if INFOS[TERMINAL]["MARGEM"] == "ESQUERDA": MARGEM = "PCZ"

            SAIDAS[DIA][MARGEM][TERMINAL]   = {
               
                "PREFIXO"       : [0] * 24, 
                "FILA"          : [0] * 24, 
                "OCUPACAO"      : [0] * 24, 
                "RESTRICAO"     : [0] * 24,
                "PLANO"         : {"OFERTA"         : 0, "PEDRA"     : 0},
                "PXO"           : {"PRODUTIVIDADE"  : 0, "OCIOSIDADE": 0},   
                "FILA_MEDIA"    : 0,
                "CAPACIDADE"    : 0,
                "OPORTUNIDADE"  : 0
            }
        
            LINHA_SALDO_TOTAL = [0] * 24
            LINHA_PRODT_TOTAL = [0] * 24
            LINHA_FILA_TOTAL  = [0] * 24
            LINHA_OCUP_TOTAL  = [0] * 24

            #region ABRINDO A DESCARGA DO TERMINAL
            with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO_DESCARGA:
                DESCARGA = json.load(ARQUIVO_DESCARGA)
            #endregion
            
            SAIDAS[DIA][MARGEM][TERMINAL]["PREFIXO"]         =  [item[0] for item in DESCARGA["PREFIXO"]]
            SAIDAS[DIA][MARGEM][TERMINAL]["RESTRICAO"]       =  DESCARGA["RESTRICAO_MOTIVO"]
       
            DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()  

            for TIPO_DESC in DESCARGAS_ATIVAS:
                
                FERROVIA, PRODUTO = TIPO_DESC.split("_")

                LINHA_SALDO_PRODUTO = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["SALDO"]
                LINHA_SALDO_TOTAL   = [x + y for x, y in zip(LINHA_SALDO_TOTAL, LINHA_SALDO_PRODUTO)]

                LINHA_PRODT_PRODUTO = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"]
                LINHA_PRODT_TOTAL   = [x + y for x, y in zip(LINHA_PRODT_TOTAL, LINHA_PRODT_PRODUTO)]

                LINHA_FILA_PRODUTO  = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["FILA"]
                LINHA_FILA_TOTAL    = [x + y for x, y in zip(LINHA_FILA_TOTAL, LINHA_FILA_PRODUTO)]
            
            for i in range(24):
                
                if LINHA_SALDO_TOTAL[i] > 0:
                    LINHA_OCUP_TOTAL[i] = "A"

                    if LINHA_PRODT_TOTAL[i] > 0:
                        LINHA_OCUP_TOTAL[i] = "V"
                    
            SAIDAS[DIA][MARGEM][TERMINAL]["OCUPACAO"]   = LINHA_OCUP_TOTAL
            SAIDAS[DIA][MARGEM][TERMINAL]["FILA"]       = LINHA_FILA_TOTAL


            SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["OFERTA"] = DESCARGA["INDICADORES"]["TOTAL_SALDO"]
            SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["PEDRA"]  = DESCARGA["INDICADORES"]["TOTAL_PEDRA"]
            
            
            CONTAGEM_PROD   = len([num for num in LINHA_PRODT_TOTAL if num != 0]) #   [round(prod, 1), (24 - cont_prod)
            
            SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["OCIOSIDADE"]    = (24 - CONTAGEM_PROD )


            if CONTAGEM_PROD != 0: SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["PRODUTIVIDADE"] = round((sum(LINHA_PRODT_TOTAL)/ CONTAGEM_PROD), 1)
            else:                  SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["PRODUTIVIDADE"] = 0  

            SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["META_PRODUTIVIDADE"]  = INFOS[TERMINAL]["PXO"]["PRODUTIVIDADE"]
            SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["META_OCIOSIDADE"]     = INFOS[TERMINAL]["PXO"]["OCIOSIDADE"]

            CONT_TRENS = len([num for num in DESCARGA["PREFIXO"] if num != 0])
            CONT_FILA  = len([num for num in LINHA_FILA_TOTAL if num != 0])
            
            if CONT_FILA != 0:  SAIDAS[DIA][MARGEM][TERMINAL]["FILA_MEDIA"]           = round(CONT_TRENS / CONT_FILA, 1)
            else:               SAIDAS[DIA][MARGEM][TERMINAL]["FILA_MEDIA"] =   0

            SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"] =  24 * SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["PRODUTIVIDADE"] * 0.8

            SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"] = int(SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"])

            CAPACIDADE = SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"]
            PEDRA      = SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["PEDRA"]

            if CAPACIDADE > PEDRA:  SAIDAS[DIA][MARGEM][TERMINAL]["OPORTUNIDADE"] = CAPACIDADE - PEDRA
            else:                   SAIDAS[DIA][MARGEM][TERMINAL]["OPORTUNIDADE"] = 0 

            SAIDAS[DIA]["TOTAIS"]["PLANO"]["OFERTA"]        += SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["OFERTA"]
            SAIDAS[DIA]["TOTAIS"]["PLANO"]["PEDRA"]         += SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["PEDRA"]
            SAIDAS[DIA]["TOTAIS"]["PXO"]["PRODUTIVIDADE"]   += SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["PRODUTIVIDADE"]
            SAIDAS[DIA]["TOTAIS"]["FILA_MEDIA"]             += SAIDAS[DIA][MARGEM][TERMINAL]["FILA_MEDIA"]
            SAIDAS[DIA]["TOTAIS"]["CAPACIDADE"]             += SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"]
            SAIDAS[DIA]["TOTAIS"]["OPORTUNIDADE"]           += SAIDAS[DIA][MARGEM][TERMINAL]["OPORTUNIDADE"]

            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["PLANO"]["OFERTA"]        += SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["OFERTA"]
            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["PLANO"]["PEDRA"]         += SAIDAS[DIA][MARGEM][TERMINAL]["PLANO"]["PEDRA"]
            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["PXO"]["PRODUTIVIDADE"]   += SAIDAS[DIA][MARGEM][TERMINAL]["PXO"]["PRODUTIVIDADE"]
            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["FILA_MEDIA"]             += SAIDAS[DIA][MARGEM][TERMINAL]["FILA_MEDIA"]
            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["CAPACIDADE"]             += SAIDAS[DIA][MARGEM][TERMINAL]["CAPACIDADE"]
            SAIDAS[DIA][f"TOTAIS_{ MARGEM }"]["OPORTUNIDADE"]           += SAIDAS[DIA][MARGEM][TERMINAL]["OPORTUNIDADE"]


        SAIDAS[DIA]["TOTAIS"]["PXO"]["OCIOSIDADE"]      = 0
        SAIDAS[DIA]["TOTAIS_PCZ"]["PXO"]["OCIOSIDADE"]  = 0
        SAIDAS[DIA]["TOTAIS_PSN"]["PXO"]["OCIOSIDADE"]  = 0

        if not SAIDAS[DIA]["TOTAIS"]["PXO"]["PRODUTIVIDADE"] == 0: 
            SAIDAS[DIA]["TOTAIS"]["PXO"]["OCIOSIDADE"]     = round((24 - (SAIDAS[DIA]["TOTAIS"]["PLANO"]["PEDRA"]     / SAIDAS[DIA]["TOTAIS"]["PXO"]["PRODUTIVIDADE"])), 1)
        if not SAIDAS[DIA]["TOTAIS_PCZ"]["PXO"]["PRODUTIVIDADE"] == 0: 
            SAIDAS[DIA]["TOTAIS_PCZ"]["PXO"]["OCIOSIDADE"] = round((24 - (SAIDAS[DIA]["TOTAIS_PCZ"]["PLANO"]["PEDRA"] / SAIDAS[DIA]["TOTAIS_PCZ"]["PXO"]["PRODUTIVIDADE"])), 1)
        if not SAIDAS[DIA]["TOTAIS_PSN"]["PXO"]["PRODUTIVIDADE"] == 0:
            SAIDAS[DIA]["TOTAIS_PSN"]["PXO"]["OCIOSIDADE"] = round((24 - (SAIDAS[DIA]["TOTAIS_PSN"]["PLANO"]["PEDRA"] / SAIDAS[DIA]["TOTAIS_PSN"]["PXO"]["PRODUTIVIDADE"])), 1)

        SAIDAS[DIA]["TOTAIS"]["PXO"]["PRODUTIVIDADE"]  = round(SAIDAS[DIA]["TOTAIS"]["PXO"]["PRODUTIVIDADE"], 1)



    return SAIDAS