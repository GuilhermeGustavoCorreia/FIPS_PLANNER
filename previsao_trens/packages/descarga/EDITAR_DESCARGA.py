import json
import pandas as pd
import os

from django.db.models import Sum
from previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS import EDITAR_PARAMETROS
from previsao_trens.models  import Trem   
from datetime               import datetime, timedelta

class NAVEGACAO_DESCARGA:

    def __init__(self, TERMINAL, FERROVIA, PRODUTO, DIA_ANTERIOR=False):
      
        #region DECLARANDO OBJETOS GLOBAIS
        
        self.NM_TERMINAL = TERMINAL
        self.FERROVIA    = FERROVIA
        self.PRODUTO     = PRODUTO

        self.INFOS            : dict = {}
        self.DESCARGAS        : dict = {}
        self.LISTA_DATA_ARQ   : list

        #endregion

        #region INICIANDO OS OBJETOS GLOBAIS
        self.PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        
        #ESTOU REMOVENDO O D-1 DO CÁLCULO PARA VER NO QUE VAI DAR
        self.QT_COLUNAS_FULL = 144
        if not DIA_ANTERIOR:

            self.QT_COLUNAS_FULL = 120
            self.PERIODO_VIGENTE = self.PERIODO_VIGENTE.drop(self.PERIODO_VIGENTE.index[0]) 
        
        self.LISTA_DATA_ARQ  = self.PERIODO_VIGENTE["DATA_ARQ"].tolist()

        with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
            self.INFOS = json.load(ARQUIVO_DESCARGA)

        self.INFOS       = self.INFOS[TERMINAL]

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO_DESCARGA:
                DESCARGA = json.load(ARQUIVO_DESCARGA)

            self.DESCARGAS[DATA_ARQ] = DESCARGA

        #endregion

    #region FUNCOES INTERNAS
    
    def __CALCULAR_DESCARGA__(self):
        
        #DEVE ESTAR AQUI DENTRO, POIS UTILIZARÁ A DESCARGA COMPLETA
        def __CALCULA_FILA__():

            def __LIMPAR_OCUPACAO__():

                DESCARGA_COMPLETA["OCUPACAO"] = [0] * self.QT_COLUNAS_FULL
                
                for _ ,SALDO in enumerate(DESCARGA_COMPLETA["SALDO"]):
                    
                    if SALDO == 0: 
                        pass
            
            SALDO_VIRADA = self.DESCARGAS[self.LISTA_DATA_ARQ[0]]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"]

            

            #PRIMEIRO ANALISAR TODOS OS ENCOSTES 
            ORDEM_DE_CHEGADA = [ 
                UM_ENCOSTE + [index] for index, UM_ENCOSTE in enumerate(DESCARGA_COMPLETA["ENCOSTE"]) if UM_ENCOSTE != [0, 0]
            ]

            if SALDO_VIRADA > 0: ORDEM_DE_CHEGADA.insert(0, [SALDO_VIRADA, 101, 0],)


            __LIMPAR_OCUPACAO__()

            #ISTO É PARA A LOGICA DE UM TREM DESCARREGAR DIRETO DO OUTRO SEM ESPAÇO ENTRE OS "S A L D O S" DELES
            SOBRA_ANTERIOR_DE_VAGOES = 0
            for i, DADOS_FILA_DO_TREM in enumerate(ORDEM_DE_CHEGADA):
                
                QUANDO_O_TREM_ENCOSTA   = DADOS_FILA_DO_TREM[2]
                TAMANHO_DO_TREM         = DADOS_FILA_DO_TREM[0]
                ID_TREM                 = int(DADOS_FILA_DO_TREM[1])
                TREM_ACABOU_DESCARGA    = False
                HORA = QUANDO_O_TREM_ENCOSTA
                DIFERENCA = 0
                HORA_FINAL = HORA
     
                while not TREM_ACABOU_DESCARGA: 
                    TAMANHO_DO_TREM += SOBRA_ANTERIOR_DE_VAGOES 



                    if (DESCARGA_COMPLETA["PRODUTIVIDADE"][HORA_FINAL] - DESCARGA_COMPLETA["SALDO"][HORA_FINAL]) == 0 or HORA_FINAL == 119:      
                        TREM_ACABOU_DESCARGA    = True
                          
                    if DESCARGA_COMPLETA["OCUPACAO"][HORA_FINAL] ==  ID_TREM or DESCARGA_COMPLETA["OCUPACAO"][HORA_FINAL] == 0:
                        
                        if (DESCARGA_COMPLETA["PRODUTIVIDADE"][HORA_FINAL] >= TAMANHO_DO_TREM):
                            DIFERENCA = DESCARGA_COMPLETA["PRODUTIVIDADE"][HORA_FINAL] - TAMANHO_DO_TREM
  
                        DESCARGA_COMPLETA["OCUPACAO"][HORA_FINAL] = ID_TREM
                        HORA_FINAL += 1
       
                        TAMANHO_DO_TREM = TAMANHO_DO_TREM - DESCARGA_COMPLETA["PRODUTIVIDADE"][HORA_FINAL - 1] - DIFERENCA
    
                        if TAMANHO_DO_TREM <= 0:

                            if TAMANHO_DO_TREM < 0:

                                ORDEM_DE_CHEGADA[i + 1][0] = ORDEM_DE_CHEGADA[i + 1][0] + (0 - TAMANHO_DO_TREM)

                            TREM_ACABOU_DESCARGA = True

                    else:

                        HORA_FINAL += 1   

            #INSERIR NA LINHA DE OCUPACAO

        DESCARGA_COMPLETA = {}

        ITENS_DESCARGA = ["ENCOSTE", "SALDO", "PRODUTIVIDADE", "EDITADO","OCUPACAO", "RESTRICAO"]
        ITENS_SUBIDA   = ["GERACAO_DE_VAZIOS", "GERACAO_EDITADA", "ALIVIO_DE_VAZIOS", "ALIVIO_EDITADO"]
        
        for ITEM in ITENS_DESCARGA:
                DESCARGA_COMPLETA[ITEM] = []

        for ITEM in ITENS_SUBIDA:
                DESCARGA_COMPLETA[ITEM] = []

        PRODUTIVIDADE = self.INFOS["PRODUTIVIDADE"][self.FERROVIA][self.PRODUTO]
        
        #CRIANDO A DESCARGA ÚNICA (LINHAS CONSIDERADAS ABAIXO)
        
        for DATA_ARQ in self.LISTA_DATA_ARQ:  
                
            for ITEM in ITENS_DESCARGA:
                DESCARGA_COMPLETA[ITEM].extend(self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO][ITEM])
            
            for ITEM in ITENS_SUBIDA:
                DESCARGA_COMPLETA[ITEM].extend(self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["SUBIDA"][ITEM])


       #ITERANDO SOBRE A DESCARGA ÚNICA
        DESCARGA_COMPLETA["SALDO"][0] = 0

        for i, _ in enumerate(DESCARGA_COMPLETA["ENCOSTE"]):#AQUI PODERIA SER QUALQUER CHAVE, É PARA PEGARMOS O TAMANHO DA LISTA
            
            if i == 0: 

                SALDO_D0 = self.DESCARGAS[self.LISTA_DATA_ARQ[0]]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"]

                DESCARGA_COMPLETA["SALDO"][i-1]         = SALDO_D0
                DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = 0
                #DESCARGA_COMPLETA["ENCOSTE"][i]       = [0, 0]
                DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-1] = 0
                DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-2] = 0
            
            #ESTAS TRÊS REGRAS SÃO PARA O AUTOMATICO E O MANUAL
            if      DESCARGA_COMPLETA["SALDO"][i-1] == 0                                        : DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = 0 #(NÃO HÁ O QUE DESCARREGAR)
            elif    DESCARGA_COMPLETA["SALDO"][i-1] < DESCARGA_COMPLETA["SALDO"][i-1]           : DESCARGA_COMPLETA["SALDO"][i-1] = DESCARGA_COMPLETA["SALDO"][i-1] #(HÁ MENOS SALDO QUE PRODUTIVIDADE)
            if      DESCARGA_COMPLETA["SALDO"][i-1] < DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1]   : DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = DESCARGA_COMPLETA["SALDO"][i-1]#(NÃO HÁ O QUE DESCARREGAR)

            #AQUI FICA O CALCULO AUTOMATICO
            elif DESCARGA_COMPLETA["EDITADO"][i-1] == 0:
                if   DESCARGA_COMPLETA["SALDO"][i-1] >= PRODUTIVIDADE: 

                    #AQUI DEVEMOS INCLUIR O CALCULO COM RESTRICAO
                    if DESCARGA_COMPLETA["RESTRICAO"][i-1] > 0: 
                        DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = round(PRODUTIVIDADE * 0.01 * DESCARGA_COMPLETA["RESTRICAO"][i-1])
                    else:
                        DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = PRODUTIVIDADE
                else:
                    DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] = DESCARGA_COMPLETA["SALDO"][i-1]


            if i == 0:  SALDO = SALDO_D0 + DESCARGA_COMPLETA["ENCOSTE"][i][0]
            else:       SALDO = DESCARGA_COMPLETA["ENCOSTE"][i][0] + DESCARGA_COMPLETA["SALDO"][i-1] - DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1]
 
            if SALDO > 0 : DESCARGA_COMPLETA["SALDO"][i] = SALDO
            else         : DESCARGA_COMPLETA["SALDO"][i] = 0


            #MÓDULO DE VAZIOS (PODE SER REMOVIDO)

            DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-1] = DESCARGA_COMPLETA["PRODUTIVIDADE"][i-1] + DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-2]
            if DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-1] == DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-2]:
               DESCARGA_COMPLETA["GERACAO_DE_VAZIOS"][i-1] = 0


            #MÓDULO DE VAZIOS (PODE SER REMOVIDO)

        __CALCULA_FILA__()

        #VOLTANDO A DESCARGA ÚNICA AO NORMAL
        LISTAS : dict = {}

        for ITEM in ITENS_DESCARGA:
            LISTAS[ITEM] = [DESCARGA_COMPLETA[ITEM][i:i + 24] for i in range(0, len(DESCARGA_COMPLETA[ITEM]), 24)]
        
        for ITEM in ITENS_SUBIDA:
            LISTAS[ITEM] = [DESCARGA_COMPLETA[ITEM][i:i + 24] for i in range(0, len(DESCARGA_COMPLETA[ITEM]), 24)]

        for index, DATA_ARQ in enumerate(self.LISTA_DATA_ARQ):
        
            for ITEM in ITENS_DESCARGA:
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO][ITEM] = LISTAS[ITEM][index] #LISTA POSSUI O MESMO TAMANHO QUE O PERIODO ATIVO, COMPARTILHAM O INDEX

            for ITEM in ITENS_SUBIDA:
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["SUBIDA"][ITEM] = LISTAS[ITEM][index] #LISTA POSSUI O MESMO TAMANHO QUE O PERIODO ATIVO, COMPARTILHAM O INDEX


            if index != 0: #NÃO VAMOS DEFINIR O SALDO DE VIRADA DE "D" AUTOMARICAMENTE (index = 1 é "D" na lista self.LISTA_DATA_ARQ)
                
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"] = \
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["SALDO"][0] -\
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["ENCOSTE"][0][0]
            
    def __CALCULAR_TOTAIS__(self):

        INDICADORES = {
                "PEDRAS"  : {},
                "ENCOSTE" : {}
        }
        
        #ITERANDO SOBRE TODOS OS DIAS PARA QUE TODOS OS DIAS TENHAM SEUS TOTAIS ATUALIZADOS (NA DETALHE E NA NAVEGAÇÃO)
        for DATA_ARQ in self.LISTA_DATA_ARQ: #1
            
            #region OBTENDO OS INDICADORES POR PERÍODO (DE CADA FERROVIA E DE CADA PRODUTO)
            for FERROVIA in self.DESCARGAS[DATA_ARQ]["DESCARGAS"].keys():  #2
                
                INDICADORES["PEDRAS"][FERROVIA]  = {}
                INDICADORES["ENCOSTE"][FERROVIA] = {}

                for PRODUTO in self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA].keys(): #3

                    #A LINHA DE PRODUTIVIDADE COMPLETA (AUXILIAR)
                    LINHA_ENCOSTE       = self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["ENCOSTE"]
                    LINHA_PRODUTIVIDADE = self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"]

                    INDICADORES["PEDRAS"][FERROVIA][PRODUTO]  = LINHA_PRODUTIVIDADE
                    INDICADORES["ENCOSTE"][FERROVIA][PRODUTO] = LINHA_ENCOSTE

                    #RECEBIMENTOS POR PERIODO (PARA O RELATORIO DETALHE)
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][0] = sum(sublista[0] for sublista in LINHA_ENCOSTE[  : 6])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][1] = sum(sublista[0] for sublista in LINHA_ENCOSTE[ 6:12])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][2] = sum(sublista[0] for sublista in LINHA_ENCOSTE[12:18])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["RECEBIMENTOS"][3] = sum(sublista[0] for sublista in LINHA_ENCOSTE[18:  ])

                    #PRODUTIVIDADE POR PERIODO (PARA O RELATORIO DETALHE)
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][0] = sum(LINHA_PRODUTIVIDADE[  : 6])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][1] = sum(LINHA_PRODUTIVIDADE[ 6:12])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][2] = sum(LINHA_PRODUTIVIDADE[12:18])
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][3] = sum(LINHA_PRODUTIVIDADE[18:  ])



                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["TOTAL_CHEGADA"] = sum(sublista[0] for sublista in LINHA_ENCOSTE)
                    self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["TOTAL_PRODUTIVIDADE"]   = sum(LINHA_PRODUTIVIDADE)


            #endregion

            #region OBTENDO OS INDICADORES TOTAIS (PERIODO POR FERROVIA)  
            
            #ESTA VARIAVEL É PARA NAO SOMAR ERRADO, TESTAMOS SEM E NAO DEU CERTO.
            PEDRAS = {
                "RUMO" : {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "MRS"  : {"P1": 0, "P2": 0, "P3": 0, "P4": 0},
                "VLI"  : {"P1": 0, "P2": 0, "P3": 0, "P4": 0}
            }

            PEDRA = [] 
            ENCOSTE = [[0, 0] for _ in range(self.QT_COLUNAS_FULL)]
            SALDOS_VIDARA = [] #ISSO SERÁ SOMADO NA OFERTA DO DIA (ENCOSTES + SALDOS) <- DO LADO DA PEDRA NA NAVEGAÇÃO
                
            #LINHA DA PEDRA DA DESCARGA
            for FERROVIA in self.DESCARGAS[DATA_ARQ]["DESCARGAS"]:
                for PRODUTO in INDICADORES["PEDRAS"][FERROVIA]:

                    #ISSO É UM ARRAY []*24 QUE POSSUIRA TODAS AS PEDRAS SOMADAS (SERÁ A LINHA DA PEDRA ABEIXO DA CHEGADA).
                    PEDRA   = [x + y for x, y in zip(PEDRA, INDICADORES["PEDRAS"][FERROVIA][PRODUTO])]    if PEDRA   else INDICADORES["PEDRAS"][FERROVIA][PRODUTO]
                    
                    #SOMA OS ESCOSTES, NECESSÁRIO PARA FAZER O CALCULO DOS RECEBIMENTOS DO DIA (QUE LEVA EM CONTA TODOS OS ENCOSTES [NÃO AS CHEGADAS]
                    #ENCOSTE = [x + y for x, y in zip(ENCOSTE, INDICADORES["ENCOSTE"][FERROVIA][PRODUTO])] if ENCOSTE else INDICADORES["ENCOSTE"][FERROVIA][PRODUTO]
                    #print(f"ENCOSTE: {INDICADORES["ENCOSTE"]["ENCOSTE"]}")
                    for i in range(len(INDICADORES["ENCOSTE"][FERROVIA][PRODUTO])):
                        ENCOSTE[i][0] += INDICADORES["ENCOSTE"][FERROVIA][PRODUTO][i][0]
                    #ENCOSTE = [[sum(first_elements), 0] for first_elements in zip(*[lst[0] for lst in INDICADORES["ENCOSTE"][FERROVIA][PRODUTO]])]

                    #AQUI JUNTO TODOS OS SALDOS DE VIRADA DE UMA DESCARGA (ESTAMOS ITERANDO POR DIA ALI EM CIMA)
                    SALDOS_VIDARA.append(self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"])

                    #VEM SOMANDO AS PEDRAS DE CADA FERROVIA PARA OS QUADRADINHOS COLORIDOS ABAIXO DE CADA TABELA DESCARGA.
                    PEDRAS[FERROVIA]["P1"] += self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][0]
                    PEDRAS[FERROVIA]["P2"] += self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][1]
                    PEDRAS[FERROVIA]["P3"] += self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][2]
                    PEDRAS[FERROVIA]["P4"] += self.DESCARGAS[DATA_ARQ]["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["PEDRA"][3]

            


            #COLOCA AS SOMAS DAS PEDRAS POR FERROVIAS NA DESCARGA (QUADRADOS COLORIDOS EM BAIXO DA DESCARGA)
            PERIODOS = ["P1", "P2", "P3", "P4"]
            for FERROVIA in self.DESCARGAS[DATA_ARQ]["DESCARGAS"].keys():
                for PERIODO in PERIODOS: 
                    self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"][FERROVIA][PERIODO] = PEDRAS[FERROVIA][PERIODO]

            #SALDO TOTAL DO TERMINAL (LADO DA PEDRA EM TOTAIS NA DESCARGA
  
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["TOTAL_SALDO"] = sum(sublista[0] for sublista in ENCOSTE) + sum(SALDOS_VIDARA)

            #COLOCA AS SOMAS DAS PEDRAS POR PERIODOS (QUADRADOS PRETOS EM BAIXO DA DESCARGA)
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P1"] = PEDRAS["RUMO"]["P1"] + PEDRAS["MRS"]["P1"] + PEDRAS["VLI"]["P1"]
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P2"] = PEDRAS["RUMO"]["P2"] + PEDRAS["MRS"]["P2"] + PEDRAS["VLI"]["P2"]
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P3"] = PEDRAS["RUMO"]["P3"] + PEDRAS["MRS"]["P3"] + PEDRAS["VLI"]["P3"]
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P4"] = PEDRAS["RUMO"]["P4"] + PEDRAS["MRS"]["P4"] + PEDRAS["VLI"]["P4"]

            #PERA TOTAL DO TERMINAL (LADO DO SALDO TOTAL EM TOTAIS NA DESCARGA)
            self.DESCARGAS[DATA_ARQ]["INDICADORES"]["TOTAL_PEDRA"] =    self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P1"] + \
                                                                        self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P2"] + \
                                                                        self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P3"] + \
                                                                        self.DESCARGAS[DATA_ARQ]["INDICADORES"]["PEDRAS"]["TOTAL"]["P4"]
            #LINHA DA PEDRA
            self.DESCARGAS[DATA_ARQ]["PEDRA"] = PEDRA

    def __SALVAR__(self):

        DIRETORIO_DESCARGAS   =  "previsao_trens/src/DESCARGAS"
        DIRETORIO_TERMINAL = f'{ DIRETORIO_DESCARGAS }/{self.NM_TERMINAL}'

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            ARQUIVO = f"descarga_{ DATA_ARQ }.json"
            with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
                json.dump(self.DESCARGAS[DATA_ARQ], ARQUIVO_NOME, indent=4)

    #endregion
    
    

    #endregion

    def EDITAR_TREM(self, TREM, ACAO):
        
        #region FUNCOES UTILIZADAS SOMENTE EM EDITAR TREM
           
        def __CHEGADA__(HORA, TREM_DATA_ARQ):
        
            PREFIXO          : str
            TOTAL_VAGOES     : int

            #region DEFININDO POSICAO DA CHEGADA
            if HORA > 0 :

                HORA_CHEGADA     = HORA - 1
                DATA_ARQ_CHEGADA = TREM_DATA_ARQ

            else: #CASO SEJA = 0, SERÁ NO DIA ANTERIOR ÀS 23h
            
                HORA_CHEGADA     = 23 
                DATA_ARQ_CHEGADA = self.LISTA_DATA_ARQ[self.LISTA_DATA_ARQ.index(TREM_DATA_ARQ) - 1]

            #endregion 
            
            TRENS_CHEGADA = Trem.objects.filter(terminal=self.NM_TERMINAL, previsao=TREM['previsao'])
            PRIMEIRO_TREM = TRENS_CHEGADA.first()
            
            TODOS_IDs_DESTA_CHEGADA = []
            
            SOMA_VAGOES  = TRENS_CHEGADA.aggregate(TOTAL_VAGOES=Sum('vagoes'))
            TOTAL_VAGOES = SOMA_VAGOES['TOTAL_VAGOES']

            #CASO EXISTA TREM
            if PRIMEIRO_TREM:
                PREFIXO = PRIMEIRO_TREM.prefixo
                TODOS_IDs_DESTA_CHEGADA = list(Trem.objects.filter(terminal=self.NM_TERMINAL, previsao=TREM['previsao']).values_list('pk', flat=True))
                print(TODOS_IDs_DESTA_CHEGADA)

            #CASO NAO EXISTA
            else:
                PREFIXO      = 0
                TOTAL_VAGOES = 0
                

            self.DESCARGAS[DATA_ARQ_CHEGADA]["PREFIXO"][HORA_CHEGADA][0] = PREFIXO    
            self.DESCARGAS[DATA_ARQ_CHEGADA]["PREFIXO"][HORA_CHEGADA][1] = TODOS_IDs_DESTA_CHEGADA
            
            self.DESCARGAS[DATA_ARQ_CHEGADA]["CHEGADA"][HORA_CHEGADA][0] = TOTAL_VAGOES
            self.DESCARGAS[DATA_ARQ_CHEGADA]["CHEGADA"][HORA_CHEGADA][1] = TODOS_IDs_DESTA_CHEGADA

            return HORA_CHEGADA, DATA_ARQ_CHEGADA

        def __ENCOSTE__(HORA_CHEGADA, DATA_ARQ_CHEGADA, ACAO):

            

            VAGOES          : int
            HORA_ENCOSTE    : int
            DATA_ARQ_ENCOSTE: str

            HORA_ENCOSTE     = self.INFOS["SLA"] + HORA_CHEGADA
            DATA_ARQ_ENCOSTE = DATA_ARQ_CHEGADA

            VAGOES = 0
            TREM_ID = 0
            if ACAO == "INSERIR": 
                VAGOES = TREM["vagoes"]
                TREM_ID = TREM["ID"]

            POSICAO_DIA = self.LISTA_DATA_ARQ.index(DATA_ARQ_CHEGADA)

            if ((HORA_ENCOSTE) >= 24 and POSICAO_DIA < 6):

                HORA_ENCOSTE     = HORA_ENCOSTE - 24
                DATA_ARQ_ENCOSTE = self.LISTA_DATA_ARQ[ POSICAO_DIA + 1]

            print(f"antes do encoste{ self.DESCARGAS[DATA_ARQ_ENCOSTE] }")
            self.DESCARGAS[DATA_ARQ_ENCOSTE]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["ENCOSTE"][HORA_ENCOSTE][1] = TREM_ID
            self.DESCARGAS[DATA_ARQ_ENCOSTE]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["ENCOSTE"][HORA_ENCOSTE][0] = VAGOES
            print(f"antes do encoste{ self.DESCARGAS[DATA_ARQ_ENCOSTE] }")
            
        def __ATIVAR_TERMINAL__(ACAO):
            
            DESC_ATV = -1

            if ACAO == "INSERIR":
                DESC_ATV = 1

            PARAMETROS = {

                "NOVO_VALOR":   DESC_ATV,
                "LINHA":        self.NM_TERMINAL,
                "COLUNA":       f'{self.FERROVIA}_{self.PRODUTO}',
                "TABELA":       "DESCARGAS_ATIVAS.csv",

            }
            EDITAR_PARAMETROS(PARAMETROS, "SOMAR")
        
        #endregion      
        TREM_DATA_ARQ    = TREM['previsao'].strftime('%Y-%m-%d')
        HORA             = TREM['previsao'].hour

        __ATIVAR_TERMINAL__(ACAO)

        HORA_CHEGADA, DATA_ARQ_CHEGADA = __CHEGADA__(HORA, TREM_DATA_ARQ)
        __ENCOSTE__(HORA_CHEGADA, DATA_ARQ_CHEGADA, ACAO)

        self.__CALCULAR_DESCARGA__()
        self.__CALCULAR_TOTAIS__()
        self.__SALVAR__()

    def EDITAR_PRODUTIVIDADE(self, PARAMETROS): 

        def __INSERIR_VALORES__():

            DATA_ARQ = PARAMETROS["DATA_ARQ"]
            for COLUNA in PARAMETROS["CELULAS"]:

                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["PRODUTIVIDADE"][COLUNA] = PARAMETROS["VALOR"]
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["EDITADO"][COLUNA]       = 1
       
       
        __INSERIR_VALORES__()

        self.__CALCULAR_DESCARGA__()
        self.__CALCULAR_TOTAIS__()
        self.__SALVAR__()

        DESCARGAS = []

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            DESCARGAS.append(self.DESCARGAS[DATA_ARQ])
            
        return DESCARGAS

    def EDITAR_SALDO_VIRADA(self, PARAMETROS):

        self.DESCARGAS[self.LISTA_DATA_ARQ[0]]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"] = PARAMETROS["VALOR"]

        self.__CALCULAR_DESCARGA__()
        self.__CALCULAR_TOTAIS__()
        self.__SALVAR__()

        DESCARGAS = []

        for DATA_ARQ in self.LISTA_DATA_ARQ:

            DESCARGAS.append(self.DESCARGAS[DATA_ARQ])
            
        return DESCARGAS

    def EDITAR_RESTRICAO(self, RESTRICAO, ACAO):
        

        # AQUI INSIRO E REMOVO RESTRICOES

        # 1. AQUI RECEBEMOS RESTRICOES VALIDADAS
        # 2. ATIVAMOS A RESTRICAO NA DESCARGA (NÃO TINHA ONDE COLOCAR ESTA FUNCAO...)
        # 3. TRATAMOS RESTRICOES QUE VAO ALÉM DE D-4 (EM CASO DE INSERIR) (LINHA 337 procurar por RESTRICAO_TERMINA_NO_PERIODO_VIGENTE )
        # 4. EXCLUIMOS RESTRICOES QUE VAO ALÉM DE D-1 (DENTRO DO IF ACAO == "REMOVER")

        #region PARAMETROS
        FERROVIAS               : list
        DIAS_AFETADOS           : int
        DATAS_AFETADAS          : dict
        DATAS_AFETADAS_FULL     : list
        FIM_APLICACAO_RESTRICAO : str

        DATA_INICIO             : datetime
        POSICAO_HORA_INICIO     : int

        DATA_FINAL              : datetime
        POSICAO_HORA_FINAL      : int

        MOTIVO                  : str
        PCT                     : int
        #endregion
        
        MOTIVO = RESTRICAO["motivo"]
        PCT    = RESTRICAO["porcentagem"]

        print(RESTRICAO)


        VALOR_ATIVACAO = 1
        if ACAO == "REMOVER":
            MOTIVO = ""
            PCT    = 0
            VALOR_ATIVACAO = 0

            #PODEMOS EXCLUIR UMA RESTRICAO QUE TENHA COMEÇADO ANTES DE D-1 (ISTO DEVERIA CONTORNAR O ERRO)
            if not (RESTRICAO["comeca_em"].strftime('%Y-%m-%d') in self.LISTA_DATA_ARQ):    
                RESTRICAO["comeca_em"] = datetime.strptime(self.PERIODO_VIGENTE.iloc[0]["DATA_ARQ"], "%Y-%m-%d").replace(hour=1, minute=0, second=0)
        

        #region ATIVANDO RESTRICAO NA NAVEGACAO
        
        DIRETORIO_RESTRICOES_ATIVAS = "previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv"

        RESTRICOES_ATIVAS = pd.read_csv(DIRETORIO_RESTRICOES_ATIVAS, sep=";", index_col=0)

        RESTRICOES_ATIVAS.loc[RESTRICAO["terminal"],    RESTRICAO["mercadoria"]] = VALOR_ATIVACAO
        RESTRICOES_ATIVAS.loc[RESTRICAO["terminal"],    "RESTRICAO"]             = RESTRICOES_ATIVAS.loc[RESTRICAO["terminal"], RESTRICOES_ATIVAS.columns[1:]].sum()

        RESTRICOES_ATIVAS.to_csv(DIRETORIO_RESTRICOES_ATIVAS, sep=";")

        #endregion


        #PRIMEIRO PRECISAMOS SABER EM QUANTAS FERROVIAS VAMOS APLICAR (POIS NEM TODOS OS TERMINAIS TEM TODAS AS FERROVIAS)       
        FERROVIAS = self.INFOS["FERROVIA"]

        #PODEMOS INSERIR DO INICIO AO FIM OU DO INICIO ATÉ D+4 23:00

        #region DEFININDO ATÉ QUANDO VAI A RESTRIÇÃO (CASO ULTRAPASSE D+4)
        RESTRICAO_TERMINA_NO_PERIODO_VIGENTE = RESTRICAO["termina_em"].strftime('%Y-%m-%d') in self.LISTA_DATA_ARQ

        FIM_APLICACAO_RESTRICAO = datetime.strptime(self.LISTA_DATA_ARQ[4] + ' 23', '%Y-%m-%d %H')
        if (RESTRICAO_TERMINA_NO_PERIODO_VIGENTE):
            FIM_APLICACAO_RESTRICAO = RESTRICAO["termina_em"]

        #endregion
        
        #DEFININDO AS LINHAS DE RESTRIÇÃO QUE SERÃO APLICADAS NA DESCARGA
        
        #region DEFININDO AS POSIÇÕES DO INICIO E FIM (CASOS ONDE INCLUEM 00:00 E VIRAM O DIA ANTERIOR)
        DATA_INICIO         = RESTRICAO["comeca_em"].date()
        POSICAO_HORA_INICIO = RESTRICAO["comeca_em"].hour - 1

        if RESTRICAO["comeca_em"].hour == 0: 

            DATA_INICIO         = (RESTRICAO["comeca_em"].date() - timedelta(days=1))
            POSICAO_HORA_INICIO =  23

        DATA_FINAL              = FIM_APLICACAO_RESTRICAO.date()
        POSICAO_HORA_FINAL      = FIM_APLICACAO_RESTRICAO.hour - 1

        if FIM_APLICACAO_RESTRICAO.hour == 0:

            DATA_FINAL         = (FIM_APLICACAO_RESTRICAO.date() - timedelta(days=1))
            POSICAO_HORA_FINAL =  24
        #endregion

        #0 é o mesmo dia 
        #1 é de um dia para o outro
        #2 -> possui (HOJE: 0, PROXIMO DIA: 1, ULTIMO_DIA: 2) APLICAREMOS FULL RESTRICAO EM 1
        
        DIAS_AFETADOS = DATA_FINAL - DATA_INICIO
        DIAS_AFETADOS = DIAS_AFETADOS.days
        
        DATAS_AFETADAS = {}
        #region MONTANDO O DICIONARIO COM AS LISTAS DE RESTRICOES QUE VAMOS INSERIR
        if DIAS_AFETADOS > 0:
            for DIA in range(DIAS_AFETADOS + 1):

                DATA_ARQ = (DATA_INICIO + timedelta(days=DIA)).strftime('%Y-%m-%d')
                DATAS_AFETADAS[DATA_ARQ] = []
                
            PRIMEIRO_DIA = next(iter(DATAS_AFETADAS))
            ULTIMO_DIA  = next(reversed(DATAS_AFETADAS))
            
            DATAS_AFETADAS_FULL = list(DATAS_AFETADAS.keys())

            DATAS_AFETADAS_FULL.remove(PRIMEIRO_DIA)
            DATAS_AFETADAS_FULL.remove(ULTIMO_DIA)

            DATAS_AFETADAS[PRIMEIRO_DIA] = [0 if i < (POSICAO_HORA_INICIO) else PCT for i in range(24)]

            for DATA_ARQ in DATAS_AFETADAS_FULL:
                DATAS_AFETADAS[DATA_ARQ] = [PCT] * 24

            DATAS_AFETADAS[ULTIMO_DIA] = [PCT if i < (POSICAO_HORA_FINAL) else 0 for i in range(24)]
    
        else: #NESTE CASO COMECA E ACABA NO MESMO DIA
            DATA_ARQ = DATA_INICIO.strftime('%Y-%m-%d')
            DATAS_AFETADAS[DATA_ARQ] = [PCT if POSICAO_HORA_INICIO <= i < (POSICAO_HORA_FINAL) else 0 for i in range(24)]

        
        #endregion
        
        #region INSERINDO AS RESTRICOES NAS DESCARGAS
        for DATA_ARQ in DATAS_AFETADAS:
            for FERROVIA in FERROVIAS:

                self.FERROVIA = FERROVIA
                self.DESCARGAS[DATA_ARQ]["DESCARGAS"][self.FERROVIA][self.PRODUTO]["RESTRICAO"] = DATAS_AFETADAS[DATA_ARQ]
                self.DESCARGAS[DATA_ARQ]["RESTRICAO_MOTIVO"] = [MOTIVO if valor > 0 else valor for valor in DATAS_AFETADAS[DATA_ARQ]]
                
                self.__CALCULAR_DESCARGA__()

        #endregion
        
        self.__CALCULAR_TOTAIS__()
        self.__SALVAR__()

    #ESTA FUNCAO É CHAMADA EM CONFIGURACAO.ATUALIZAR_DESCARA (PARA INSERIR AS RESTRICOES NOS DIAS QUE ULTRAPASSAVAM D+4)
    def RESTRICAO_ATUALIZAR_PERIODO(self, RESTRICAO, ULTIMO_DIA_ANTIGO, ULTIMO_DIA_NOVO):

        RESTRICAO["comeca_em"] = ULTIMO_DIA_ANTIGO
        self.EDITAR_RESTRICAO(self, RESTRICAO, "INSERIR")

    def ATUALIZAR_CALCULO(self):

        self.__CALCULAR_DESCARGA__()
        self.__CALCULAR_TOTAIS__()
        self.__SALVAR__()