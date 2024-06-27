import pandas as pd


def EDITAR_PARAMETROS(PARAMETROS, ACAO="INSERIR"):
        
        print(f'LINHA: {PARAMETROS["COLUNA"]} COLUNA: {PARAMETROS["COLUNA"]} VALOR: {PARAMETROS["NOVO_VALOR"]}')
    
        DIRETORIO = f'previsao_trens/src/PARAMETROS/{PARAMETROS["TABELA"]}'

        DATAFRAME = pd.read_csv(DIRETORIO, sep=";", index_col=0)
        DATAFRAME[DATAFRAME < 0] = 0
        
        if PARAMETROS["LINHA"] in DATAFRAME.index and PARAMETROS["COLUNA"] in DATAFRAME.columns:
            

            if ACAO == "SOMAR":
                PARAMETROS["NOVO_VALOR"] = DATAFRAME.loc[PARAMETROS["LINHA"], PARAMETROS["COLUNA"]] + int(PARAMETROS["NOVO_VALOR"])
        
            DATAFRAME.loc[PARAMETROS["LINHA"], PARAMETROS["COLUNA"]] = int(PARAMETROS["NOVO_VALOR"])
            DATAFRAME[DATAFRAME < 0] = 0

            DATAFRAME.loc[PARAMETROS["LINHA"], "TERMINAL"] = DATAFRAME.loc[PARAMETROS['LINHA'], DATAFRAME.columns[1:]].sum()

            DATAFRAME.to_csv(DIRETORIO, sep=";")

            return int(DATAFRAME.loc[PARAMETROS["LINHA"], PARAMETROS["COLUNA"]])



def EDITAR_PARAMOS_SUBIDAS(PARAMETROS):

    DIRETORIO = "previsao_trens/src/SUBIDA/PARAMETROS/TERMINAIS_ATIVOS.csv"
    DATAFRAME = pd.read_csv(DIRETORIO, sep=";", index_col=0)

    DATAFRAME.loc[PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"]] = int(PARAMETROS["NOVO_VALOR"])
    DATAFRAME.to_csv(DIRETORIO, sep=";")

    return int(DATAFRAME.loc[PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"]])