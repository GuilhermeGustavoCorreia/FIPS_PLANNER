    
import os
import json
import pandas as pd


DIRETORIO_SUBIDA    = "previsao_trens/src/SUBIDA"
CHAVES_SUBIDA       = ["SALDO_NAVEGACAO",   "GERACAO_DE_VAZIOS",    "GERACAO_EDITADA",  "ALIVIO_DE_VAZIOS", "ALIVIO_EDITADO", "SALDO_DE_VAZIOS" ]
CHAVES_L4K          = ["GERACAO_DE_VAZIOS", "GERACAO_EDITADA",      "ALIVIO_DE_VAZIOS", "ALIVIO_EDITADO",   "SALDO_DE_VAZIOS"]
CHAVES_OCUPACAO_L4K = ["FERROVIA", "SEGMENTO", "LOTE_COMPLETO"]
CHAVES_CONDENSADOS  = ["GRAO", "FERTILIZANTE", "CELULOSE", "ACUCAR", "CONTEINER"]
CHAVES_BUFFERS      = ["SALDO"]


class CALCULAR_SALDO: #INSERE DOS TERMINAIS PARA OS TOTAIS POR FERROVIA

    def __init__(self):

        with open(os.path.join(DIRETORIO_SUBIDA, "PARAMETROS/TERMINAIS_ESPECIAIS.json")) as ARQUIVO: 
            self.TERMINAIS_ESPECIAIS = json.load(ARQUIVO)
        
        with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO:
            self.INFOS = json.load(ARQUIVO)

        with open(os.path.join(DIRETORIO_SUBIDA, "PARAMETROS/LINHAS.json")) as ARQUIVO: 
            self.INFOS_LINHAS = json.load(ARQUIVO)

        self.TERMINAIS_SUBIDA = os.listdir(os.path.join(DIRETORIO_SUBIDA, "TERMINAIS_SUBIDA")) 

        self.PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        self.PERIODO_VIGENTE = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0])
        self.LISTA_DATA_ARQ  = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()
            
        self.TERMINAIS_DO_CALCULO       = [item for item in self.TERMINAIS_SUBIDA if item not in self.TERMINAIS_ESPECIAIS["DESCONSIDERAR"]["CALCULO_SUBIDA"]]
        
        self.full_TERMINAIS_DO_CALCULO  = {}
        self.full_L4K                   = {"SUBIDA": {}, "OCUPACAO": {}}
        self.full_CONDENSADOS           = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}},    "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}}}
        self.full_BUFFERS               = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}},                  "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}}}

        self.jsL4K          = {}
        self.jsSUBIDAS      = {}
        self.jsCONDENSADOS  = {}
        self.jsBUFFERS      = {} 

    def __MONTAR_FULL__(self): #e abrir arquivos tbm :)

        #region MONTANDO TERMINAIS_SUBIDA   (full)

        for TERMINAL in self.TERMINAIS_DO_CALCULO:
            
            try:    
            
                SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                PATIO     = self.INFOS[TERMINAL]["PATIO"]
                MARGEM    = self.INFOS[TERMINAL]["MARGEM"]
                SATURACAO = self.INFOS[TERMINAL]["SATURACAO_VAZIO"]
            
            except KeyError:
                
                SEGMENTO  = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SEGMENTO"]
                FERROVIAS = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["FERROVIA"]
                PATIO     = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]
                MARGEM    = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["MARGEM"]
                SATURACAO = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SATURACAO_VAZIO"]

            self.jsSUBIDAS[TERMINAL] = {}
            self.jsSUBIDAS[TERMINAL]["SATURACAO_VAZIO"] = SATURACAO

            if not MARGEM   in self.full_TERMINAIS_DO_CALCULO:                             self.full_TERMINAIS_DO_CALCULO[MARGEM]                              = {}
            if not PATIO    in self.full_TERMINAIS_DO_CALCULO[MARGEM]:                     self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO]                       = {}
            if not TERMINAL in self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO]:              self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL]             = {}
            if not SEGMENTO in self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL]:    self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO]   = {}

            for FERROVIA in FERROVIAS:

                if not FERROVIA in self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO]: self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA] = {}
                
                for CHAVE in CHAVES_SUBIDA:

                    self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][CHAVE] = []

                    for DATA_ARQ in self.LISTA_DATA_ARQ:

                        
                        with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{TERMINAL}/subida_{DATA_ARQ}.json") as ARQUIVO:
                            self.jsSUBIDAS[TERMINAL][DATA_ARQ] = json.load(ARQUIVO)

                        if DATA_ARQ == self.LISTA_DATA_ARQ[0]:
                            self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VIRADA"] = self.jsSUBIDAS[TERMINAL][DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_VIRADA"]

                        self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][CHAVE].extend(self.jsSUBIDAS[TERMINAL][DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO][CHAVE])


        #endregion

        #region MONTANDO L4K                (full)

        SEGMENTOS = self.INFOS_LINHAS["LINHA_4K"]["SEGMENTOS"]
        FERROVIAS = self.INFOS_LINHAS["LINHA_4K"]["FERROVIAS"]
        
        for FERROVIA in FERROVIAS:
        
            if not FERROVIA in self.full_L4K["SUBIDA"]: self.full_L4K["SUBIDA"][FERROVIA] = {}
        
            for SEGMENTO in SEGMENTOS:

                if not SEGMENTO in self.full_L4K["SUBIDA"][FERROVIA]: self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO] = {}

                for CHAVE in CHAVES_L4K:

                    self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO][CHAVE] = []

                    for DATA_ARQ in self.LISTA_DATA_ARQ:

                        if not DATA_ARQ in self.jsL4K:
                            with open(f"previsao_trens/src/SUBIDA/LINHAS/LINHA_4K/linha_4k_{ DATA_ARQ }.json") as ARQUIVO:
                                self.jsL4K[DATA_ARQ] = json.load(ARQUIVO)

                        if DATA_ARQ == self.LISTA_DATA_ARQ[0]:
                            self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_VIRADA"] = self.jsL4K[DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_VIRADA"]


                        self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO][CHAVE].extend(self.jsL4K[DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO][CHAVE])

                #ISTO É PARA IMPEDIR QUE ALIVIOS DE CALCULOS PASSADOS SEJAM INSERIDOS NO CALCULO NOVO (QUE SERÁ FEITO NA __CALCULAR__)
                self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = [0] * 144 
                self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["ALIVIO_DE_VAZIOS"]  = [0] * 144 

        for ITEM in CHAVES_OCUPACAO_L4K:

            self.full_L4K["OCUPACAO"][ITEM] = []

            for DATA_ARQ in self.LISTA_DATA_ARQ:

                self.full_L4K["OCUPACAO"][ITEM].extend(self.jsL4K[DATA_ARQ]["OCUPACAO"][ITEM])

                

        #endregion

        #region MONTANDO CONDENSADOS        (full)

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json") as ARQUIVO:
                self.jsCONDENSADOS[DATA_ARQ] = json.load(ARQUIVO)

        for MARGEM in list(self.full_CONDENSADOS.keys()):

            for FERROVIA in ["RUMO", "MRS", "VLI"]:     

                for CHAVE in CHAVES_CONDENSADOS:
                  
                    if not CHAVE in self.full_CONDENSADOS[MARGEM][FERROVIA]: 
                        self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE] = {"SALDO": [0] * 144, "SALDO_VIRADA": self.jsCONDENSADOS[self.LISTA_DATA_ARQ[0]][MARGEM][FERROVIA][CHAVE]["SALDO_VIRADA"]}
                    
          
                    if not CHAVE in self.full_CONDENSADOS[MARGEM]["SAIDAS"]: self.full_CONDENSADOS[MARGEM]["SAIDAS"][CHAVE] = []
                    
                    for DATA_ARQ in self.LISTA_DATA_ARQ:

                        self.full_CONDENSADOS[MARGEM]["SAIDAS"][CHAVE].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM]["SAIDAS"][CHAVE])  

                for DATA_ARQ in self.LISTA_DATA_ARQ:
                    
                    if not "FERROVIA" in self.full_CONDENSADOS[MARGEM]["SAIDAS"]: self.full_CONDENSADOS[MARGEM]["SAIDAS"]["FERROVIA"] = []  
                    self.full_CONDENSADOS[MARGEM]["SAIDAS"]["FERROVIA"].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM]["SAIDAS"]["FERROVIA"])

        
        #endregion

        #region MONTANDO BUFFERS            (full)

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/SUBIDA/BUFFER/buffer_{ DATA_ARQ }.json") as ARQUIVO:
                self.jsBUFFERS[DATA_ARQ] = json.load(ARQUIVO)

            for MARGEM in ["DIREITA", "ESQUERDA"]:  
                for FERROVIA in ["RUMO", "MRS", "VLI"]: 
                    for CHAVE in CHAVES_BUFFERS:

                        if not CHAVE in self.full_BUFFERS[MARGEM][FERROVIA]: self.full_BUFFERS[MARGEM][FERROVIA][CHAVE] = []
                        self.full_BUFFERS[MARGEM][FERROVIA][CHAVE].extend(self.jsBUFFERS[DATA_ARQ][MARGEM][FERROVIA][CHAVE])  

        #endregion


    def __CALCULAR__(self):
        
        def __SALDO__(TIPO, MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, i):

            if TIPO == "TERMINAL": 

                if i == 0:

                    RECEBIDOS      = self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_DE_VAZIOS"][0]
                    SALDO_ANTERIOR = int(self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_VIRADA"]) 
                    ALIVIO         = 0
                        
                    SALDO = (RECEBIDOS + SALDO_ANTERIOR - ALIVIO)
                    self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][0] = SALDO
                    
                    i = (i + 1)

                for i in range(i, 120):
                            
                    RECEBIDOS      = self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["GERACAO_DE_VAZIOS"][i]
                    SALDO_ANTERIOR = self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][i-1]
                    ALIVIO         = self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO_DE_VAZIOS"][i-1]
                    
                    SALDO = (RECEBIDOS + SALDO_ANTERIOR - ALIVIO)

                    self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][i] = SALDO

            if TIPO == "L4K":
                
                if i == 0:

                    RECEBIDOS      = self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][0]
                    SALDO_ANTERIOR = int(self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_VIRADA"])
                    ALIVIO         = 0
                        
                    SALDO = (RECEBIDOS + SALDO_ANTERIOR - ALIVIO)
                    self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_DE_VAZIOS"][0] = SALDO
                    
                    self.full_L4K["OCUPACAO"]["FERROVIA"][0] = ""
                    self.full_L4K["OCUPACAO"]["SEGMENTO"][0] = ""
                    
                    for umaFERROVIA in self.INFOS_LINHAS["LINHA_4K"]["FERROVIAS"]:
                        for umSEFMENTO in self.INFOS_LINHAS["LINHA_4K"]["SEGMENTOS"]:
                    
                                if self.full_L4K["SUBIDA"][umaFERROVIA][umSEFMENTO]["SALDO_DE_VAZIOS"][0] > 0:
                                    self.full_L4K["OCUPACAO"]["FERROVIA"][0] = umaFERROVIA
                                    self.full_L4K["OCUPACAO"]["SEGMENTO"][0] = umSEFMENTO

                    i = (i + 1)

                for i in range(i, 120):
                            
                    RECEBIDOS      = self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][i]
                    SALDO_ANTERIOR = self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_DE_VAZIOS"][i-1]
                    ALIVIO         = self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["ALIVIO_DE_VAZIOS"][i-1]
                    
                    SALDO = (RECEBIDOS + SALDO_ANTERIOR - ALIVIO)
                    self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_DE_VAZIOS"][i] = SALDO

        def __L4K__():

            #region FIFO

            def __FIFO_L4K__(LINHA: dict, TABELA_DE_ALIVIOS):

                TABELA_DE_ALIVIOS["ALIVIAR_4K"] = False
                TABELA_DE_ALIVIOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["VAGOES"] > 0]
                
                if len(TABELA_DE_ALIVIOS) == 0          : return [False, None]
                if LINHA["VAGOES"] >= LINHA["UM_TREM"]  : return [False, None] #VAGOES SUFICIENTES NA LINHA
               
                #region LINHA VAZIA

                if LINHA["OCUPACAO_FERROVIA"] == "":

                    TABELA_DE_ALIVIOS  = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["TX_MIN"] >= 1]
                    if len(TABELA_DE_ALIVIOS) == 0 : return [False, None]
                    
                    id      = TABELA_DE_ALIVIOS['TX_MAX'].idxmax()
                    ALIVIO  = TABELA_DE_ALIVIOS.loc[id]
                    

                    LOTE_NECESSARIO = (LINHA["UM_TREM"] - LINHA["VAGOES"])

                    if (ALIVIO["VAGOES"] > LOTE_NECESSARIO):
                        
                        ALIVIO["VAGOES"] = LOTE_NECESSARIO
                        ALIVIO["ALIVIAR_4K"] = True

                    return [True, ALIVIO]

                
                #endregion

                #region LINHA OCUPADA
                else:
                    
                    FILTRO_FERROVIA = LINHA["OCUPACAO_FERROVIA"]
                    FILTRO_SEGMENTO = LINHA["OCUPACAO_SEGMENTO"]
                    
                    TABELA_DE_ALIVIOS = TABELA_DE_ALIVIOS[(TABELA_DE_ALIVIOS["SEGMENTO"] == FILTRO_SEGMENTO) & (TABELA_DE_ALIVIOS["FERROVIA"] == FILTRO_FERROVIA)]
                
                    if len(TABELA_DE_ALIVIOS) == 0 : return [False, None]

                    LOTE_NECESSARIO = (LINHA["UM_TREM"] - LINHA["VAGOES"])

                    TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"] = abs(LOTE_NECESSARIO - TABELA_DE_ALIVIOS["VAGOES"])

                    #region CASO HOUVER BLOCO MINIMO COMPATIVEL ALIVIE-O
                    TABELA_DE_ALIVIOS_MIN_OK = TABELA_DE_ALIVIOS[TABELA_DE_ALIVIOS["TX_MIN"] >= 1]
                    
                    if len(TABELA_DE_ALIVIOS_MIN_OK) > 0:
                        
                        try:
                            id      = TABELA_DE_ALIVIOS_MIN_OK["TX_MIN"].idmax()
                            ALIVIO  = TABELA_DE_ALIVIOS_MIN_OK.loc[id]
                            
                        except AttributeError: #CASO NAO SEJA UM DATAFRAME, MAS UM PDSERIES
                            
                            ALIVIO  = TABELA_DE_ALIVIOS_MIN_OK.iloc[0]
                        
                        
                        if (ALIVIO["VAGOES"] > LOTE_NECESSARIO):
                            
                            ALIVIO["ALIVIAR_4K"] = True
                            ALIVIO["VAGOES"]     = LOTE_NECESSARIO
                        
                        return [True, ALIVIO]

                    #endregion




                    id      = TABELA_DE_ALIVIOS["DIFERENCA_VAGOES"].idxmin()
                    ALIVIO  = TABELA_DE_ALIVIOS.loc[id]
                    
                    
                    if not ((FILTRO_FERROVIA == "RUMO") and (FILTRO_FERROVIA == "GRAO")):

                        if (ALIVIO["VAGOES"] < ALIVIO["MIN"]) and (not ALIVIO["SALDO"] == 0): # SO PODE ALIVIAR QUANDO ACABAR O TREM

                            return [False, None]
                        
                        elif ALIVIO["SALDO"] == 0:

                            ALIVIO["ALIVIAR_4K"] = True

                    if (ALIVIO["VAGOES"] > LOTE_NECESSARIO):
                        
                        ALIVIO["VAGOES"]     = LOTE_NECESSARIO
                        ALIVIO["ALIVIAR_4K"] = True


                    if (ALIVIO["VAGOES"] < ALIVIO["MIN"]) and (not ALIVIO["SALDO"] == 0): # SO PODE ALIVIAR QUANDO ACABAR O TREM

                            return [False, None]
                    
                    return [True, ALIVIO]
                
                #endregion
   
            #endregion
        
            SEGMENTOS = self.INFOS_LINHAS["LINHA_4K"]["SEGMENTOS"]
            FERROVIAS = self.INFOS_LINHAS["LINHA_4K"]["FERROVIAS"]
            
            for FERROVIA in ["RUMO", "MRS", "VLI"]: __SALDO__("L4K", "DIREITA", "PCX", None, "GRAO", FERROVIA, 0)
          
            for i in range(1, 119):

                ALIVIO_SELECIONADO = None         
                EXISTE_ALIVIO      = False  

                #region ANALISAR LINHA
                LINHA = {
                            "VAGOES"      : 0, 
                            "LOTE_PRONTO" : 0, 
                            "UM_TREM"     : self.INFOS_LINHAS["LINHA_4K"]["LOTE"],
                            "OCUPACAO_FERROVIA"      : self.full_L4K["OCUPACAO"]["FERROVIA"][i],
                            "OCUPACAO_SEGMENTO"      : self.full_L4K["OCUPACAO"]["SEGMENTO"][i],
                            "OCUPACAO_LOTE_COMPLETO" : self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i]
                        }
                
                

                if not self.full_L4K["OCUPACAO"]["FERROVIA"][i] == "":

                    LINHA["VAGOES"] = self.full_L4K["SUBIDA"][LINHA["OCUPACAO_FERROVIA"]][LINHA["OCUPACAO_SEGMENTO"]]["SALDO_DE_VAZIOS"][i]

                #endregion
                
                TABELA_DE_ALIVIOS = pd.DataFrame(columns=["HR", "TERMINAL", "SEGMENTO", "FERROVIA", "VAGOES", "SALDO", "EXISTE_SLD", "MIN", "MAX", "TX_MIN", "TX_MAX"])

                if LINHA["OCUPACAO_LOTE_COMPLETO"] == False:

                    
                    for TERMINAL in list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PCX"]):
            
                        for SEGMENTO in SEGMENTOS:

                            for FERROVIA in FERROVIAS: 
                                
                                VAGOES    = self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][i]
                                SALDO_DSC = self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["SALDO_NAVEGACAO"][i]
                                MIN       = self.jsSUBIDAS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MIN"]
                                MAX       = self.jsSUBIDAS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MAX"]
                                
                                EXISTE_SALDO = False
                                if SALDO_DSC > 0:   EXISTE_SALDO = True

                                DADOS = {

                                            "HR"         : i,
                                            "TERMINAL"   : TERMINAL,
                                            "FERROVIA"   : FERROVIA,
                                            "SEGMENTO"   : SEGMENTO,
                                            "VAGOES"     : VAGOES,
                                            "EXISTE_SLD" : EXISTE_SALDO,
                                            "SALDO"      : SALDO_DSC,
                                            "TEMPO"      : i,
                                            "MIN"        : MIN,
                                            "MAX"        : MAX,
                                            "TX_MIN"     : round((VAGOES / MIN), 2), 
                                            "TX_MAX"     : round((VAGOES / MAX), 2)
                                        }

                                TABELA_DE_ALIVIOS.loc[len(TABELA_DE_ALIVIOS)] = DADOS
                
                
                FIFO = __FIFO_L4K__(LINHA, TABELA_DE_ALIVIOS)
                EXISTE_ALIVIO      = FIFO[0]

                if EXISTE_ALIVIO:
                    
                    ALIVIO_SELECIONADO = dict(FIFO[1]) 
                    TERMINAL    = ALIVIO_SELECIONADO["TERMINAL"]
                    FERROVIA    = ALIVIO_SELECIONADO["FERROVIA"]
                    SEGMENTO    = ALIVIO_SELECIONADO["SEGMENTO"]
                    VAGOES      = int(ALIVIO_SELECIONADO["VAGOES"])
                    ALIVIAR_4K  = ALIVIO_SELECIONADO["ALIVIAR_4K"]

                    self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PCX"][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO_DE_VAZIOS"][i] = VAGOES
                    self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][i] = VAGOES


                    self.full_L4K["OCUPACAO"]["FERROVIA"][i] = FERROVIA
                    self.full_L4K["OCUPACAO"]["SEGMENTO"][i] = SEGMENTO

                    self.full_L4K["OCUPACAO"]["FERROVIA"][i+1] = FERROVIA
                    self.full_L4K["OCUPACAO"]["SEGMENTO"][i+1] = SEGMENTO

                    __SALDO__("TERMINAL", "DIREITA", "PCX", TERMINAL,   SEGMENTO, FERROVIA, i)
                    __SALDO__("L4K",      "DIREITA", "PCX", None,       SEGMENTO, FERROVIA, i)

                    if self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_DE_VAZIOS"][i] >= self.INFOS_LINHAS["LINHA_4K"]["LOTE"]:
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i] = True
                    
                    if ALIVIAR_4K:
                        
                        self.full_L4K["OCUPACAO"]["FERROVIA"][i] = ""
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i] = ""
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i] = False

                        self.full_L4K["OCUPACAO"]["FERROVIA"][i+1] = ""
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i+1] = ""
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i+1] = False

                        VAGOES_4K = self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_DE_VAZIOS"][i]
                        self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["ALIVIO_DE_VAZIOS"][i] = VAGOES_4K
                        __SALDO__("L4K",      "DIREITA", "PCX", None,       SEGMENTO, FERROVIA, i)

                else: #mantém status

                    FERROVIA = self.full_L4K["OCUPACAO"]["FERROVIA"][i-1]
                    SEGMENTO = self.full_L4K["OCUPACAO"]["SEGMENTO"][i-1]
                    LOTE     = self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i-1]

                    if (not FERROVIA == "") and (not SEGMENTO == ""): 

                        self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][i] = 0

                        self.full_L4K["OCUPACAO"]["FERROVIA"][i]        = FERROVIA
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i]        = SEGMENTO
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i]   = LOTE

                        self.full_L4K["OCUPACAO"]["FERROVIA"][i+1]      = FERROVIA
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i+1]      = SEGMENTO
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i+1] = LOTE

                    else:

                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i-1]   = False

                        self.full_L4K["OCUPACAO"]["FERROVIA"][i]        = ""
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i]        = ""
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i]   = False

                        self.full_L4K["OCUPACAO"]["FERROVIA"][i+1]      = ""
                        self.full_L4K["OCUPACAO"]["SEGMENTO"][i+1]      = ""
                        self.full_L4K["OCUPACAO"]["LOTE_COMPLETO"][i+1] = False

        def __PSN_PMC__():

            MARGEM      = ["DIREITA"] 

            TERMINAIS   = list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PMC"].keys()) + list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PST"].keys())
            
            for TERMINAL in TERMINAIS:

                try:    
            
                    SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                    FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                    PATIO     = self.INFOS[TERMINAL]["PATIO"]
                    MARGEM    = self.INFOS[TERMINAL]["MARGEM"]

                except KeyError:
                    
                    SEGMENTO  = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SEGMENTO"]
                    FERROVIAS = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["FERROVIA"]
                    PATIO     = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]
                    MARGEM    = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["MARGEM"]

                for FERROVIA in FERROVIAS:

                    __SALDO__("TERMINAL", MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, 0)


            for i in range(1, 119):

                for TERMINAL in TERMINAIS:

                    SEGMENTO = self.INFOS[TERMINAL]["SEGMENTO"]
                    PATIO    = self.INFOS[TERMINAL]["PATIO"]

                    for FERROVIA in self.INFOS[TERMINAL]["FERROVIA"]:

                        VAGOES      = self.full_TERMINAIS_DO_CALCULO["DIREITA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][i]
                        MIN         = self.jsSUBIDAS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MIN"]
                        SALDO_DSC   = self.full_TERMINAIS_DO_CALCULO["DIREITA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_NAVEGACAO"][i]
                        
                        if (VAGOES > MIN) or (SALDO_DSC == 0): #NAO TEM FIFO, O ALIVIO É SO ISSO MESMO

                            self.full_TERMINAIS_DO_CALCULO["DIREITA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO_DE_VAZIOS"][i] = VAGOES
                            __SALDO__("TERMINAL", MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, i)
                            
        def __PCX__():

            MARGEM      = ["DIREITA"] 
           #PATIOS      = ["PMC", "PSN"]
            TERMINAIS   = list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PCX"].keys())
            
            for TERMINAL in TERMINAIS:

                try:    
            
                    SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                    FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                    PATIO     = self.INFOS[TERMINAL]["PATIO"]
                    MARGEM    = self.INFOS[TERMINAL]["MARGEM"]

                except KeyError:
                    
                    SEGMENTO  = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SEGMENTO"]
                    FERROVIAS = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["FERROVIA"]
                    PATIO     = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]
                    MARGEM    = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["MARGEM"]

                for FERROVIA in FERROVIAS:
                                       
                    __SALDO__("TERMINAL", MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, 0)

        def __PCZ__():

            TERMINAIS   = list(self.full_TERMINAIS_DO_CALCULO["ESQUERDA"]["PCZ"].keys())

            for TERMINAL in TERMINAIS:

                SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                PATIO     = self.INFOS[TERMINAL]["PATIO"]
                MARGEM    = self.INFOS[TERMINAL]["MARGEM"]

                for FERROVIA in FERROVIAS:
                    __SALDO__("TERMINAL", MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, 0)

            for i in range(1, 119):

                for TERMINAL in TERMINAIS:

                    SEGMENTO = self.INFOS[TERMINAL]["SEGMENTO"]
                    PATIO    = self.INFOS[TERMINAL]["PATIO"]

                    for FERROVIA in self.INFOS[TERMINAL]["FERROVIA"]:

                        VAGOES      = self.full_TERMINAIS_DO_CALCULO["ESQUERDA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_DE_VAZIOS"][i]
                        MIN         = self.jsSUBIDAS[TERMINAL]["SATURACAO_VAZIO"][FERROVIA]["MIN"]
                        SALDO_DSC   = self.full_TERMINAIS_DO_CALCULO["ESQUERDA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["SALDO_NAVEGACAO"][i]
                        
                        if (VAGOES > MIN) or (SALDO_DSC == 0): #NAO TEM FIFO, O ALIVIO É SO ISSO MESMO

                            self.full_TERMINAIS_DO_CALCULO["ESQUERDA"][PATIO][TERMINAL][SEGMENTO][FERROVIA]["ALIVIO_DE_VAZIOS"][i] = VAGOES
                            __SALDO__("TERMINAL", MARGEM, PATIO, TERMINAL, SEGMENTO, FERROVIA, i)
                            
                            #self.full_CONDENSADOS["ESQUERDA"][FERROVIA][SEGMENTO][i] += VAGOES
            
        __PCZ__()
        
        __PCX__()

        __PSN_PMC__()
        
        __L4K__()
    
    def __DESMONTAR_FULL__(self):

        #region TERMINAIS_SUBIDA (full)

        LISTAS = {}

        for TERMINAL in self.TERMINAIS_DO_CALCULO:

            try:    
            
                SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                PATIO     = self.INFOS[TERMINAL]["PATIO"]
                MARGEM    = self.INFOS[TERMINAL]["MARGEM"]

            except KeyError:
                
                SEGMENTO  = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SEGMENTO"]
                FERROVIAS = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["FERROVIA"]
                PATIO     = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]
                MARGEM    = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["MARGEM"]

            LISTAS[TERMINAL]            = {}
            LISTAS[TERMINAL][SEGMENTO]  = {}
            

            for FERROVIA in FERROVIAS:

                LISTAS[TERMINAL][SEGMENTO][FERROVIA] = {}

                for CHAVE in CHAVES_SUBIDA:

                    LISTAS[TERMINAL][SEGMENTO][FERROVIA][CHAVE] = [self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][CHAVE][i:i + 24] for i in range(0, len(self.full_TERMINAIS_DO_CALCULO[MARGEM][PATIO][TERMINAL][SEGMENTO][FERROVIA][CHAVE]), 24)]

                    for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                            self.jsSUBIDAS[TERMINAL][DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO][CHAVE] = LISTAS[TERMINAL][SEGMENTO][FERROVIA][CHAVE][index]
            
            
            for DATA_ARQ in  self.LISTA_DATA_ARQ:

                with open(os.path.join(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{TERMINAL}/subida_{DATA_ARQ}.json"), 'w') as ARQUIVO:
                    json.dump(self.jsSUBIDAS[TERMINAL][DATA_ARQ], ARQUIVO, indent=4)   

        #endregion

        #region L4K
        
        LISTAS = {"SUBIDA": {}, "OCUPACAO": {}}
        SEGMENTOS = self.INFOS_LINHAS["LINHA_4K"]["SEGMENTOS"]
        FERROVIAS = self.INFOS_LINHAS["LINHA_4K"]["FERROVIAS"]
        
        for FERROVIA in FERROVIAS:

            LISTAS["SUBIDA"][FERROVIA] = {}
            
            for SEGMENTO in SEGMENTOS:

                LISTAS["SUBIDA"][FERROVIA][SEGMENTO] = {}

                for CHAVE in CHAVES_L4K:

                    LISTAS["SUBIDA"][FERROVIA][SEGMENTO][CHAVE] = [self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO][CHAVE][i:i + 24] for i in range(0, len(self.full_L4K["SUBIDA"][FERROVIA][SEGMENTO][CHAVE]), 24)]

                    for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                        self.jsL4K[DATA_ARQ]["SUBIDA"][FERROVIA][SEGMENTO][CHAVE] = LISTAS["SUBIDA"][FERROVIA][SEGMENTO][CHAVE][index]


        for ITEM in CHAVES_OCUPACAO_L4K:

            LISTAS["OCUPACAO"][ITEM] = [self.full_L4K["OCUPACAO"][ITEM][i:i + 24] for i in range(0, len(self.full_L4K["OCUPACAO"][ITEM]), 24)]

            for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                self.jsL4K[DATA_ARQ]["OCUPACAO"][ITEM] = LISTAS["OCUPACAO"][ITEM][index]


        for DATA_ARQ in  self.LISTA_DATA_ARQ:

            with open(os.path.join(f"previsao_trens/src/SUBIDA/LINHAS/LINHA_4K/linha_4k_{ DATA_ARQ }.json"), 'w') as ARQUIVO:
                json.dump(self.jsL4K[DATA_ARQ], ARQUIVO, indent=4)  

        #endregion

        #region CONDENSADOS

        LISTAS = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}},  "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}}}

        for MARGEM in (LISTAS.keys()):

            for FERROVIA in (LISTAS[MARGEM].keys()):

                for ITEM in CHAVES_CONDENSADOS:
                    
                    # A CHAVE SAIDAS NAO POSSUI SALDO                   
                    if not FERROVIA == "SAIDAS": LISTAS[MARGEM][FERROVIA][ITEM] = [self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]["SALDO"][i:i + 24] for i in range(0, len(self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]["SALDO"]), 24)]
                    else:                        LISTAS[MARGEM][FERROVIA][ITEM] = [self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM][i:i + 24]          for i in range(0, len(self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]), 24)]
                    
                    for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):
                        
                        # A CHAVE SAIDAS NAO POSSUI SALDO
                        if not FERROVIA == "SAIDAS": self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][ITEM]["SALDO"] = LISTAS[MARGEM][FERROVIA][ITEM][index]
                        else:                        self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][ITEM]          = LISTAS[MARGEM][FERROVIA][ITEM][index]

        for DATA_ARQ in  self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json", 'w') as ARQUIVO:
                json.dump(self.jsCONDENSADOS[DATA_ARQ], ARQUIVO, indent=4) 

        #endregion

        #region BUFFERS 

        LISTAS = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}},  "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}}}

        for MARGEM in (LISTAS.keys()):

            for FERROVIA in (LISTAS[MARGEM].keys()):

                for ITEM in CHAVES_BUFFERS:

                    LISTAS[MARGEM][FERROVIA][ITEM] = [self.full_BUFFERS[MARGEM][FERROVIA][ITEM][i:i + 24] for i in range(0, len(self.full_BUFFERS[MARGEM][FERROVIA][ITEM]), 24)]

                    for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                        self.jsBUFFERS[DATA_ARQ][MARGEM][FERROVIA][ITEM] = LISTAS[MARGEM][FERROVIA][ITEM][index]


        #endregion

    def __CALCULAR_CONDENSADOS__(self):

        #DIREITA

        TERMINAIS_PMC   = list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PMC"].keys())
        TERMINAIS_PST   = list(self.full_TERMINAIS_DO_CALCULO["DIREITA"]["PST"].keys())
   
        TERMINAIS       = (TERMINAIS_PMC + TERMINAIS_PST)
        
        #FAZENDO PARA I = 0 


        for i in range(119):
            
            for FERROVIA in ["RUMO", "MRS", "VLI"]:
                    
                for CHAVE in CHAVES_CONDENSADOS:
                    ALIVIOS = 0
                    
                    for TERMINAL in TERMINAIS:
                                
                        try:                PATIO = self.INFOS[TERMINAL]["PATIO"]
                        except KeyError:    PATIO = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]

                        if CHAVE in self.full_TERMINAIS_DO_CALCULO["DIREITA"][PATIO][TERMINAL]:
                            ALIVIOS += self.full_TERMINAIS_DO_CALCULO["DIREITA"][PATIO][TERMINAL][CHAVE][FERROVIA]["ALIVIO_DE_VAZIOS"][i]

                    if CHAVE in  self.full_L4K["SUBIDA"][FERROVIA]:
                         ALIVIOS += self.full_L4K["SUBIDA"][FERROVIA][CHAVE]["ALIVIO_DE_VAZIOS"][i]

                    SAIDAS = 0
                    if self.full_CONDENSADOS["DIREITA"]["SAIDAS"]["FERROVIA"][i] == FERROVIA: SAIDAS =  self.full_CONDENSADOS["DIREITA"]["SAIDAS"][CHAVE][i]
                    
                    BUFFER = 0
                    if CHAVE =="GRAO": BUFFER = self.full_BUFFERS["DIREITA"][FERROVIA]["SALDO"][i]
                    
                    if i == 0:
                        self.full_CONDENSADOS["DIREITA"][FERROVIA][CHAVE]["SALDO"][0] = self.full_CONDENSADOS["DIREITA"][FERROVIA][CHAVE]["SALDO_VIRADA"] + ALIVIOS - SAIDAS - BUFFER
                    else:
                        self.full_CONDENSADOS["DIREITA"][FERROVIA][CHAVE]["SALDO"][i] = self.full_CONDENSADOS["DIREITA"][FERROVIA][CHAVE]["SALDO"][i-1] + ALIVIOS - SAIDAS - BUFFER

        #ESQUERDA

        TERMINAIS_PCZ   = list(self.full_TERMINAIS_DO_CALCULO["ESQUERDA"]["PCZ"].keys())
        TERMINAIS       = TERMINAIS_PCZ

        for i in range(119):
            
            for FERROVIA in ["RUMO", "MRS", "VLI"]:

                for CHAVE in CHAVES_CONDENSADOS:
                    ALIVIOS = 0

                    for TERMINAL in TERMINAIS:

                        try:                PATIO = self.INFOS[TERMINAL]["PATIO"]
                        except KeyError:    PATIO = self.TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]

                        if CHAVE in self.full_TERMINAIS_DO_CALCULO["ESQUERDA"][PATIO][TERMINAL]:
                            ALIVIOS += self.full_TERMINAIS_DO_CALCULO["ESQUERDA"][PATIO][TERMINAL][CHAVE][FERROVIA]["ALIVIO_DE_VAZIOS"][i]


                    SAIDAS = 0
                    if self.full_CONDENSADOS["ESQUERDA"]["SAIDAS"]["FERROVIA"][i] == FERROVIA: SAIDAS =  self.full_CONDENSADOS["ESQUERDA"]["SAIDAS"][CHAVE][i]

                    BUFFER = 0
                    if CHAVE =="GRAO": BUFFER = self.full_BUFFERS["ESQUERDA"][FERROVIA]["SALDO"][i]
                      
                    if i == 0:
                        self.full_CONDENSADOS["ESQUERDA"][FERROVIA][CHAVE]["SALDO"][0] = self.full_CONDENSADOS["ESQUERDA"][FERROVIA][CHAVE]["SALDO_VIRADA"] + ALIVIOS - SAIDAS - BUFFER
                    else:
                        self.full_CONDENSADOS["ESQUERDA"][FERROVIA][CHAVE]["SALDO"][i] = self.full_CONDENSADOS["ESQUERDA"][FERROVIA][CHAVE]["SALDO"][i-1] + ALIVIOS - SAIDAS - BUFFER

    def CALCULAR(self):

        self.__MONTAR_FULL__()
        self.__CALCULAR__()
        self.__CALCULAR_CONDENSADOS__()
        self.__DESMONTAR_FULL__()



