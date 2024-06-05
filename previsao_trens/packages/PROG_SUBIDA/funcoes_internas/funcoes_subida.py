import pandas as pd
import os, copy, json

class clsSubida:

    def __init__(self):

        PATH_PERIODO_VIGENTE        = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
        PATH_DESCARGAS_ATIVAS       = "previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv"
        PATH_DICIONARIO_TERMINAIS   = "previsao_trens/src/DICIONARIOS/TERMINAIS.json"
        PATH_DICIONARIO_LINHAS      = "previsao_trens/src/OPERACAO/LINHAS.json"

        self.PERIODO_VIGENTE   = pd.read_csv(PATH_PERIODO_VIGENTE,   encoding='utf-8-sig', sep=';', index_col=0)
        self.PERIODO_VIGENTE   = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0])
        self.LISTA_DATA_ARQ    = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()

        self.TERMINAIS_ATIVOS  = pd.read_csv(PATH_DESCARGAS_ATIVAS,  encoding='utf-8-sig', sep=';', index_col=0)

        with open(PATH_DICIONARIO_TERMINAIS)    as ARQUIVO_DESCARGA:   self.INFOS        = json.load(ARQUIVO_DESCARGA)
        with open(PATH_DICIONARIO_LINHAS)       as ARQUIVO_LINHA:      self.INFOS_LINHAS = json.load(ARQUIVO_LINHA)
        

        

class clsLinhaValongoFIPS(clsSubida):

    def __init__():

        pass

    def atualizar_saldo():

        pass

    def FIFO():

        pass


class clsLinhaValongoMRS(clsSubida):

    def __init__():

        pass

    def atualizar_saldo():

        pass

    def FIFO():

        pass


class clsLinha_4000(clsSubida):

    def __init__(self, FULL_4000, INFO):

        self.FULL_4000 = FULL_4000
        self.INFO      = INFO
        pass

    def atualizar_saldo():

        pass

    def FIFO():

        pass

    def analisar_lotes(self):

        for i in range(120):

            DADOS_LINHA_NESTA_HORA          = self.FULL_4000["OCUPACAO"][i]    
            QUANTOS_VAGOES_FORMAM_UM_TREM   = self.INFOS_LINHAS["LINHA_4000"]["ALIVIO"]