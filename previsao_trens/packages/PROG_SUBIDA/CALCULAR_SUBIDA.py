import pandas as pd
import os, copy, json
from previsao_trens.packages.PROG_SUBIDA.funcoes_internas.funcoes_subida import clsLinhaValongoMRS, clsLinhaValongoFIPS, clsLinha_4000
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)


SATURACAO_ADM = { "MAX": 35, "MIN": 20 }
ALIVIO_ADM    = 20



#TERMINAG MAX L4 -> 28
#

class SUBIDA_DE_VAZIOS:

    def __init__(self):

        self.PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
        self.PERIODO_VIGENTE   = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0])
        self.LISTA_DATA_ARQ    = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()

        self.TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)

        with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
            self.INFOS = json.load(ARQUIVO_DESCARGA)

        with open(f"previsao_trens/src/OPERACAO/LINHAS.json") as ARQUIVO_LINHA:
            self.INFOS_LINHAS = json.load(ARQUIVO_LINHA)

        self.MODELO_TABELA_VAZIA    : dict
        self.TERMIAIS_VAZIOS        : dict #ESTE!
        self.LINHAS                 : dict
        self.FULL_TABLE             : dict #ESTE NÃO ERA "self." AGORA É
        self.FULL_LINHAS            : dict

    def __SALVAR__(self):

        DIRETORIO_TABELA_VAZIOS = "previsao_trens/src/OPERACAO/TABELAS_VAZIOS"


        #SALVANDO AS TABELAS
        for DATA_ARQ in self.TERMIAIS_VAZIOS.keys():
                with open(os.path.join(DIRETORIO_TABELA_VAZIOS, f'GERACAO_VAZIO_{DATA_ARQ}.json'), 'w') as ARQUIVO_NOME:
                    json.dump(self.TERMIAIS_VAZIOS[DATA_ARQ], ARQUIVO_NOME, indent=4)

        #SALVANSO AS LINHAS
        DIRETORIO_LINHAS = "previsao_trens/src/OPERACAO/LINHAS_VAZIOS"
        LINHAS = (os.listdir(DIRETORIO_LINHAS))

        for DATA_ARQ in self.LINHAS.keys():
            for LINHA in LINHAS:
                with open(os.path.join(DIRETORIO_LINHAS, f"{ LINHA }/subida_{ DATA_ARQ }.json"), 'w') as ARQUIVO_NOME:
                    json.dump(self.LINHAS[DATA_ARQ][LINHA], ARQUIVO_NOME, indent=4)   

    def __CRIAR_TABELAS__(self):

        def __CRIAR_VAZIAS__():     #CRIA PARA OS TERMINAIS E PARA AS LINHAS
            
            #region CRIANDO AS TABELAS

            lst_TERMINAIS_ATIVOS  = self.TERMINAIS_ATIVOS[self.TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
            self.TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)
            self.TERMIAIS_VAZIOS = {}

            for DATA_ARQ in self.LISTA_DATA_ARQ:

                self.TERMIAIS_VAZIOS[DATA_ARQ] = {}
                self.TERMIAIS_VAZIOS[DATA_ARQ] = {}

                for TERMINAL in lst_TERMINAIS_ATIVOS:

                    if not TERMINAL == "SBR":

                        MARGEM   = self.INFOS[TERMINAL]["MARGEM"]
                        PATIO    = self.INFOS[TERMINAL]["PATIO"]
                        SEGMENTO = self.INFOS[TERMINAL]["SEGMENTO"]

                        if not MARGEM in self.TERMIAIS_VAZIOS[DATA_ARQ]:        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]        = {}
                        if not PATIO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]: self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO] = {}

                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]             = {}
                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]   = {}


                        DESCARGAS_ATIVAS = self.TERMINAIS_ATIVOS.loc[TERMINAL][self.TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
                        DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS]

                        for DESCARGA in DESCARGAS_ATIVAS:

                            FERROVIA = DESCARGA[0]
                            
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]                            = {}
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]               =  0
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_VAZIO"]           = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"]                  = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"]             = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"]           = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["OCUPACAO"]                = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"] = []
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VIRADA_VAZIOS"]     =  0
                            self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"]                   = []

            self.MODELO_TABELA_VAZIA = copy.deepcopy(self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]])
            
            #endregion

            #region CRIANDO AS LINHAS

            DIRETORIO_LINHAS = "previsao_trens/src/OPERACAO/LINHAS_VAZIOS"
            LINHAS           = (os.listdir(DIRETORIO_LINHAS))
            ITENS_DAS_LINHAS = ["RECEBIDOS", "SALDO", "SEGMENTO", "ALIVIO", "SAIDA"] 
            FERROVIAS        = ["RUMO", "MRS", "VLI"]
            self.LINHAS      = {}

            

            for DATA_ARQ in self.LISTA_DATA_ARQ:
                self.LINHAS[DATA_ARQ] = {}

                for NM_LINHA in LINHAS:

                    self.LINHAS[DATA_ARQ][NM_LINHA]              = {}
                    self.LINHAS[DATA_ARQ][NM_LINHA]["LINHA"]     = NM_LINHA
                    self.LINHAS[DATA_ARQ][NM_LINHA]["DATA"]      = DATA_ARQ
                    self.LINHAS[DATA_ARQ][NM_LINHA]["FERROVIAS"] = {}  
                    self.LINHAS[DATA_ARQ][NM_LINHA]["OCUPACAO"]  = [{"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""} for _ in range(24)]  

                    for FERROVIA in FERROVIAS:
                        self.LINHAS[DATA_ARQ][NM_LINHA]["FERROVIAS"][FERROVIA] = {}
                        
                        for ITEM in ITENS_DAS_LINHAS:
                            self.LINHAS[DATA_ARQ][NM_LINHA]["FERROVIAS"][FERROVIA][ITEM] = [0] * 24

                        try:
                            with open(f"previsao_trens/src/OPERACAO/LINHAS_VAZIOS/{ NM_LINHA }/subida_{ self.LISTA_DATA_ARQ[0] }.json") as ARQUIVO_LINHA:
                                LINHA_SUBIDA = json.load(ARQUIVO_LINHA)
                            
                            self.LINHAS[DATA_ARQ][NM_LINHA]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"] = LINHA_SUBIDA["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]
                        except:
                            self.LINHAS[DATA_ARQ][NM_LINHA]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"] = {"STATUS": "LIVRE", "VAGOES": 0, "FERROVIA": None, "SEGMENTO": None}

            #endregion

        def __PREENCHER_TABELAS__():

            for DATA_ARQ in self.TERMIAIS_VAZIOS.keys():
                for MARGEM in self.TERMIAIS_VAZIOS[DATA_ARQ]:
                    for PATIO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]:
                        for TERMINAL in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]:

                            with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO_DESCARGA:
                                JSON_DESCARGA = json.load(ARQUIVO_DESCARGA)

                            for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]:
                                if not SEGMENTO == "SATURACAO":

                                    for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]:

                                        LISTA_TOTAL      = [0] * 24
                                        LISTA_PROD_TOTAL = [0] * 24
                                        LISTA_SLD_TOTAL  = [0] * 24

                                        #   CHAVE  , VALOR ;)
                                        for PRODUTO, LISTA in JSON_DESCARGA["DESCARGAS"][FERROVIA].items():
                                            
                                            #AQUI SOMA AS PRODUTIVIDADES DO MESMO SEGMENTO DE UMA FERROVIA NO MESMO TERMINAL
                                            #EXEMPLO: FARELO e MILHO DE UM TREM DA RUMO NO TES
                                            LISTA_TOTAL      = [sum(x) for x in zip(LISTA_TOTAL,        LISTA["GERACAO_DE_VAZIOS"])]
                                            LISTA_PROD_TOTAL = [sum(x) for x in zip(LISTA_PROD_TOTAL,   LISTA["PRODUTIVIDADE"])]
                                            LISTA_SLD_TOTAL  = [sum(x) for x in zip(LISTA_SLD_TOTAL,    LISTA["SALDO"])]

                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]               = self.INFOS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_VAZIO"]           = LISTA_TOTAL
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"] = [[0, 0]] * 24
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"]                  = [0] * 24
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"]             = LISTA_TOTAL
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"]           = LISTA_PROD_TOTAL
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VIRADA_VAZIOS"]     = JSON_DESCARGA["INDICADORES"]["SALDO_DE_VIRADA_VAZIOS"][FERROVIA]
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"]                   = LISTA_SLD_TOTAL
        
        def __AJUSTAR_ADM__():

            # 1.CRIAR DICIONARIO ADM VAZIO
            # 2.POPULAR DICIONARIO ADM
            # 3.EXCLUIR MOEGAS

            if not "DIREITA" in self.MODELO_TABELA_VAZIA:
                return
        
            if not "PCX" in self.MODELO_TABELA_VAZIA["DIREITA"]:
                return
     
            MOEGAS = ["MOEGA X", "MOEGA V"]
            MARGEM = "DIREITA"
            PATIO  = "PCX"

            ITENS  = ["GERACAO_VAZIO", "ALIVIO", "SALDO_VAZIO", "PRODUTIVIDADE", "SALDO"]

            if "MOEGA X" in self.MODELO_TABELA_VAZIA["DIREITA"]["PCX"] and "MOEGA V" in self.MODELO_TABELA_VAZIA["DIREITA"]["PCX"]:
                
                for DATA_ARQ in self.TERMIAIS_VAZIOS.keys():  
                   
                    self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"] = {}        

                    #CRIANDO A TABELA DA ADM COM OS SEGMENTOS E FERROVIAS PRESENTES NA MOEGA X OU NA MOEGA V
                    for TERMINAL in MOEGAS:
                        
                        for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]:

                            if not SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"]:
                                self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO] = {}

                            for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]:  

                                if not FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO]:
                                    self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO][FERROVIA] = {}
                                
                                #INSERINDO OS ITENS EM CADA FERROVIA DA ADM, OS ITENS ESTAO VAZIOS
                                for ITEM in ITENS:
                                    
                                    if not ITEM in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO][FERROVIA]:
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO][FERROVIA][ITEM] = ["x"] * 24

                                if not "SATURACAO" in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO][FERROVIA]:
                                    self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO][FERROVIA]["SATURACAO"] = SATURACAO_ADM

                    #1. SOMANDO E INSERINDO OS VALORES DAS MOEGAS NA ADM
                    for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"]:
                        for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["ADM"][SEGMENTO]: 
                            if FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["MOEGA X"][SEGMENTO] and FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["MOEGA V"][SEGMENTO]:
                                
                                self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"] = [[0, 0]] * 24
                                for ITEM in ITENS:
                                    LISTA_TOTAL = [0] * 24

                                    for MOEGA in MOEGAS: 
                                        LISTA_TOTAL = [sum(x) for x in zip(LISTA_TOTAL, self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][MOEGA][SEGMENTO][FERROVIA][ITEM])]
                                    
                                    self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"][SEGMENTO][FERROVIA][ITEM] = LISTA_TOTAL

                            elif FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["MOEGA X"][SEGMENTO]:

                                self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"][SEGMENTO][FERROVIA] = self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["MOEGA X"][SEGMENTO][FERROVIA]

                            elif FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["MOEGA V"][SEGMENTO]:

                                self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"][SEGMENTO][FERROVIA] = self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["MOEGA V"][SEGMENTO][FERROVIA]

                            self.TERMIAIS_VAZIOS[DATA_ARQ]["DIREITA"]["PCX"]["ADM"][SEGMENTO][FERROVIA]["SALDO_VIRADA_VAZIOS"] = self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]["MOEGA V"][SEGMENTO][FERROVIA]["SALDO_VIRADA_VAZIOS"]
                   
                    #3. EXCLUINDO MOEGAS
                    for TERMINAL in MOEGAS:
                        del self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL] 
          
            self.MODELO_TABELA_VAZIA = copy.deepcopy(self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]])
     
        __CRIAR_VAZIAS__()

        __PREENCHER_TABELAS__()
           
        __AJUSTAR_ADM__()

    def __CRIAR_TABELAS_FULL__(self):

        #region MONTANDO A TABELA FULL (CONTEM TODOS OS DIAS EM SÉRIE EM UMA UNICA LISTA)

        #CRIANDO A VARIAVEL COM 120 COLUNAS EM CADA CHAVE
        ITENS_DAS_LINHAS    =  ["RECEBIDOS", "SALDO", "SEGMENTO", "ALIVIO", "SAIDA"] 

        self.FULL_TABLE = {}

        #CRIANDO A FULL_TABLE

        for MARGEM in self.MODELO_TABELA_VAZIA:
            self.FULL_TABLE[MARGEM] = {}
            
            for PATIO in self.MODELO_TABELA_VAZIA[MARGEM]:
                
                self.FULL_TABLE[MARGEM][PATIO] = {}

                for TERMINAL in self.MODELO_TABELA_VAZIA[MARGEM][PATIO]:
                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL] = {}

                    for SEGMENTO in self.MODELO_TABELA_VAZIA[MARGEM][PATIO][TERMINAL]:
                        self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO] = {}
                        
                        for FERROVIA in self.MODELO_TABELA_VAZIA[MARGEM][PATIO][TERMINAL][SEGMENTO]:

                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA] = {}

                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]       = self.MODELO_TABELA_VAZIA[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_VAZIO"]   = []
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"]          = []
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"]     = []
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"]   = []
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"] = []
                            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"] = []


        for DATA_ARQ in self.LISTA_DATA_ARQ:  

            for MARGEM in self.TERMIAIS_VAZIOS[DATA_ARQ]:

                for PATIO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]:

                    for TERMINAL in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]:

                        for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]:

                            if not SEGMENTO == "SATURACAO":

                                for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]:

                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_VAZIO"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_VAZIO"])
                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"])
                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"])
                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"])
                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"])
                                    self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"].extend(self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"])
        #endregion 

        #region MONTANDO AS LINHA FULL (self.FULL_LINHAS)
        DIRETORIO_LINHAS = "previsao_trens/src/OPERACAO/LINHAS_VAZIOS"
        LINHAS = (os.listdir(DIRETORIO_LINHAS))
        
        FERROVIAS   = ["RUMO", "MRS", "VLI"]
        ITENS_DAS_LINHAS    =  ["RECEBIDOS", "SALDO", "SEGMENTO", "ALIVIO", "SAIDA"] 
        self.FULL_LINHAS = {}
        
        #CRIA A TABELA
        for LINHA in LINHAS:
            
            self.FULL_LINHAS[LINHA] = {}
            self.FULL_LINHAS[LINHA]["FERROVIAS"] = {}
            self.FULL_LINHAS[LINHA]["OCUPACAO"]  = []
            
            for FERROVIA in FERROVIAS:
                self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA] = {}

                for ITEM in ITENS_DAS_LINHAS:
                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA][ITEM] = []

        #PREENCHE OS VALORES DA TABELA
        for DATA_ARQ in self.LISTA_DATA_ARQ:  
            for LINHA in LINHAS:
                for FERROVIA in FERROVIAS:

                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["RECEBIDOS"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["FERROVIAS"][FERROVIA]["RECEBIDOS"])
                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["SALDO"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO"])
                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["SEGMENTO"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SEGMENTO"])
                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["ALIVIO"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["FERROVIAS"][FERROVIA]["ALIVIO"])
                    self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["SAIDA"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SAIDA"]) 

    
                self.FULL_LINHAS[LINHA]["OCUPACAO"].extend(self.LINHAS[DATA_ARQ][LINHA]["OCUPACAO"])

        #endregion
  
    def __CALCULAR__(self):

        ############################################################################################################

        def __ATUALIZAR_SALDO_LINHA_VALONGO__(FERROVIA):

            for i in range(120):
                
                if i > 0:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                    ALIVIO         = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                else:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = int(self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"])
                    ALIVIO         = 0
                                           
                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO
                                    
                if (SALDO == 0) and self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["FERROVIA"] == FERROVIA:            
                    self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}
                    
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:
                    
                    if i > 0:
                    
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i-1]["STATUS"]
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i-1]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i-1]["SEGMENTO"]

                    else: 

                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["STATUS"]   = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"]
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["FERROVIA"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i]["SEGMENTO"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"]

        def __ATUALIZAR_SALDO_LINHA_4000__(FERROVIA):      
            
            for i in range(120):
               
                if i > 0:

                    RECEBIDOS       = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR  = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                    ALIVIO          = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                else:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = int(self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"])
                    ALIVIO         = 0

                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO

                if (SALDO == 0) and (self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["FERROVIA"] == FERROVIA):
                    self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}    
                    
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:
                    
                    if i > 0:
                    
                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i-1]["STATUS"]
                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i-1]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i-1]["SEGMENTO"]

                    else: 

                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["STATUS"]   = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"]
                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["FERROVIA"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["SEGMENTO"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"]

        def __ATUALIZAR_SALDO_LINHA_VALONGO_MRS__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False):

            if FORCAR_ALIVIO:

                RECEBIDOS       = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO]
                SALDO_ANTERIOR  = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO - 1]
                self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = RECEBIDOS + SALDO_ANTERIOR
            
            
            for i in range(1, 120):
                
                RECEBIDOS      = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                SALDO_ANTERIOR = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                ALIVIO         = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO
                                    
                if (SALDO == 0):            
                    self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}
                    
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:
                    
                    self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i-1]["STATUS"]
                    self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i-1]["FERROVIA"]
                    self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i-1]["SEGMENTO"]

        def __ATUALIZAR_SALDO_LINHA_1__(FERROVIA):

            for i in range(120):
                
                if i > 0:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                    ALIVIO         = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                else:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = int(self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"])
                    ALIVIO         = 0

                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO

                if (SALDO == 0):       

                    self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}
                
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:

                    if i > 0:

                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i-1]["STATUS"]
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i-1]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i-1]["SEGMENTO"]
                    
                    else: 

                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["STATUS"]   = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"]
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["FERROVIA"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i]["SEGMENTO"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"]

        def __ATUALIZAR_SALDO_LINHA_2__(FERROVIA):

            for i in range(120):


                if i > 0:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                    ALIVIO         = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                else:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = int(self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"])
                    ALIVIO         = 0


                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO

                if (SALDO == 0):            
                    self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}
                
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:

                    if i > 0:

                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i-1]["STATUS"]
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i-1]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i-1]["SEGMENTO"]

                    else: 

                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["STATUS"]   = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"]
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["FERROVIA"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i]["SEGMENTO"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"]
 
        def __ATUALIZAR_SALDO_LINHA_3__(FERROVIA):

            for i in range(120):


                if i > 0:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO"][i-1]
                    ALIVIO         = self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA]["ALIVIO"][i-1]

                else:

                    RECEBIDOS      = self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][i]
                    SALDO_ANTERIOR = int(self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"])
                    ALIVIO         = 0


                SALDO = RECEBIDOS + SALDO_ANTERIOR - ALIVIO

                self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO"][i] = SALDO

                if (SALDO == 0):            
                    
                    self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i] = {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}
                
                elif SALDO > 0 and self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i] == {"STATUS": "LIVRE", "FERROVIA": "", "SEGMENTO": ""}:

                    if i > 0:

                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["STATUS"]   = self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i-1]["STATUS"]
                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["FERROVIA"] = self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i-1]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["SEGMENTO"] = self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i-1]["SEGMENTO"]

                    else: 

                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["STATUS"]   = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"]
                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["FERROVIA"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"]
                        self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i]["SEGMENTO"] = self.LINHAS[self.LISTA_DATA_ARQ[1]]["LINHA_3"]["FERROVIAS"][FERROVIA]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"]
 
        def __ATUALIZAR_SALDO_LINHA_PCZ__(LINHA, FERROVIA):

            if LINHA == "LINHA_1":
                __ATUALIZAR_SALDO_LINHA_1__(FERROVIA)

            if LINHA == "LINHA_2":
                __ATUALIZAR_SALDO_LINHA_2__(FERROVIA)

            if LINHA == "LINHA_3":
                __ATUALIZAR_SALDO_LINHA_3__(FERROVIA)

        ############################################################################################################
        
        def __GESTAO_DE_FIFO_VALONGO_FIPS__(VAGOES_NOS_TEMRINAS, VAGOES_DA_LINHA_4000, PARAMETROS_LINHA_VALONGO):
            
            ALIVIO = {    
                "ORIGEM":       "",
                "SEGMENTO":     "",
                "QUANTIDADE":   "",
                "FERROVIA":     "",
                "SLA":          ""
            }

            TIPO_DESC_ESCOLHIDO = ""
            
            #region JUNTANDO AS POSSIBILIDADES VALONGO E TERMINAIS EM UMA LISTA (x)

            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX"])

            for ALIVIO in VAGOES_NOS_TEMRINAS:
                
                NOVA_LINHA = {

                    "PATIO":    ALIVIO["PATIO"],
                    "ORIGEM":   ALIVIO["TERMINAL"],
                    "SEGMENTO": ALIVIO["SEGMENTO"], 
                    "FERROVIA": ALIVIO["FERROVIA"], 
                    "VAGOES":   ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":      ALIVIO["MIN"],
                    "MAX":      ALIVIO["MAX"]

                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            if not VAGOES_DA_LINHA_4000 == None:

                NOVA_LINHA =  {

                    "PATIO":    "",
                    "ORIGEM":   VAGOES_DA_LINHA_4000["ORIGEM"],
                    "SEGMENTO": VAGOES_DA_LINHA_4000["SEGMENTO"], 
                    "FERROVIA": VAGOES_DA_LINHA_4000["FERROVIA"], 
                    "VAGOES":   VAGOES_DA_LINHA_4000["VAGOES"], 
                    "MIN":      VAGOES_DA_LINHA_4000["MIN"],
                    "MAX":      VAGOES_DA_LINHA_4000["MAX"]

                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            #endregion

            if len(TABELA_DE_ALIVIOS) == 0: return None 
            
            #region LINHA VALONGO LIVRE
            
            if  PARAMETROS_LINHA_VALONGO["STATUS"] == "LIVRE":
                
                #region ALIVIOS ACIMA DO LIMITE MAXIMO
                TIPO_DESC_SATURADOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MAX"]]
                TIPO_DESC_COM_ALIVIO = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MIN"]]
                
                if not TIPO_DESC_SATURADOS.empty:
                    
                    TIPO_DESC_SELECIONADO = TIPO_DESC_SATURADOS.loc[TIPO_DESC_SATURADOS["VAGOES"].idxmax()]

                    if TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_VALONGO["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_VALONGO["VAGOES_NECESSÁRIOS"]

                #endregion

                #region ACIMA DO LIMITE MINIMO       
                elif not TIPO_DESC_COM_ALIVIO.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_COM_ALIVIO.loc[TIPO_DESC_COM_ALIVIO["VAGOES"].idxmax()]

                else:
                    return None
                
                #endregion

            #endregion

            #region LINHA VALONGO OCUPADA (NAO CONSIDERA MEIO VAGAO DO PCX - LINHA 4000)
            
            elif PARAMETROS_LINHA_VALONGO["STATUS"] == "OCUPADO":
                               
                FERROVIA     = PARAMETROS_LINHA_VALONGO["FERROVIA"]
                SEGMENTO     = PARAMETROS_LINHA_VALONGO["SEGMENTO"]

                # Adicionando novas colunas
                TABELA_DE_ALIVIOS["VAGOES_NESC."]       = PARAMETROS_LINHA_VALONGO["VAGOES_NECESSÁRIOS"]
                TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"]   = TABELA_DE_ALIVIOS["VAGOES"] - TABELA_DE_ALIVIOS["VAGOES_NESC."]
                TABELA_DE_ALIVIOS["TX_MIN"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
                TABELA_DE_ALIVIOS["TX_MAX"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)

                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FERROVIA)]
                
                if len(TABELA_DE_ALIVIOS) == 0: return None    

                #region CONSIDERANDO APENAS PST

                TABELA_DE_PST = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["PATIO"] == "PST"]
                
                if len(TABELA_DE_PST) > 0:
                    
                    TABELA_DE_PST = TABELA_DE_PST[TABELA_DE_PST["DIFERENCA_VAGOES"] >= 0]
                    
                    if len(TABELA_DE_PST) > 0:
        
                        ID_LINHA_MAIS_PROXIMA = TABELA_DE_PST['DIFERENCA_VAGOES'].idxmin()
                        TIPO_DESC_SELECIONADO = TABELA_DE_PST.loc[ID_LINHA_MAIS_PROXIMA]
                        TIPO_DESC_SELECIONADO["VAGOES"] = TIPO_DESC_SELECIONADO["VAGOES_NESC."]

                    else: return None

                else: return None

                #endregion
            
            #endregion
            
            TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

            return TIPO_DESC_ESCOLHIDO
        
        def __GESTAO_DE_FIFO_VALONGO_MRS__(VAGOES_NOS_TEMRINAS, VAGOES_DA_LINHA_4000, PARAMETROS_LINHA_VALONGO):

            ALIVIO = {    
                
                "ORIGEM":       "",
                "SEGMENTO":     "",
                "QUANTIDADE":   "",
                "FERROVIA":     "",
                "SLA":          ""

            }

            TIPO_DESC_ESCOLHIDO = ""
            ALIVIAR = False
            #region JUNTANDO AS POSSIBILIDADES VALONGO E TERMINAIS EM UMA LISTA (x)

            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX", "SALDO"])
            
            if not VAGOES_DA_LINHA_4000 == None and len(VAGOES_NOS_TEMRINAS) > 0:
                
                pass

            for ALIVIO in VAGOES_NOS_TEMRINAS:
                
                NOVA_LINHA = {
                    "PATIO":    ALIVIO["PATIO"],
                    "ORIGEM":   ALIVIO["TERMINAL"],
                    "SEGMENTO": ALIVIO["SEGMENTO"], 
                    "FERROVIA": ALIVIO["FERROVIA"], 
                    "VAGOES":   ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":      ALIVIO["MIN"],
                    "MAX":      ALIVIO["MAX"],
                    "SALDO":    ALIVIO["SALDO"]
                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            if not VAGOES_DA_LINHA_4000 == None:

                NOVA_LINHA =  {
                    "PATIO":    "",
                    "ORIGEM":   VAGOES_DA_LINHA_4000["ORIGEM"],
                    "SEGMENTO": VAGOES_DA_LINHA_4000["SEGMENTO"], 
                    "FERROVIA": VAGOES_DA_LINHA_4000["FERROVIA"], 
                    "VAGOES":   VAGOES_DA_LINHA_4000["VAGOES"], 
                    "MIN":      VAGOES_DA_LINHA_4000["MIN"],
                    "MAX":      VAGOES_DA_LINHA_4000["MAX"],
                    "SALDO":    99
                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            #endregion

            if len(TABELA_DE_ALIVIOS) == 0: return None, None
            
            #region LINHA VALONGO LIVRE
            
            if  PARAMETROS_LINHA_VALONGO["STATUS"] == "LIVRE":

                #region ALIVIOS ACIMA DO LIMITE MAXIMO
                TIPO_DESC_SATURADOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MAX"]]
                TIPO_DESC_COM_ALIVIO = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MIN"]]
                
                if not TIPO_DESC_SATURADOS.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_SATURADOS.loc[TIPO_DESC_SATURADOS["VAGOES"].idxmax()]
                
                #endregion

                #region ACIMA DO LIMITE MINIMO       
                elif not TIPO_DESC_COM_ALIVIO.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_COM_ALIVIO.loc[TIPO_DESC_COM_ALIVIO["VAGOES"].idxmax()]

                else:
                    return None, None
                
                #endregion

            #endregion

            #region LINHA VALONGO OCUPADA (NAO CONSIDERA MEIO VAGAO DO PCX - LINHA 4000)
            
            elif PARAMETROS_LINHA_VALONGO["STATUS"] == "OCUPADO":
                
                FERROVIA     = PARAMETROS_LINHA_VALONGO["FERROVIA"]
                SEGMENTO     = PARAMETROS_LINHA_VALONGO["SEGMENTO"]

                # Adicionando novas colunas
                TABELA_DE_ALIVIOS["VAGOES_NESC."]       = PARAMETROS_LINHA_VALONGO["VAGOES_NECESSÁRIOS"]
                TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"]   = TABELA_DE_ALIVIOS["VAGOES"] - TABELA_DE_ALIVIOS["VAGOES_NESC."]
                TABELA_DE_ALIVIOS["TX_MIN"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
                TABELA_DE_ALIVIOS["TX_MAX"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)


                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FERROVIA)]
                if len(TABELA_DE_ALIVIOS) == 0: return None, None    

                #region CONSIDERANDO APENAS PST

                TABELA_DE_PST = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["PATIO"] == "PST"]
                
                if len(TABELA_DE_PST) > 0:
                    
                    TABELA_LOTES_FINAIS = TABELA_DE_PST[TABELA_DE_PST["SALDO"] == 0]

                    if len(TABELA_LOTES_FINAIS) > 0:

                        ID_LINHA_MAIS_PROXIMA = TABELA_LOTES_FINAIS['DIFERENCA_VAGOES'].idxmin()
                        TIPO_DESC_SELECIONADO = TABELA_LOTES_FINAIS.loc[ID_LINHA_MAIS_PROXIMA]
                        ALIVIAR  = True

                    else: return None, None, 

                else: return None, None

                #endregion

                
            #endregion
            
            TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

            return TIPO_DESC_ESCOLHIDO, ALIVIAR

        def __GESTAO_DE_FIFO_LINHA_1__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA):

            TIPO_DESC_SELECIONADO = ""

            #region LISTANDO AS POSSIBILIDADES EM UMA TABELA

            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX"])

            for ALIVIO in VAGOES_NOS_TEMRINAS:
                
                NOVA_LINHA = {
                    "PATIO":    ALIVIO["PATIO"],
                    "ORIGEM":   ALIVIO["TERMINAL"],
                    "SEGMENTO": ALIVIO["SEGMENTO"], 
                    "FERROVIA": ALIVIO["FERROVIA"], 
                    "VAGOES":   ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":      ALIVIO["MIN"],
                    "MAX":      ALIVIO["MAX"]
                }
                
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            if len(TABELA_DE_ALIVIOS) == 0: return None
            #endregion 

            #region LINHA VALONGO LIVRE
            if  PARAMETROS_LINHA["STATUS"] == "LIVRE":
                
                #region ALIVIOS ACIMA DO LIMITE MAXIMO
                TIPO_DESC_SATURADOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MAX"]]
                TIPO_DESC_COM_ALIVIO = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MIN"]]
                
                if not TIPO_DESC_SATURADOS.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_SATURADOS.loc[TIPO_DESC_SATURADOS["VAGOES"].idxmax()]
                
                #endregion

                #region ACIMA DO LIMITE MINIMO       
                elif not TIPO_DESC_COM_ALIVIO.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_COM_ALIVIO.loc[TIPO_DESC_COM_ALIVIO["VAGOES"].idxmax()]

                else:
                    return None
                
                #endregion

            #endregion

            #region LINHA 1 OCUPADA
            
            elif PARAMETROS_LINHA["STATUS"] == "OCUPADO":
                
                FERROVIA     = PARAMETROS_LINHA["FERROVIA"]
                SEGMENTO     = PARAMETROS_LINHA["SEGMENTO"]
                VAGOES_LINHA = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]

                # Adicionando novas colunas
                TABELA_DE_ALIVIOS["VAGOES_NESC."]       = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]
                TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"]   = TABELA_DE_ALIVIOS["VAGOES"] - TABELA_DE_ALIVIOS["VAGOES_NESC."]
                TABELA_DE_ALIVIOS["TX_MIN"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
                TABELA_DE_ALIVIOS["TX_MAX"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)


                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FERROVIA)]
                if len(TABELA_DE_ALIVIOS) == 0: return None    

                #region CONSIDERANDO 

                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"] >= 0]
                
                if len(TABELA_DE_ALIVIOS) > 0:
    
                    ID_LINHA_MAIS_PROXIMA = TABELA_DE_ALIVIOS['DIFERENCA_VAGOES'].idxmin()
                    TIPO_DESC_SELECIONADO = TABELA_DE_ALIVIOS.loc[ID_LINHA_MAIS_PROXIMA]
                    TIPO_DESC_SELECIONADO["VAGOES"] = TIPO_DESC_SELECIONADO["VAGOES_NESC."]
                
                else: 
                    
                    return None



                #endregion

            #endregion

            TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

            return TIPO_DESC_ESCOLHIDO
        
        def __GESTAO_DE_FIFO_LINHA_2__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA):

            TIPO_DESC_SELECIONADO = ""

            #region LISTANDO AS POSSIBILIDADES EM UMA TABELA

            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX"])

            for ALIVIO in VAGOES_NOS_TEMRINAS:
                
                NOVA_LINHA = {
                    "PATIO":    ALIVIO["PATIO"],
                    "ORIGEM":   ALIVIO["TERMINAL"],
                    "SEGMENTO": ALIVIO["SEGMENTO"], 
                    "FERROVIA": ALIVIO["FERROVIA"], 
                    "VAGOES":   ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":      ALIVIO["MIN"],
                    "MAX":      ALIVIO["MAX"]
                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA

            if len(TABELA_DE_ALIVIOS) == 0: return None
            #endregion

            #region LINHA 2 LIVRE
            if  PARAMETROS_LINHA["STATUS"] == "LIVRE":
                
                #region ALIVIOS ACIMA DO LIMITE MAXIMO
                TIPO_DESC_SATURADOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MAX"]]
                TIPO_DESC_COM_ALIVIO = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MIN"]]
                
                if not TIPO_DESC_SATURADOS.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_SATURADOS.loc[TIPO_DESC_SATURADOS["VAGOES"].idxmax()]
                
                #endregion

                #region ACIMA DO LIMITE MINIMO       
                elif not TIPO_DESC_COM_ALIVIO.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_COM_ALIVIO.loc[TIPO_DESC_COM_ALIVIO["VAGOES"].idxmax()]

                else:
                    return None
                #endregion
                                
            #endregion

            #region LINHA 2 OCUPADA
            
            elif PARAMETROS_LINHA["STATUS"] == "OCUPADO":
                
                FERROVIA     = PARAMETROS_LINHA["FERROVIA"]
                SEGMENTO     = PARAMETROS_LINHA["SEGMENTO"]
                VAGOES_LINHA = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]

                # Adicionando novas colunas
                TABELA_DE_ALIVIOS["VAGOES_NESC."]       = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]
                TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"]   = TABELA_DE_ALIVIOS["VAGOES"] - TABELA_DE_ALIVIOS["VAGOES_NESC."]
                TABELA_DE_ALIVIOS["TX_MIN"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
                TABELA_DE_ALIVIOS["TX_MAX"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)


                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FERROVIA)]
                if len(TABELA_DE_ALIVIOS) == 0: return None    

                #region CONSIDERANDO 

                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"] >= 0]
                
                if len(TABELA_DE_ALIVIOS) > 0:
    
                    ID_LINHA_MAIS_PROXIMA = TABELA_DE_ALIVIOS['DIFERENCA_VAGOES'].idxmin()
                    TIPO_DESC_SELECIONADO = TABELA_DE_ALIVIOS.loc[ID_LINHA_MAIS_PROXIMA]
                    TIPO_DESC_SELECIONADO["VAGOES"] = TIPO_DESC_SELECIONADO["VAGOES_NESC."]
                
                else: 
                     return None



                #endregion

            #endregion

            TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

            return TIPO_DESC_ESCOLHIDO
        
        def __GESTAO_DE_FIFO_LINHA_4000__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA):
            
            #ESTE FILTRO É PARA O CASO DA LINHA ESTAR CHEIA

            if PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"] < 0:
                 return None

            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX"])

            for ALIVIO in VAGOES_NOS_TEMRINAS:

                NOVA_LINHA = {

                    "PATIO":    ALIVIO["PATIO"],
                    "ORIGEM":   ALIVIO["TERMINAL"],
                    "SEGMENTO": ALIVIO["SEGMENTO"], 
                    "FERROVIA": ALIVIO["FERROVIA"], 
                    "VAGOES":   ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":      ALIVIO["MIN"],
                    "MAX":      ALIVIO["MAX"]

                }

                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA
            
            TABELA_DE_ALIVIOS["VAGOES_LINHA"] = PARAMETROS_LINHA["VAGOES"]

            if len(TABELA_DE_ALIVIOS) == 0: return None 
                
            #region LINHA LIVRE
            if  PARAMETROS_LINHA["STATUS"] == "LIVRE":
                
                #region ALIVIOS ACIMA DO LIMITE MAXIMO
                TIPO_DESC_SATURADOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MAX"]]
                TIPO_DESC_COM_ALIVIO = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] >= TABELA_DE_ALIVIOS["MIN"]]
                
                if not TIPO_DESC_SATURADOS.empty:

                    TIPO_DESC_SELECIONADO = TIPO_DESC_SATURADOS.loc[TIPO_DESC_SATURADOS["VAGOES"].idxmax()]

                    if TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]
                
                #endregion

                #region ACIMA DO LIMITE MINIMO       
                elif not TIPO_DESC_COM_ALIVIO.empty:
                    TIPO_DESC_SELECIONADO = TIPO_DESC_COM_ALIVIO.loc[TIPO_DESC_COM_ALIVIO["VAGOES"].idxmax()]

                else:
                    return None
                
                #endregion

            #endregion

            #region LINHA OCUPADA
            elif PARAMETROS_LINHA["STATUS"] == "OCUPADO":

                FERROVIA     = PARAMETROS_LINHA["FERROVIA"]
                SEGMENTO     = PARAMETROS_LINHA["SEGMENTO"]

                TABELA_DE_ALIVIOS["VAGOES_NESC."]       = PARAMETROS_LINHA["VAGOES_NECESSÁRIOS"]
                TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"]   = TABELA_DE_ALIVIOS["VAGOES"] - TABELA_DE_ALIVIOS["VAGOES_NESC."]
                TABELA_DE_ALIVIOS["TX_MIN"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
                TABELA_DE_ALIVIOS["TX_MAX"]             = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)

                #ESTE FILTRO IMPEDE QUE VC MISTRURE VAGÕES DE SEGMENTOS OU FERROVIAS DISTINTAS
                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FERROVIA)]
                if len(TABELA_DE_ALIVIOS) == 0: return None 

                #ESTE FILTRO IMPEDE QUE VOCE TENHA VAGOES NEGATIVOS
                TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"] >= 0]
                if len(TABELA_DE_ALIVIOS) == 0: return None 

                ID_LINHA_MAIS_PROXIMA = TABELA_DE_ALIVIOS['DIFERENCA_VAGOES'].idxmin()
                TIPO_DESC_SELECIONADO = TABELA_DE_ALIVIOS.loc[ID_LINHA_MAIS_PROXIMA]
                TIPO_DESC_SELECIONADO["VAGOES"] = TIPO_DESC_SELECIONADO["VAGOES_NESC."]

            TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

            return TIPO_DESC_ESCOLHIDO

            #endregion

        def __GESTAO_DE_FIFO_ESQUERDA__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA_1, PARAMETROS_LINHA_2, PARAMETROS_LINHA_3):
            
            #region JUNTANDO AS POSSIBILIDADES VALONGO E TERMINAIS EM UMA LISTA (x)
            TIPO_DESC_ESCOLHIDO = None
            LINHA = None
            ALIVIAR = False
            
            # MONTANDO LISTA DE ANÁLISE {#6aa84f, 22}
            TABELA_DE_ALIVIOS = pd.DataFrame(columns=["PATIO", "ORIGEM", "SEGMENTO", "FERROVIA", "VAGOES", "MIN", "MAX", "CARREGAGOS"])
            for ALIVIO in VAGOES_NOS_TEMRINAS:

                NOVA_LINHA = {

                    "PATIO":        ALIVIO["PATIO"],
                    "ORIGEM":       ALIVIO["TERMINAL"],
                    "SEGMENTO":     ALIVIO["SEGMENTO"], 
                    "FERROVIA":     ALIVIO["FERROVIA"], 
                    "VAGOES":       ALIVIO["QT_VAZIOS_NO_TERMINAL"], 
                    "MIN":          ALIVIO["MIN"],
                    "MAX":          ALIVIO["MAX"],
                    "CARREGAGOS":   ALIVIO["SALDO"]

                }
                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = NOVA_LINHA
 

            # COLUNAS DE CRITÉRIOS {#355427, 2}
            TABELA_DE_ALIVIOS["TX_MIN"] = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MIN"]).round(2)
            TABELA_DE_ALIVIOS["TX_MAX"] = (TABELA_DE_ALIVIOS["VAGOES"] / TABELA_DE_ALIVIOS["MAX"]).round(2)
            
            
            # ANALISANDO OS ALIVIOS POSSIVEIS {#bcbcbc, 130}
            TABELA_DE_ALIVIOS_BLOCO = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["TX_MIN"] >= 1)]

            # ANALISANDO OS ALIVIOS POSSIVEIS {#bcbcbc, 93}
            if len(TABELA_DE_ALIVIOS_BLOCO) > 0:

                TIPO_DESC_SELECIONADO = TABELA_DE_ALIVIOS_BLOCO.loc[TABELA_DE_ALIVIOS_BLOCO["TX_MIN"].idxmax()]
                TIPO_SELECIONADO      = [TIPO_DESC_SELECIONADO["FERROVIA"], TIPO_DESC_SELECIONADO["SEGMENTO"]]

                L1_STATUS = PARAMETROS_LINHA_1["STATUS"]
                L2_STATUS = PARAMETROS_LINHA_2["STATUS"]
                L3_STATUS = PARAMETROS_LINHA_3["STATUS"]

                L1_TIPO   = [PARAMETROS_LINHA_1["FERROVIA"], PARAMETROS_LINHA_1["SEGMENTO"]]
                L2_TIPO   = [PARAMETROS_LINHA_2["FERROVIA"], PARAMETROS_LINHA_2["SEGMENTO"]]
                L3_TIPO   = [PARAMETROS_LINHA_3["FERROVIA"], PARAMETROS_LINHA_3["SEGMENTO"]]

                L1_COMPATIVEL = (L1_TIPO == TIPO_SELECIONADO and not(L1_STATUS == "LIVRE"))
                L2_COMPATIVEL = (L2_TIPO == TIPO_SELECIONADO and not(L2_STATUS == "LIVRE"))
                L3_COMPATIVEL = (L3_TIPO == TIPO_SELECIONADO and not(L3_STATUS == "LIVRE"))
                
                #LINHA 1 
                if L1_STATUS == "LIVRE" and L2_COMPATIVEL and L3_COMPATIVEL:

                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"] 

                    LINHA = "LINHA_1" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                elif L1_STATUS == "LIVRE" and (not L2_COMPATIVEL) and L3_STATUS == "LIVRE":

                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_1" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()
             
                elif  L1_COMPATIVEL:
                    
                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_1" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()
                
            
                #LINHA 2
                elif (not L1_COMPATIVEL) and L2_STATUS == "LIVRE": #INDEPENDENTE DO QUE L3 SEJA

                    LINHA = "LINHA_2" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                elif (not L1_COMPATIVEL) and L2_COMPATIVEL:

                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_2["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_2["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_2" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                elif L1_STATUS == "LIVRE" and L2_COMPATIVEL:

                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_1["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_2" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                elif L1_STATUS == "LIVRE" and L2_STATUS == "LIVRE" and L3_STATUS == "LIVRE":

                    LINHA = "LINHA_1" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                #LINHA 3
                elif L3_COMPATIVEL        and L1_STATUS == "LIVRE"    and L2_STATUS == "LIVRE":

                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_3["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_3["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_3" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()


                elif L3_COMPATIVEL        and (not L1_COMPATIVEL)     and (not L2_COMPATIVEL):
                    
                    if  TIPO_DESC_SELECIONADO["VAGOES"] > PARAMETROS_LINHA_3["VAGOES_NECESSÁRIOS"]:
                        TIPO_DESC_SELECIONADO["VAGOES"] = PARAMETROS_LINHA_3["VAGOES_NECESSÁRIOS"]

                    LINHA = "LINHA_3" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()

                elif L3_STATUS == "LIVRE" and (not L1_COMPATIVEL)     and (not L2_COMPATIVEL):

                    LINHA = "LINHA_3" 
                    TIPO_DESC_ESCOLHIDO = TIPO_DESC_SELECIONADO.to_dict()
                

            else:
                
                ALIVIOS_FINAIS = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["CARREGAGOS"] == 0]
                
                if len(ALIVIOS_FINAIS) > 0:
                    
                    ALIVIO_SELECIONADO = ALIVIOS_FINAIS.iloc[0]
                    TIPO_DESC_SELECIONADO = [ALIVIO_SELECIONADO["FERROVIA"], ALIVIO_SELECIONADO["SEGMENTO"]]
                    
                    if (ALIVIO_SELECIONADO["FERROVIA"] == "MRS") or (ALIVIO_SELECIONADO["FERROVIA"] == "VLI"):
                        ALIVIAR  = True

                    L1_TIPO   = [PARAMETROS_LINHA_1["FERROVIA"], PARAMETROS_LINHA_1["SEGMENTO"]]
                    L2_TIPO   = [PARAMETROS_LINHA_2["FERROVIA"], PARAMETROS_LINHA_2["SEGMENTO"]]
                    L3_TIPO   = [PARAMETROS_LINHA_3["FERROVIA"], PARAMETROS_LINHA_3["SEGMENTO"]]
                   
                    if TIPO_DESC_SELECIONADO == L1_TIPO: 
                       
                        LINHA = "LINHA_1" 
                        TIPO_DESC_ESCOLHIDO = ALIVIO_SELECIONADO.to_dict()


                    elif TIPO_DESC_SELECIONADO == L2_TIPO: 
                       
                        LINHA = "LINHA_2" 
                        TIPO_DESC_ESCOLHIDO = ALIVIO_SELECIONADO.to_dict()


                    elif TIPO_DESC_SELECIONADO == L3_TIPO: 
                       
                        LINHA = "LINHA_3" 
                        TIPO_DESC_ESCOLHIDO = ALIVIO_SELECIONADO.to_dict()
                   

            return TIPO_DESC_ESCOLHIDO, LINHA, ALIVIAR
        
        ############################################################################################################
     
        def __ATUALIZAR_4000__():

            #region FILTRO
            if  (not"PCX" in self.MODELO_TABELA_VAZIA["DIREITA"]) or (not "DIREITA" in self.MODELO_TABELA_VAZIA): 
                return
            #endregion

            __ATUALIZAR_SALDO_LINHA_4000__("RUMO")
            __ATUALIZAR_SALDO_LINHA_4000__("MRS")
            __ATUALIZAR_SALDO_LINHA_4000__("VLI")

            for i in range(119): 

                #region ANALISAR LINHA

                DADOS_LINHA_NESTA_HORA          = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i + 1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM   = self.INFOS_LINHAS["LINHA_4000"]["ALIVIO"]
                
                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                
                FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                
                if DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":    
                    
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]


                else:

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS["LINHA_4000"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_VALONGO = {

                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA,
                    "VAGOES":               QUANTOS_VAGOES_ESTAO_NA_LINHA
                     
                }
                #endregion

                #region ANALISAR TERMINAIS DE PCX

                VAGOES_NOS_TEMRINAS = []
                for TERMINAL in self.FULL_TABLE["DIREITA"]["PCX"]:                  #NA HORA i ESTOU OLHANDO TODOS  OS TERMINAIS
                    
                    for SEGMENTO in self.FULL_TABLE["DIREITA"]["PCX"][TERMINAL]:    #NA HORA i ESTOU OLHANDO TODOAS AS DESCARGAS DO TERMINAL
                        
                        if not SEGMENTO == "SATURACAO":
                            
                            for FERROVIA in self.FULL_TABLE["DIREITA"]["PCX"][TERMINAL][SEGMENTO]: #E TODAS AS FERROVIAS

                                __ATUALIZAR_SALDO__("DIREITA", "PCX", TERMINAL, SEGMENTO, FERROVIA, i)
                                
                                # AQUI DENTRO ESTAMOS EM UM INSTANTE TAL DENTRO DE UM TERMINAL
                                # PARA ANALIZAR QUE DECISÃO TOMAR
                                # VAMOS VERIFICAR COMO ESTA O TERMINAL

                                QT_VAZIOS_NO_TERMINAL = self.FULL_TABLE["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                
                                SATURACAO_NO_TERMINAL = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]
                                                            
                                #EXISTE UMA QUANTIDADE PRONTA PARA SER ALIVIADA?
                                BLOCO = False
                                if QT_VAZIOS_NO_TERMINAL > 0:
                                    
                                    if QT_VAZIOS_NO_TERMINAL >= SATURACAO_NO_TERMINAL:
                                        BLOCO = True
                                    #ENTAO PODE SER ALIVIADO 

                                     
                                    DADOS = {
                                        "PATIO" :                   "PCX",
                                        "TERMINAL":                 TERMINAL,
                                        "FERROVIA":                 FERROVIA,
                                        "SEGMENTO":                 SEGMENTO,
                                        "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                        "TEMPO":                    i,
                                        "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                        "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"]
                                    }

                                    VAGOES_NOS_TEMRINAS.append(DADOS)
                
                #endregion

                ALIVIO = __GESTAO_DE_FIFO_LINHA_4000__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA_VALONGO)
                
                #NOVO LAYOUT PARA NAO TER DOIS ALIVIOS SIMULTANEOS (DE DOIS TERMINAIS DISTINTOS)
                TEMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS["LINHA_4000"]["TEMPO_ALIVIO"]
                HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                HORA_MAXIA  = HORA_ALIVIO > 120

                RECEBIMENTO_LINHA =  self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO]

                if not ALIVIO == None and not HORA_MAXIA and RECEBIMENTO_LINHA == 0:
               
                    ORIGEM          = ALIVIO["ORIGEM"]
                    SEGMENTO        = ALIVIO["SEGMENTO"]
                    FERROVIA        = ALIVIO["FERROVIA"]
                    LOTE_DE_VAGOES  = ALIVIO["VAGOES"]

                    self.FULL_TABLE["DIREITA"]["PCX"][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                    
                    __ATUALIZAR_SALDO__("DIREITA", "PCX", ORIGEM, SEGMENTO, FERROVIA, i)

                    self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                    self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                    self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                    self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO

                    __ATUALIZAR_SALDO_LINHA_4000__(FERROVIA)
        
                #endregion

        def __ATUALIZAR_VALONGO_FIPS__():
            
            MARGEM = "DIREITA"
            PATIOS = list(self.FULL_TABLE[MARGEM].keys())

            if 'PCX' in PATIOS: PATIOS.remove('PCX')

            __ATUALIZAR_SALDO_LINHA_VALONGO__("RUMO")
            __ATUALIZAR_SALDO_LINHA_VALONGO__("VLI")

            for i in range(119): #ATUALIZANDO VALONGO FIPS
        
                #region ANALISANDO - A LINHA VALONGO
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][i + 1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_VALONGO"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO" 
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_VALONGO"]["TEMPO_ALIVIO"]
                
                PARAMETROS_LINHA_VALONGO = {

                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA

                }
                
                #endregion 
                        
                #region ANALISANDO - TODOS OS TERMINAIS DE PST E PMC
                
                VAGOES_NOS_TEMRINAS = []   
                
                for PATIO in PATIOS:
                    for TERMINAL in self.FULL_TABLE[MARGEM][PATIO]:
                        for SEGMENTO in self.FULL_TABLE[MARGEM][PATIO][TERMINAL]:
                            if not SEGMENTO == "SATURACAO":
                                for FERROVIA in self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO]:
                                    if not FERROVIA == "MRS":    

                                        __ATUALIZAR_SALDO__(MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, i)

                                        QT_VAZIOS_NO_TERMINAL  = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                        SATURACAO__NO_TERMINAL = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]
                                    
                                        
                                        if QT_VAZIOS_NO_TERMINAL > 0:
                                            
                                            DADOS = {
                                                "PATIO" :                   PATIO,
                                                "TERMINAL":                 TERMINAL,
                                                "FERROVIA":                 FERROVIA,
                                                "SEGMENTO":                 SEGMENTO,
                                                "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                                "SATURACAO":                SATURACAO__NO_TERMINAL,
                                                "TEMPO":                    i,
                                                "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                                "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"]
                                            }

                                            VAGOES_NOS_TEMRINAS.append(DADOS)     
                                        

                
                #endregion
                
                #region ANALISANDO - LINHA 4000 (VERIFICA SE SALDO É MINIMO) 

                FERROVIAS_QUE_USAM_VANLONGO = ["RUMO", "VLI"]
                VAGOES_DA_LINHA_4000  = None

                for FERROVIA in FERROVIAS_QUE_USAM_VANLONGO:
                    
                    SALDO_LINHA_4000 = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO"][i]
                    
                    SATURACAO_MINIMA = self.INFOS_LINHAS["LINHA_4000"]["MIN"]
                    SATURACAO_MAXIMA = self.INFOS_LINHAS["LINHA_4000"]["MAX"]

                    FERROVIA_NA_LINHA_4000 = FERROVIA
                    SEGMENTO_NA_LINHA_4000 = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["SEGMENTO"]
                        
                        
                    if SALDO_LINHA_4000 > 0:
                                    
                        VAGOES_DA_LINHA_4000 = {
                            
                            "ORIGEM":   "LINHA_4000",
                            "VAGOES":   SALDO_LINHA_4000,
                            "SEGMENTO": SEGMENTO_NA_LINHA_4000,
                            "FERROVIA": FERROVIA_NA_LINHA_4000,
                            "MIN":      SATURACAO_MINIMA,
                            "MAX":      SATURACAO_MAXIMA 
                        }
                
                #endregion
                    
                ALIVIO = __GESTAO_DE_FIFO_VALONGO_FIPS__(VAGOES_NOS_TEMRINAS, VAGOES_DA_LINHA_4000, PARAMETROS_LINHA_VALONGO)
                
                #region EXECUTAR O ALIVIO
                if not ALIVIO == None:

                    ORIGEM          = ALIVIO["ORIGEM"]
                    SEGMENTO        = ALIVIO["SEGMENTO"]
                    FERROVIA        = ALIVIO["FERROVIA"]
                    PATIO           = ALIVIO["PATIO"]
                    LOTE_DE_VAGOES  = ALIVIO["VAGOES"]

                    if ORIGEM == "LINHA_4000":
                        
                        self.FULL_LINHAS[ORIGEM]["FERROVIAS"][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                        __ATUALIZAR_4000__()
                    
                    else:
                        self.FULL_TABLE["DIREITA"][PATIO][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                        __ATUALIZAR_SALDO__("DIREITA", PATIO, ORIGEM, SEGMENTO, FERROVIA, i)

                    
                    TEMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS["LINHA_VALONGO"]["TEMPO_ALIVIO"]
                    HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                    HORA_MAXIA  = HORA_ALIVIO > 120

                    if not HORA_MAXIA:

                        self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                        self.FULL_LINHAS["LINHA_VALONGO"]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO

                        __ATUALIZAR_SALDO_LINHA_VALONGO__(FERROVIA)

                        SALDO_VALONGO = self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO]
                        TREM_ALIVIO_VALONGO = self.INFOS_LINHAS["LINHA_VALONGO"]["ALIVIO"]

                        if SALDO_VALONGO >= TREM_ALIVIO_VALONGO:
                            self.FULL_LINHAS["LINHA_VALONGO"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_VALONGO
                            __ATUALIZAR_SALDO_LINHA_VALONGO__(FERROVIA)
                #endregion

        def __ATUALIZAR_VALONGO_MRS__():

            MARGEM = "DIREITA"
            PATIOS = list(self.FULL_TABLE[MARGEM].keys())
            if 'PCX' in PATIOS: PATIOS.remove('PCX')

            for i in range(119): #ATUALIZANDO VALONGO MRS

                #region ANALISANDO - A LINHA VALONGO MRS

                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_VALONGO_MRS"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = (QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA)
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_VALONGO_MRS"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_VALONGO = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }
                #endregion 

                #region ANALISANDO - TODOS OS TERMINAIS DE PST E PMC

     
                VAGOES_NOS_TEMRINAS = []  

                for PATIO in PATIOS:
                    for TERMINAL in self.FULL_TABLE[MARGEM][PATIO]:
                        for SEGMENTO in self.FULL_TABLE[MARGEM][PATIO][TERMINAL]:
                            if not SEGMENTO == "SATURACAO":
                                for FERROVIA in self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO]:
                                    if not( FERROVIA == "VLI" or  FERROVIA == "RUMO"):  

                                        __ATUALIZAR_SALDO__(MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, i)

                                        QT_VAZIOS_NO_TERMINAL       = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                        SATURACAO__NO_TERMINAL      = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]
                                        QT_CARREGAGOS_NO_TERMINAL   = self.FULL_TABLE["DIREITA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO"][i]
                                        
                                        #TESTE PARA FIFO
                                        if QT_VAZIOS_NO_TERMINAL > 0:

                                            DADOS = {
                                                "PATIO" :                   PATIO,
                                                "TERMINAL":                 TERMINAL,
                                                "FERROVIA":                 FERROVIA,
                                                "SEGMENTO":                 SEGMENTO,
                                                "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                                "SATURACAO":                SATURACAO__NO_TERMINAL,
                                                "TEMPO":                    i,
                                                "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                                "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"],
                                                "SALDO":                    QT_CARREGAGOS_NO_TERMINAL     
                                            }

                                            VAGOES_NOS_TEMRINAS.append(DADOS)     
                                        
                
                #endregion
                
                #region ANALISANDO - LINHA 4000 (VERIFICA SE SALDO É MINIMO) 

                FERROVIAS_QUE_USAM_VANLONGO = ["MRS"] #ESTA ASSIM POIS FOI COPIADO DE CIMA
                VAGOES_DA_LINHA_4000  = None

                for FERROVIA in FERROVIAS_QUE_USAM_VANLONGO:
                    SALDO_LINHA_4000 = self.FULL_LINHAS["LINHA_4000"]["FERROVIAS"][FERROVIA]["SALDO"][i]
                    
                    QUANTO_A_LINHA_PODE_ALIVIAR = self.INFOS_LINHAS["LINHA_4000"]["ALIVIO"]
                    SATURACAO_MINIMA = self.INFOS_LINHAS["LINHA_4000"]["MIN"]
                    SATURACAO_MAXIMA = self.INFOS_LINHAS["LINHA_4000"]["MAX"]

                    if SALDO_LINHA_4000 >= QUANTO_A_LINHA_PODE_ALIVIAR:

                        FERROVIA_NA_LINHA_4000 = FERROVIA
                        VAGOES_DA_4000_ALIVIO  = QUANTO_A_LINHA_PODE_ALIVIAR
                        SEGMENTO_NA_LINHA_4000 = self.FULL_LINHAS["LINHA_4000"]["OCUPACAO"][i]["SEGMENTO"]
                        
            ########################ESTAMOS ANALISANDO ISSO AQUI################################    
                
                        if SALDO_LINHA_4000 > 0:
                                        
                            VAGOES_DA_LINHA_4000 = {
                                
                                "ORIGEM":   "LINHA_4000",
                                "VAGOES":   VAGOES_DA_4000_ALIVIO,
                                "SEGMENTO": SEGMENTO_NA_LINHA_4000,
                                "FERROVIA": FERROVIA_NA_LINHA_4000,
                                "MIN":      SATURACAO_MINIMA,
                                "MAX":      SATURACAO_MAXIMA 
                            }
                
                #endregion

                FIFO = __GESTAO_DE_FIFO_VALONGO_MRS__(VAGOES_NOS_TEMRINAS, VAGOES_DA_LINHA_4000, PARAMETROS_LINHA_VALONGO)
                ALIVIO = FIFO[0]
                ALIVIAR_LINHA = FIFO[1]




                #region EXECUTAR O ALIVIO
                if not ALIVIO == None:

                    ORIGEM          = ALIVIO["ORIGEM"]
                    SEGMENTO        = ALIVIO["SEGMENTO"]
                    FERROVIA        = ALIVIO["FERROVIA"]
                    PATIO           = ALIVIO["PATIO"]
                    LOTE_DE_VAGOES  = ALIVIO["VAGOES"]

                    if ORIGEM == "LINHA_4000":
                        
                        self.FULL_LINHAS[ORIGEM]["FERROVIAS"][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                        __ATUALIZAR_SALDO_LINHA_4000__(FERROVIA)
                    
                    else:
                        self.FULL_TABLE["DIREITA"][PATIO][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                        __ATUALIZAR_SALDO__("DIREITA", PATIO, ORIGEM, SEGMENTO, FERROVIA, i)

                    
                    TEMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS["LINHA_VALONGO_MRS"]["TEMPO_ALIVIO"]
                    HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                    HORA_MAXIA  = HORA_ALIVIO > 120

                    if not HORA_MAXIA:

                        self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                        self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                        self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                        self.FULL_LINHAS["LINHA_VALONGO_MRS"]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO

                        __ATUALIZAR_SALDO_LINHA_VALONGO_MRS__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False)

                        SALDO_VALONGO = self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO]
                        TREM_ALIVIO_VALONGO = self.INFOS_LINHAS["LINHA_VALONGO_MRS"]["ALIVIO"]

                        if ALIVIAR_LINHA:
                            self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_VALONGO
                            __ATUALIZAR_SALDO_LINHA_VALONGO_MRS__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False)

                        elif SALDO_VALONGO >= TREM_ALIVIO_VALONGO:
                            
                            self.FULL_LINHAS["LINHA_VALONGO_MRS"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_VALONGO
                            __ATUALIZAR_SALDO_LINHA_VALONGO_MRS__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False)
                #endregion
                
        def __ATUALIZAR_LINHA_1__():


            __ATUALIZAR_SALDO_LINHA_1__("RUMO")
            __ATUALIZAR_SALDO_LINHA_1__("MRS")
            __ATUALIZAR_SALDO_LINHA_1__("VLI")

            

            for i in range(119):

                #region ANALISANDO - A LINHA 1   
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_1"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""
                    SEGMENTO_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    SEGMENTO_NA_LINHA = DADOS_LINHA_NESTA_HORA["SEGMENTO"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_1"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_1 = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }

                #endregion

                #region ANALISANDO - TODOS OS TERMINAIS DE PCZ

                VAGOES_NOS_TEMRINAS = []
                for TERMINAL in self.FULL_TABLE["ESQUERDA"]["PCZ"]:
                    for SEGMENTO in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL]:
                        if not SEGMENTO == "SATURACAO":
                            for FERROVIA in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO]:

                                __ATUALIZAR_SALDO__("ESQUERDA", "PCZ", TERMINAL, SEGMENTO, FERROVIA, i)

                                QT_VAZIOS_NO_TERMINAL  = self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                SATURACAO__NO_TERMINAL = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]

                                if QT_VAZIOS_NO_TERMINAL > 0:
                                            
                                    DADOS = {
                                        "PATIO" :                   "PCZ",
                                        "TERMINAL":                 TERMINAL,
                                        "FERROVIA":                 FERROVIA,
                                        "SEGMENTO":                 SEGMENTO,
                                        "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                        "SATURACAO":                SATURACAO__NO_TERMINAL,
                                        "TEMPO":                    i,
                                        "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                        "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"]
                                    }

                                    VAGOES_NOS_TEMRINAS.append(DADOS)

                #endregion

                ALIVIO = __GESTAO_DE_FIFO_LINHA_1__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA_1)
                
                #region EXECUTAR O ALIVIO
                if not ALIVIO == None:
                    
                    ORIGEM          = ALIVIO["ORIGEM"]
                    SEGMENTO        = ALIVIO["SEGMENTO"]
                    FERROVIA        = ALIVIO["FERROVIA"]
                    PATIO           = ALIVIO["PATIO"]
                    LOTE_DE_VAGOES  = ALIVIO["VAGOES"]

                    self.FULL_TABLE["ESQUERDA"]["PCZ"][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                    __ATUALIZAR_SALDO__("ESQUERDA", PATIO, ORIGEM, SEGMENTO, FERROVIA, i)

                    HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                    HORA_MAXIA  = HORA_ALIVIO > 120
                    
                    if not HORA_MAXIA:

                        self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                        self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO
                        
                        __ATUALIZAR_SALDO_LINHA_1__(FERROVIA)

                        SALDO_VALONGO       = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO]
                        TREM_ALIVIO_VALONGO = self.INFOS_LINHAS["LINHA_1"]["ALIVIO"]

                        if SALDO_VALONGO >= TREM_ALIVIO_VALONGO:
                            self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_VALONGO
                            __ATUALIZAR_SALDO_LINHA_1__(FERROVIA)

                #endregion

        def __ATUALIZAR_LINHA_2__():

            for i in range(119):

                #region ANALISANDO - A LINHA 2   
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_2"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""
                    SEGMENTO_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    SEGMENTO_NA_LINHA = DADOS_LINHA_NESTA_HORA["SEGMENTO"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_2"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_2 = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }

                #endregion

                #region ANALISANDO - TODOS OS TERMINAIS DE PCZ

                VAGOES_NOS_TEMRINAS = []
                for TERMINAL in self.FULL_TABLE["ESQUERDA"]["PCZ"]:
                    for SEGMENTO in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL]:
                        if not SEGMENTO == "SATURACAO":
                            for FERROVIA in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO]:

                                __ATUALIZAR_SALDO__("ESQUERDA", "PCZ", TERMINAL, SEGMENTO, FERROVIA, i)

                                QT_VAZIOS_NO_TERMINAL  = self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                SATURACAO__NO_TERMINAL = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]
                                QT_ALIVIO_NO_TERMINAL  = self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"][i]  

                                if (QT_VAZIOS_NO_TERMINAL > 0 and QT_ALIVIO_NO_TERMINAL == 0):
                                            
                                    DADOS = {
                                        "PATIO" :                   "PCZ",
                                        "TERMINAL":                 TERMINAL,
                                        "FERROVIA":                 FERROVIA,
                                        "SEGMENTO":                 SEGMENTO,
                                        "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                        "SATURACAO":                SATURACAO__NO_TERMINAL,
                                        "TEMPO":                    i,
                                        "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                        "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"]
                                    }
 
                                    VAGOES_NOS_TEMRINAS.append(DADOS)

                #endregion

                ALIVIO = __GESTAO_DE_FIFO_LINHA_2__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA_2)

                #region EXECUTAR O ALIVIO

                if not ALIVIO == None:

                    ORIGEM          = ALIVIO["ORIGEM"]
                    SEGMENTO        = ALIVIO["SEGMENTO"]
                    FERROVIA        = ALIVIO["FERROVIA"]
                    PATIO           = ALIVIO["PATIO"]
                    LOTE_DE_VAGOES  = ALIVIO["VAGOES"]

                    self.FULL_TABLE["ESQUERDA"]["PCZ"][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                    __ATUALIZAR_SALDO__("ESQUERDA", PATIO, ORIGEM, SEGMENTO, FERROVIA, i)

                    EMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS["LINHA_2"]["TEMPO_ALIVIO"]
                    HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                    HORA_MAXIA  = HORA_ALIVIO > 120

                    if not HORA_MAXIA:

                        self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                        self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO

                        __ATUALIZAR_SALDO_LINHA_2__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False)

                        SALDO_VALONGO       = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO]
                        TREM_ALIVIO_VALONGO = self.INFOS_LINHAS["LINHA_2"]["ALIVIO"]

                        if SALDO_VALONGO >= TREM_ALIVIO_VALONGO:
                            self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_VALONGO
                            __ATUALIZAR_SALDO_LINHA_2__(SEGMENTO, FERROVIA, HORA_ALIVIO, FORCAR_ALIVIO=False)

                #endregion

        ############################################################################################################

        def __ATUALIZAR_SALDO__(MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, HORA):
            
            RECEBIDOS       = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["PRODUTIVIDADE"][HORA]

            if HORA > 0:
                SALDO_ANTERIOR  = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][HORA-1]
                ALIVIO          = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO"][HORA-1]
                CONTADOR_FILA   = self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"][HORA - 1][1]
            else:
                SALDO_ANTERIOR  = int(self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[0]][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VIRADA_VAZIOS"])
                ALIVIO          = 0
                CONTADOR_FILA   = 0

            
            SALDO_ATUAL     = RECEBIDOS + SALDO_ANTERIOR - ALIVIO
            
            self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][HORA] = SALDO_ATUAL

            if SALDO_ATUAL == SALDO_ANTERIOR and not (SALDO_ATUAL == 0) and HORA < 24: 

                self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"][HORA - 1]   = ["P", CONTADOR_FILA]
                self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"][HORA]       = ["P", CONTADOR_FILA + 1]

            else:

                self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["CONTADOR_FILA_DE_VAZIOS"][HORA]    = [0, 0]

        def __CALCULAR_MARGEM_DIREITA__():
      
        #############################################################################################################

            __ATUALIZAR_4000__()

            __ATUALIZAR_VALONGO_FIPS__() 

            __ATUALIZAR_VALONGO_MRS__()

        def __CALCULAR_MARGEM_ESQUERDA__():

            #region FILTRO
            if  (not"PCZ" in self.MODELO_TABELA_VAZIA["ESQUERDA"]) or (not "ESQUERDA" in self.MODELO_TABELA_VAZIA): 
                return
            #endregion

            #ANALISAR TERMINAIS

            # ATUALIZANDO TERMINAIS {#3ec1d5, 8}
            FERROVIAS = ["RUMO", "MRS", "VLI"]

            for FERROVIA in FERROVIAS:
                
                __ATUALIZAR_SALDO_LINHA_1__(FERROVIA)
                __ATUALIZAR_SALDO_LINHA_2__(FERROVIA)
                __ATUALIZAR_SALDO_LINHA_3__(FERROVIA)

            
            #DECIDIR EM QUAL LINHA JOGAR 

            # ANALISANDO OS ALIVIOS POSSIVEIS {#bcbcbc, 165}
            for i in range(119):
              
                # ANALISANDO LINHA 01 {#bcbcbc, 25}   
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_1"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_1"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_1"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_1"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_1 = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }


                # ANALISANDO LINHA 02 {#bcbcbc, 25} 
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_2"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_2"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_2"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_2"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_2 = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }


                # ANALISANDO LINHA 03 {#bcbcbc, 25}
                DADOS_LINHA_NESTA_HORA        = self.FULL_LINHAS["LINHA_3"]["OCUPACAO"][i+1]    
                QUANTOS_VAGOES_FORMAM_UM_TREM = self.INFOS_LINHAS["LINHA_3"]["ALIVIO"]

                #SO EXISES AS OPCOES "LIVRE" E "OCUPADO"
                if   DADOS_LINHA_NESTA_HORA["STATUS"] == "LIVRE":               

                    QUANTOS_VAGOES_ESTAO_NA_LINHA = 0
                    FERROVIA_NA_LINHA = ""

                if  DADOS_LINHA_NESTA_HORA["STATUS"] == "OCUPADO":

                    FERROVIA_NA_LINHA = DADOS_LINHA_NESTA_HORA["FERROVIA"]
                    QUANTOS_VAGOES_ESTAO_NA_LINHA = self.FULL_LINHAS["LINHA_3"]["FERROVIAS"][FERROVIA_NA_LINHA]["SALDO"][i+1]

                QUANTOS_VAGOES_A_LINHA_PRECISA  = QUANTOS_VAGOES_FORMAM_UM_TREM - QUANTOS_VAGOES_ESTAO_NA_LINHA
                TEMPO_DE_ALIVIO_PARA_A_LINHA    = self.INFOS_LINHAS["LINHA_3"]["TEMPO_ALIVIO"]

                PARAMETROS_LINHA_3 = {
                    "STATUS":               DADOS_LINHA_NESTA_HORA["STATUS"], 
                    "FERROVIA":             FERROVIA_NA_LINHA,
                    "SEGMENTO":             DADOS_LINHA_NESTA_HORA["SEGMENTO"],      
                    "VAGOES_NECESSÁRIOS":   QUANTOS_VAGOES_A_LINHA_PRECISA,
                    "SLA":                  TEMPO_DE_ALIVIO_PARA_A_LINHA
                }


                # ANALISANDO OS TERMINAIS {#bcbcbc, 33}
                VAGOES_NOS_TEMRINAS = []

                for TERMINAL in self.FULL_TABLE["ESQUERDA"]["PCZ"]:

                    for SEGMENTO in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL]:

                        if not SEGMENTO == "SATURACAO":
                            
                            for FERROVIA in self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO]:

                                __ATUALIZAR_SALDO__("ESQUERDA", "PCZ", TERMINAL, SEGMENTO, FERROVIA, i)

                                QT_VAZIOS_NO_TERMINAL       = self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VAZIO"][i]
                                QT_CARREGAGOS_NO_TERMINAL   = self.FULL_TABLE["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SALDO"][i]
                                SATURACAO__NO_TERMINAL      = self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"]

                                if QT_VAZIOS_NO_TERMINAL > 0:
                                            
                                    DADOS = {
                                        "PATIO" :                   "PCZ",
                                        "TERMINAL":                 TERMINAL,
                                        "FERROVIA":                 FERROVIA,
                                        "SEGMENTO":                 SEGMENTO,
                                        "QT_VAZIOS_NO_TERMINAL":    QT_VAZIOS_NO_TERMINAL,
                                        "SATURACAO":                SATURACAO__NO_TERMINAL,
                                        "TEMPO":                    i,
                                        "MIN":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MIN"],
                                        "MAX":                      self.TERMIAIS_VAZIOS[self.LISTA_DATA_ARQ[1]]["ESQUERDA"]["PCZ"][TERMINAL][SEGMENTO][FERROVIA]["SATURACAO"]["MAX"],
                                        "SALDO":                    QT_CARREGAGOS_NO_TERMINAL                   
                                    }

                                    VAGOES_NOS_TEMRINAS.append(DADOS)

                    
                
                # TOMANDO A DECISÃO {#45818e, 6}
                FIFO = __GESTAO_DE_FIFO_ESQUERDA__(VAGOES_NOS_TEMRINAS, PARAMETROS_LINHA_1, PARAMETROS_LINHA_2, PARAMETROS_LINHA_3)

                ALIVIO  = FIFO[0]
                LINHA   = FIFO[1]
                ALIVIAR = FIFO[2]

                
                
                if (not ALIVIO == None): 

                    #NOVO LAYOUT PARA NAO TER DOIS ALIVIOS SIMULTANEOS (DE DOIS TERMINAIS DISTINTOS)
                    TEMPO_DE_ALIVIO_PARA_A_LINHA = self.INFOS_LINHAS[LINHA]["TEMPO_ALIVIO"]
                    HORA_ALIVIO = i + TEMPO_DE_ALIVIO_PARA_A_LINHA
                    HORA_MAXIA  = HORA_ALIVIO > 120
                    RECEBIMENTO_LINHA = self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO]

                    if (not HORA_MAXIA) and (RECEBIMENTO_LINHA == 0):
                                                
                        ORIGEM          = ALIVIO["ORIGEM"]
                        SEGMENTO        = ALIVIO["SEGMENTO"]
                        FERROVIA        = ALIVIO["FERROVIA"]
                        LOTE_DE_VAGOES  = ALIVIO["VAGOES"]  

                        self.FULL_TABLE["ESQUERDA"]["PCZ"][ORIGEM][SEGMENTO][FERROVIA]["ALIVIO"][i] = LOTE_DE_VAGOES
                        
                        __ATUALIZAR_SALDO__("ESQUERDA", "PCZ", ORIGEM, SEGMENTO, FERROVIA, i)

                        self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["RECEBIDOS"][HORA_ALIVIO] = LOTE_DE_VAGOES
                        self.FULL_LINHAS[LINHA]["OCUPACAO"][HORA_ALIVIO]["STATUS"]   = "OCUPADO"
                        self.FULL_LINHAS[LINHA]["OCUPACAO"][HORA_ALIVIO]["FERROVIA"] = FERROVIA
                        self.FULL_LINHAS[LINHA]["OCUPACAO"][HORA_ALIVIO]["SEGMENTO"] = SEGMENTO
                        
                        __ATUALIZAR_SALDO_LINHA_PCZ__(LINHA, FERROVIA)

                        SALDO_NA_LINHA = self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["SALDO"][HORA_ALIVIO]
                        QT_FORMA_TREM  = self.INFOS_LINHAS[LINHA]["ALIVIO"]
                       
                        if ALIVIAR: 
                            self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_NA_LINHA
                            __ATUALIZAR_SALDO_LINHA_PCZ__(LINHA, FERROVIA)
                                                          
                        elif SALDO_NA_LINHA >= QT_FORMA_TREM:

                            self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA]["ALIVIO"][HORA_ALIVIO] = SALDO_NA_LINHA
                            __ATUALIZAR_SALDO_LINHA_PCZ__(LINHA, FERROVIA)               
  
    def __SEPARAR_FULL__(self):

        #region VOLTANDO DIVIDINDO A LINHA_FULL UNICA NAS LINHAS DIARIAS
        ITENS_DAS_LINHAS = ["RECEBIDOS", "SALDO", "SEGMENTO", "ALIVIO", "SAIDA"]
        FERROVIAS        = ["RUMO", "MRS", "VLI"]
        
        DIRETORIO_LINHAS = "previsao_trens/src/OPERACAO/LINHAS_VAZIOS"
        LINHAS = (os.listdir(DIRETORIO_LINHAS))
        
        LISTAS = {}
        
        #PASSANDO AS INFORMAÇÕES PARA LISTA
        for LINHA in LINHAS:
            LISTAS[LINHA] = {}

            for FERROVIA in FERROVIAS:
                LISTAS[LINHA][FERROVIA] = {}

                for ITEM in ITENS_DAS_LINHAS:
                    LISTAS[LINHA][FERROVIA][ITEM] = []
                
                    
                for ITEM in ITENS_DAS_LINHAS:
                    LISTAS[LINHA][FERROVIA][ITEM] = [self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA][ITEM][i:i + 24] for i in range(0, len(self.FULL_LINHAS[LINHA]["FERROVIAS"][FERROVIA][ITEM]), 24)]
        
            LISTAS[LINHA]["OCUPACAO"] = [self.FULL_LINHAS[LINHA]["OCUPACAO"][i:i + 24] for i in range(0, len(self.FULL_LINHAS[LINHA]["OCUPACAO"]), 24)]
        
        #PASSANDO DA LISTA PARA O DICIONARIO
        for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):
            for LINHA in LINHAS:
                for FERROVIA in FERROVIAS:
                    for ITEM in ITENS_DAS_LINHAS:

                        self.LINHAS[DATA_ARQ][LINHA]["FERROVIAS"][FERROVIA][ITEM] = LISTAS[LINHA][FERROVIA][ITEM][index]

                #FULL_LINHA_400["OCUPACAO"].extend(self.LINHAS[DATA_ARQ]["LINHA_4000"]["OCUPACAO"])
                self.LINHAS[DATA_ARQ][LINHA]["OCUPACAO"] =  LISTAS[LINHA]["OCUPACAO"][index]        
        #endregion

        #region VOLTANDO DIVIDINDO OS TERMINAIS

        ITENS_CALCULADOS = ["GERACAO_VAZIO", "ALIVIO", "SALDO_VAZIO", "CONTADOR_FILA_DE_VAZIOS"]
        LISTAS = {}

        for MARGEM in self.TERMIAIS_VAZIOS[DATA_ARQ]:
            LISTAS[MARGEM] = {}

            for PATIO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]:
                LISTAS[MARGEM][PATIO] = {}

                for TERMINAL in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]:
                    LISTAS[MARGEM][PATIO][TERMINAL] = {}   
                    
                    for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]:
                        if not SEGMENTO == "SATURACAO":
                            LISTAS[MARGEM][PATIO][TERMINAL][SEGMENTO] = {}                                 

                            for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]:
                                LISTAS[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA] = {} 
                            
                                for ITEM in ITENS_CALCULADOS:
                                    LISTAS[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][ITEM] = [self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][ITEM][i:i + 24] for i in range(0, len(self.FULL_TABLE[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][ITEM]), 24)]

    
        for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):
            for MARGEM in self.TERMIAIS_VAZIOS[DATA_ARQ]:
                for PATIO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM]:
                    for TERMINAL in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO]:
                        for SEGMENTO in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL]:
                            if not SEGMENTO == "SATURACAO":
                                for FERROVIA in self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO]:
                                    for ITEM in ITENS_CALCULADOS:
                                        self.TERMIAIS_VAZIOS[DATA_ARQ][MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][ITEM] = LISTAS[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][ITEM][index] #LISTA POSSUI O MESMO TAMANHO QUE O PERIODO ATIVO, COMPARTILHAM O INDEX

        #endregion

    def ATUALIZAR(self):

        self.__CRIAR_TABELAS__()        # CRIA A TABELAS PARA TODOS OS TERMINAIS, DIVIDINDO A FERROVIA E O SEGMENTO, CRIA AS LINHAS E AJUDAS A ADM.
        
        self.__CRIAR_TABELAS_FULL__()   # DEIXEI ISTO A PARTE PARA NAS FUTURAS MANUTENÇÃO TERMOS UM CONTROLE MELHOR DO QUE ESTAMOS FAZENDO.

        self.__CALCULAR__() 

        self.__SEPARAR_FULL__()

        self.__SALVAR__()