class SUBIDA_DE_VAZIOS: #BAIXA A PRODUTIVIDADE

    def __init__(self):

        self.TERMINAIS_SUBIDA = os.listdir(os.path.join(DIRETORIO_SUBIDA, "TERMINAIS_SUBIDA")) 

        self.PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        self.PERIODO_VIGENTE = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0])
        self.LISTA_DATA_ARQ  = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()

        with open(f"previsao_trens/src/SUBIDA/PARAMETROS/TERMINAIS_ESPECIAIS.json") as ARQUIVO:
            self.TERMINAIS_ESPECIAIS = json.load(ARQUIVO)
        
        with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO:
            self.INFOS = json.load(ARQUIVO)
        
    def __OUTORGAR_PRODUTIVIDADE__(self):
        
        TERMINAIS_SALDO = [item for item in self.TERMINAIS_SUBIDA if item not in self.TERMINAIS_ESPECIAIS["DESCONSIDERAR"]["OUTORGA_SALDO"]]
        
        #region OUTORGA DA PRODUTIVIDADE COMUM
        for TERMINAL in TERMINAIS_SALDO:
            
            SALDO_VIRADA = {}

            for i, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                SALDO_VIRADA[i] = {}

                PRODUTOS  = self.INFOS[TERMINAL]["PRODUTOS"]
                SEGMENTO  = self.INFOS[TERMINAL]["SEGMENTO"]
                FERROVIAS = self.INFOS[TERMINAL]["FERROVIA"]
                
                with open(f"previsao_trens/src/DESCARGAS/{TERMINAL}/descarga_{DATA_ARQ}.json") as ARQUIVO:
                    jsDESCARGA = json.load(ARQUIVO)

                with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{TERMINAL}/subida_{DATA_ARQ}.json") as ARQUIVO:
                    jsSUBIDA   = json.load(ARQUIVO)

                PEDRAS = {}
                SALDOS = {}

                for FERROVIA in FERROVIAS:

                    if not FERROVIA in SALDO_VIRADA[i]: SALDO_VIRADA[i][FERROVIA] = {}
                    
                    SALDOS[FERROVIA] = {}
                    SALDOS[FERROVIA]["SALDO_NAVEGACAO"] = [0] * 24

                    PEDRAS[FERROVIA] = {}
                    PEDRAS[FERROVIA]["GERACAO_VAZIOS"]  = [0] * 24

                    for PRODUTO in PRODUTOS:

                        if not PRODUTO in SALDO_VIRADA[i][FERROVIA]: SALDO_VIRADA[i][FERROVIA][PRODUTO] = {}

                        SALDOS[FERROVIA][PRODUTO] = jsDESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["SALDO"]
                        SALDOS[FERROVIA]["SALDO_NAVEGACAO"] = [sum(x) for x in zip(SALDOS[FERROVIA][PRODUTO], SALDOS[FERROVIA]["SALDO_NAVEGACAO"])]

                        PEDRAS[FERROVIA][PRODUTO] = jsDESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"]
                        PEDRAS[FERROVIA]["GERACAO_VAZIOS"]  = [sum(x) for x in zip(PEDRAS[FERROVIA][PRODUTO], PEDRAS[FERROVIA]["GERACAO_VAZIOS"])]

                    jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_NAVEGACAO"]   = SALDOS[FERROVIA]["SALDO_NAVEGACAO"]
                    jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = PEDRAS[FERROVIA]["GERACAO_VAZIOS"]
                    
                    if not i == 0: HR_01 = [SALDO_VIRADA[i-1][FERROVIA][PRODUTO]]
                    else:          HR_01 = [0]
 
                    SALDO_VIRADA[i][FERROVIA][PRODUTO] = jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][23]

                    jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = HR_01 + jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][:-1]
                    jsSUBIDA["SUBIDA"][FERROVIA][SEGMENTO]["ALIVIO_DE_VAZIOS"]  = [0] * 24

                with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{ TERMINAL }/subida_{ DATA_ARQ }.json", 'w') as ARQUIVO:
                    json.dump(jsSUBIDA, ARQUIVO, indent=4)

                
        #endregion

        #region OUTORGA PRODUTIVIDADE ADM
        MOEGAS_ADM = ["MOEGA X", "MOEGA V"]
        
        PRODUTOS  = self.INFOS["MOEGA X"]["PRODUTOS"]
        SEGMENTO  = self.INFOS["MOEGA X"]["SEGMENTO"]
        FERROVIAS = self.INFOS["MOEGA X"]["FERROVIA"]
        
        for MOEGA in MOEGAS_ADM:
            
            
            SALDO_VIRADA = {}
            
            for i, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):
                
                with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/ADM/subida_{ DATA_ARQ }.json") as ARQUIVO:
                    jsSUBIDA_ADM   = json.load(ARQUIVO)
                
                if MOEGA == "MOEGA X": #LIMPANDO DA PRIMEIRA VEZ QUE ABRIR

                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_NAVEGACAO"]   = [0] * 24
                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = [0] * 24
    

                SALDO_VIRADA[i] = {}


                with open(f"previsao_trens/src/DESCARGAS/{ MOEGA }/descarga_{ DATA_ARQ }.json") as ARQUIVO:
                    jsDESCARGA = json.load(ARQUIVO)

                PEDRAS = {}
                SALDOS = {}

                for FERROVIA in ["RUMO", "MRS", "VLI"]:

                    if not FERROVIA in SALDO_VIRADA[i]: SALDO_VIRADA[i][FERROVIA] = {}

                    SALDOS[FERROVIA] = {}
                    SALDOS[FERROVIA]["SALDO_NAVEGACAO"] = [0] * 24

                    PEDRAS[FERROVIA] = {}
                    PEDRAS[FERROVIA]["GERACAO_VAZIOS"]  = [0] * 24

                    for PRODUTO in PRODUTOS:

                        if not PRODUTO in SALDO_VIRADA[i][FERROVIA]: SALDO_VIRADA[i][FERROVIA][PRODUTO] = {}

                        SALDOS[FERROVIA][PRODUTO] = jsDESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["SALDO"]
                        SALDOS[FERROVIA]["SALDO_NAVEGACAO"] = [sum(x) for x in zip(SALDOS[FERROVIA][PRODUTO], SALDOS[FERROVIA]["SALDO_NAVEGACAO"])]

                        PEDRAS[FERROVIA][PRODUTO] = jsDESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"]
                        PEDRAS[FERROVIA]["GERACAO_VAZIOS"]  = [sum(x) for x in zip(PEDRAS[FERROVIA][PRODUTO], PEDRAS[FERROVIA]["GERACAO_VAZIOS"])]

                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_NAVEGACAO"]   = [sum(x) for x in zip(jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["SALDO_NAVEGACAO"],   SALDOS[FERROVIA]["SALDO_NAVEGACAO"])]
                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = [sum(x) for x in zip(jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"], PEDRAS[FERROVIA]["GERACAO_VAZIOS"])]

                    if not i == 0: HR_01 = [SALDO_VIRADA[i-1][FERROVIA][PRODUTO]]
                    else:          HR_01 = [0]

                    SALDO_VIRADA[i][FERROVIA][PRODUTO] = jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][23]

                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"] = HR_01 + jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["GERACAO_DE_VAZIOS"][:-1]
                    jsSUBIDA_ADM["SUBIDA"][FERROVIA][SEGMENTO]["ALIVIO_DE_VAZIOS"]  = [0] * 24
      
                with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/ADM/subida_{ DATA_ARQ }.json", 'w') as ARQUIVO:
                    json.dump(jsSUBIDA_ADM, ARQUIVO, indent=4)

        #endregion

    def ATUALIZAR(self): #BOTAO ATUALIZAR SUBIDA

        self.__OUTORGAR_PRODUTIVIDADE__()

        CALCULOS_SUBIDA = CALCULAR_SALDO()
        CALCULOS_SUBIDA.CALCULAR()
       
def EDITAR_SALDO_VIRADA_TERMINAL(PARAMETROS): #AQUI PARA PODER AGILIZAR A ENTREGA, TAMBÉM ENVIA SALDO DE VIRADA DA LINHA 4K TERMINAL = L4K    

    if PARAMETROS["NOVO_VALOR"] == "": PARAMETROS["NOVO_VALOR"] = 0

    if not PARAMETROS["TERMINAL"] == "L4K":

        PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        PERIODO_VIGENTE = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
        DATA_ARQ        = PERIODO_VIGENTE["DATA_ARQ"].tolist()[0]
    
        with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{PARAMETROS["TERMINAL"]}/subida_{DATA_ARQ}.json") as ARQUIVO:
            jsSUBIDA   = json.load(ARQUIVO)

        jsSUBIDA["SUBIDA"][PARAMETROS["FERROVIA"]][PARAMETROS["SEGMENTO"]]["SALDO_VIRADA"] = PARAMETROS["NOVO_VALOR"]

        with open(f"previsao_trens/src/SUBIDA/TERMINAIS_SUBIDA/{PARAMETROS["TERMINAL"]}/subida_{DATA_ARQ}.json", 'w') as ARQUIVO:
            json.dump(jsSUBIDA, ARQUIVO, indent=4)  

    else:

        PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        PERIODO_VIGENTE = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
        DATA_ARQ        = PERIODO_VIGENTE["DATA_ARQ"].tolist()[0]
    
        with open(f"previsao_trens/src/SUBIDA/LINHAS/LINHA_4K/linha_4K_{ DATA_ARQ }.json") as ARQUIVO:
            jsL4K = json.load(ARQUIVO)

        jsL4K["SUBIDA"][PARAMETROS["FERROVIA"]][PARAMETROS["SEGMENTO"]]["SALDO_VIRADA"] = PARAMETROS["NOVO_VALOR"]

        with open(f"previsao_trens/src/SUBIDA/LINHAS/LINHA_4K/linha_4K_{ DATA_ARQ }.json", 'w') as ARQUIVO:
            json.dump(jsL4K, ARQUIVO, indent=4) 

def EDITAR_BUFFER(PARAMETROS):

    PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
    
    if PARAMETROS["NOVO_VALOR"] == "": PARAMETROS["NOVO_VALOR"] = 0
    
    if not PARAMETROS["HORA"] == "SALDO_VIRADA":

        LINHA       = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == PARAMETROS["DIA_LOGISTICO"]]
        DATA_ARQ    = LINHA['DATA_ARQ'].values[0]
        INDEX       = LINHA.index[0]

        HORA        = (int(PARAMETROS["HORA"]) - 1) 
        FERROVIA    = PARAMETROS["FERROVIA"]
        MARGEM      = PARAMETROS["MARGEM"]
        VALOR       = PARAMETROS["NOVO_VALOR"]

        with open(f"previsao_trens/src/SUBIDA/BUFFER/buffer_{ DATA_ARQ }.json") as ARQUIVO:
            jsBUFFER = json.load(ARQUIVO)

        jsBUFFER[MARGEM][FERROVIA]["SALDO"][HORA] = int(VALOR)

        with open(f"previsao_trens/src/SUBIDA/BUFFER/buffer_{ DATA_ARQ }.json", 'w') as ARQUIVO:
            json.dump(jsBUFFER, ARQUIVO, indent=4) 

