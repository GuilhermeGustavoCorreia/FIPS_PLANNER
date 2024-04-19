import json
import pandas as pd
import os
from previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS import EDITAR_PARAMETROS

class NAVEGACAO_DESCARGA:

    def __init__(self):

        self.NM_TERMINAL :  str
        self.DATA_ARQ    :  str
        self.INFOS       :  dict = {}
        self.DESCARGAS   :  dict = {}
        
        self.PERIODO_VIGENTE = pd.read_csv(f"previsao_trens\src\PARAMETROS\PERIODO_VIGENTE.csv", sep=";", index_col=0)
    
    def EDITAR_TREM(self, TREM, ACAO):

        DIRETORIO_DESCARGAS   =  "previsao_trens\src\DESCARGAS"
        


        #region INICIANDO OS OBJETOS
        with open(f"previsao_trens\src\DICIONARIOS\TERMINAIS.json") as ARQUIVO_DESCARGA:
            self.INFOS = json.load(ARQUIVO_DESCARGA)
        
        self.NM_TERMINAL = TREM['terminal']
        TREM_DATA_ARQ    = TREM['previsao'].strftime('%Y-%m-%d')

        #PADRAO PARA REMOVER TREM
        PREFIXO  = 0
        VAGOES   = 0
        HORA     = TREM['previsao'].hour
        DESC_ATV = - 1

        if ACAO == "INSERIR":
            DESC_ATV = 1
            PREFIXO  = TREM["prefixo"]
            VAGOES   = TREM["vagoes"]

        for _, LINHA in self.PERIODO_VIGENTE.iterrows():

            with open(f"previsao_trens\src\DESCARGAS\{ self.NM_TERMINAL }\descarga_{ LINHA['DATA_ARQ'] }.json") as ARQUIVO_DESCARGA:
                DESCARGA = json.load(ARQUIVO_DESCARGA)

            self.DESCARGAS[LINHA['DATA_ARQ']] = DESCARGA

        
        #endregion 

        if HORA > 0 :

            HORA_CHEGADA     = HORA - 1
            DATA_ARQ_CHEGADA = TREM_DATA_ARQ

        else:
            
            HORA_CHEGADA     = 24 - 1
            DATA_ARQ_CHEGADA = self.PERIODO_VIGENTE['DATA_ARQ'].tolist()[self.PERIODO_VIGENTE['DATA_ARQ'].tolist().index(TREM_DATA_ARQ) - 1]
         
        self.DESCARGAS[DATA_ARQ_CHEGADA]["PREFIXO"][HORA_CHEGADA] = PREFIXO
        self.DESCARGAS[DATA_ARQ_CHEGADA]["CHEGADA"][HORA_CHEGADA] = VAGOES

        DIRETORIO_TERMINAL = f'{ DIRETORIO_DESCARGAS }\{self.NM_TERMINAL}'     
        ARQUIVO = f"descarga_{ DATA_ARQ_CHEGADA }.json"
        
        PARAMETROS = {

                "NOVO_VALOR":   DESC_ATV,
                "LINHA":        self.NM_TERMINAL,
                "COLUNA":       f"{TREM["ferrovia"]}_{TREM["mercadoria"]}",
                "TABELA":       "DESCARGAS_ATIVAS.csv",

            }


        EDITAR_PARAMETROS(PARAMETROS, "SOMAR")

        with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
            json.dump(self.DESCARGAS[DATA_ARQ_CHEGADA], ARQUIVO_NOME)