def editarSaldoViradaVazios(PARAMETROS):

    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
    PERIODO_VIGENTE   = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
    LISTA_DATA_ARQ    = PERIODO_VIGENTE["DATA_ARQ"].tolist()
    DATA_ARQ          = LISTA_DATA_ARQ[0]
    
    if PARAMETROS["TERMINAL"] == "ADM": PARAMETROS["TERMINAL"] = "MOEGA V"

    DIRETORIO_DESCARGA = f"previsao_trens/src/DESCARGAS/{ PARAMETROS["TERMINAL"] }/descarga_{ DATA_ARQ }.json"

    with open(DIRETORIO_DESCARGA) as ARQUIVO_DESCARGA:
        JSON_DESCARGA = json.load(ARQUIVO_DESCARGA)

    JSON_DESCARGA["INDICADORES"]["SALDO_DE_VIRADA_VAZIOS"][PARAMETROS['FERROVIA']] = PARAMETROS['NOVO_VALOR']

    with open(DIRETORIO_DESCARGA, 'w') as ARQUIVO_NOME:
        json.dump(JSON_DESCARGA, ARQUIVO_NOME, indent=4)

    return



def editarSaldoViradaVaziosNaLinha(PARAMETROS): 

    PERIODO_VIGENTE   = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", encoding='utf-8-sig', sep=';', index_col=0)
    PERIODO_VIGENTE   = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
    LISTA_DATA_ARQ    = PERIODO_VIGENTE["DATA_ARQ"].tolist()
    DATA_ARQ          = LISTA_DATA_ARQ[0]

    DIRETORIO_LINHAS = f"previsao_trens/src/OPERACAO/LINHAS_VAZIOS/{ PARAMETROS['LINHA'] }/subida_{ DATA_ARQ }.json"

    with open(DIRETORIO_LINHAS) as ARQUIVO_LINHA:
        LINHA = json.load(ARQUIVO_LINHA)

    LINHA["FERROVIAS"][PARAMETROS['FERROVIA']]["SALDO_DE_VIRADA_VAZIOS"]["VAGOES"]   = PARAMETROS['VAGOES']
    LINHA["FERROVIAS"][PARAMETROS['FERROVIA']]["SALDO_DE_VIRADA_VAZIOS"]["SEGMENTO"] = PARAMETROS['SEGMENTO']
    LINHA["FERROVIAS"][PARAMETROS['FERROVIA']]["SALDO_DE_VIRADA_VAZIOS"]["FERROVIA"] = PARAMETROS['FERROVIA']
    
    if int(PARAMETROS['VAGOES']) > 0:
        LINHA["FERROVIAS"][PARAMETROS['FERROVIA']]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"] = "OCUPADO"

    else:
        LINHA["FERROVIAS"][PARAMETROS['FERROVIA']]["SALDO_DE_VIRADA_VAZIOS"]["STATUS"] = "LIVRE"

    with open(DIRETORIO_LINHAS, 'w') as ARQUIVO_NOME:
        json.dump(LINHA, ARQUIVO_NOME, indent=4)