def EDITAR_SALDO_CONDENSADO(PARAMETROS):

    PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
    LINHA       = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == "D"]
    DATA_ARQ    = LINHA['DATA_ARQ'].values[0]

    if PARAMETROS["NOVO_VALOR"] == "": PARAMETROS["NOVO_VALOR"] = 0

    with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json") as ARQUIVO:
            jsBUFFER = json.load(ARQUIVO)

    jsBUFFER[PARAMETROS["MARGEM"]][PARAMETROS["FERROVIA"]][PARAMETROS["SEGMENTO"]]["SALDO_VIRADA"] = int(PARAMETROS["NOVO_VALOR"])

    with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json", 'w') as ARQUIVO:
        json.dump(jsBUFFER, ARQUIVO, indent=4) 


class Condensados():

    def __init__(self):

        self.PERIODO_VIGENTE    = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        self.PERIODO_VIGENTE    = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0])
        self.LISTA_DATA_ARQ     = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()
        

        self.full_CONDENSADOS   = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}}, "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}}}
        self.jsCONDENSADOS      = {}
        
    def __abrir__(self):

        #region MONTANDO CONDENSADOS (full)

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json") as ARQUIVO:
                self.jsCONDENSADOS[DATA_ARQ] = json.load(ARQUIVO)

            for MARGEM in list(self.full_CONDENSADOS.keys()):

                for FERROVIA in list(self.full_CONDENSADOS[MARGEM].keys()): # ['RUMO', 'MRS', 'VLI', 'SAIDAS']

                    for CHAVE in CHAVES_CONDENSADOS:

                        #if not CHAVE in self.full_CONDENSADOS[MARGEM][FERROVIA]: self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE] = []

                        #self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][CHAVE])

                        if not FERROVIA == "SAIDAS": 
                            
                            if not CHAVE in self.full_CONDENSADOS[MARGEM][FERROVIA]: self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE] = {"SALDO": []}
                            self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE]["SALDO"].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][CHAVE]["SALDO"])
                        else:                        
                            
                            if not CHAVE in self.full_CONDENSADOS[MARGEM][FERROVIA]: self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE] = []
                            self.full_CONDENSADOS[MARGEM][FERROVIA][CHAVE].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][CHAVE])
                   

                if not "FERROVIA" in self.full_CONDENSADOS[MARGEM]["SAIDAS"]: self.full_CONDENSADOS[MARGEM]["SAIDAS"]["FERROVIA"] = []  
                self.full_CONDENSADOS[MARGEM]["SAIDAS"]["FERROVIA"].extend(self.jsCONDENSADOS[DATA_ARQ][MARGEM]["SAIDAS"]["FERROVIA"])

        #endregion
    
    def __salvar__(self):

        #region CONDENSADOS

        LISTAS = {"DIREITA":  {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}},  "ESQUERDA": {"RUMO": {}, "MRS": {}, "VLI": {}, "SAIDAS": {}}}

        for MARGEM in (LISTAS.keys()):

            for FERROVIA in (LISTAS[MARGEM].keys()):

                for ITEM in CHAVES_CONDENSADOS:

                    if not FERROVIA == "SAIDAS": LISTAS[MARGEM][FERROVIA][ITEM] = [self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]["SALDO"][i:i + 24] for i in range(0, len(self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]["SALDO"]), 24)]
                    else:                        LISTAS[MARGEM][FERROVIA][ITEM] = [self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM][i:i + 24]          for i in range(0, len(self.full_CONDENSADOS[MARGEM][FERROVIA][ITEM]         ), 24)]
                    
                    

                    for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):

                        # A CHAVE SAIDAS NAO POSSUI SALDO
                        if not FERROVIA == "SAIDAS": self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][ITEM]["SALDO"] = LISTAS[MARGEM][FERROVIA][ITEM][index]
                        else:                        self.jsCONDENSADOS[DATA_ARQ][MARGEM][FERROVIA][ITEM]          = LISTAS[MARGEM][FERROVIA][ITEM][index]
                                                    


        for DATA_ARQ in  self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ DATA_ARQ }.json", 'w') as ARQUIVO:
                json.dump(self.jsCONDENSADOS[DATA_ARQ], ARQUIVO, indent=4) 

        #endregion

    def inserirTrem(self, PARAMETROS):


        TIPO_VAGOES = ["QT_GRAOS", "QT_FERTI", "QT_CELUL", "QT_ACUCA", "QT_CONTE"]
        SEGMENTOS   = ["GRAO", "FERTILIZANTE", "CELULOSE", "ACUCAR", "CONTEINER"] 


        LINHA       = self.PERIODO_VIGENTE[self.PERIODO_VIGENTE['NM_DIA'] == PARAMETROS["DIA_LOGISTICO"]]
        DATA_ARQ    = LINHA['DATA_ARQ'].values[0]
        INDEX       = LINHA.index[0]
        
        HORA        = (int(PARAMETROS["HORA"]) - 1)
        MARGEM      = PARAMETROS["MARGEM"]
        FERROVIA    = PARAMETROS["FERROVIA"]
        PREFIXO     = PARAMETROS["PREFIXO"]
        
        self.__abrir__()
        
        for i, SEGMENTO in enumerate(TIPO_VAGOES):

            COLUNA = HORA + (24 * (INDEX - 1))

            if not PARAMETROS[SEGMENTO] == "":

                VAGOES = int(PARAMETROS[SEGMENTO])
                self.full_CONDENSADOS[MARGEM]["SAIDAS"][SEGMENTOS[i]][COLUNA] = VAGOES

        self.jsCONDENSADOS[DATA_ARQ][MARGEM]["SAIDAS"]["PREFIXO"][HORA]  = PREFIXO
        self.jsCONDENSADOS[DATA_ARQ][MARGEM]["SAIDAS"]["FERROVIA"][HORA] = FERROVIA

        self.__salvar__()

        SUBIDA_DE_VAZIOS().ATUALIZAR()

