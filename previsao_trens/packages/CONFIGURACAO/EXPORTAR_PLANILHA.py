import  json
from    openpyxl                import load_workbook
from    datetime                import datetime
from    previsao_trens.models   import Trem, Restricao, TremVazio
import  pandas as pd
from    django.conf import settings
import  os

class EXPORTAR_PLANILHA():

    def __init__(self):

        self.PLANILHA           = load_workbook("previsao_trens/src/DICIONARIOS/planilha_planner.xlsx", keep_vba=True) 
        self.PERIODO_VIGENTE    = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        
    def atualizar_a_data(self):

        LINHA       = self.PERIODO_VIGENTE[self.PERIODO_VIGENTE['NM_DIA'] == "D"]
        DATA_ARQ    = LINHA['DATA_ARQ'].values[0]
        DATETIME_D  = datetime.strptime(DATA_ARQ, "%Y-%m-%d")
        
        PREVISAO = self.PLANILHA['PREVISAO']    
        PREVISAO['X5'].value = DATETIME_D

    def inserir_previsao(self):

        DIAS_LOGISTICOS     = ["D", "D+1", "D+2", "D+3", "D+4"]
        CRIAR_TREM          = self.PLANILHA['PREVISAO']
        PREVISOES           = {}
     
        for i, DIA_LOGISTICO in enumerate(DIAS_LOGISTICOS):

            PREVISOES[DIA_LOGISTICO] = ""

            LINHA    = self.PERIODO_VIGENTE[self.PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO]
            DATA_ARQ = LINHA['DATA_ARQ'].values[0]
            DATETIME = datetime.strptime(DATA_ARQ, "%Y-%m-%d")

            QUERYSET = Trem.objects.filter(
                previsao__year  = DATETIME.year,
                previsao__month = DATETIME.month,
                previsao__day   = DATETIME.day
            ).order_by('posicao_previsao')
            
            if QUERYSET.exists():
                     
                for j, TREM in enumerate(QUERYSET):

                    j = j + 5 # É PQ COMEÇA NA LINHA 5

                    CRIAR_TREM.cell(row = j, column=2  + (11 * i),   value=TREM.posicao_previsao)
                    CRIAR_TREM.cell(row = j, column=3  + (11 * i),   value=TREM.prefixo)
                    CRIAR_TREM.cell(row = j, column=4  + (11 * i),   value=TREM.os)
                    CRIAR_TREM.cell(row = j, column=5  + (11 * i),   value=TREM.origem)
                    CRIAR_TREM.cell(row = j, column=6  + (11 * i),   value=TREM.destino)              
                    CRIAR_TREM.cell(row = j, column=7  + (11 * i),   value=TREM.terminal)
                    CRIAR_TREM.cell(row = j, column=8  + (11 * i),   value=TREM.vagoes)
                    CRIAR_TREM.cell(row = j, column=9  + (11 * i),   value=TREM.mercadoria)
                    CRIAR_TREM.cell(row = j, column=10 + (11 * i),   value=TREM.previsao.replace(tzinfo=None))
                    CRIAR_TREM.cell(row = j, column=11 + (11 * i),   value=TREM.ferrovia)

    def inserir_navegacao(self):

        NAVEGACAO = self.PLANILHA['NAVEGACAO']  
        COLUNAS   = { "D": 5, "D+1": 35, "D+2": 65, "D+3": 95, "D+4": 125 }

        with open(f"previsao_trens/src/DICIONARIOS/MAPA_TERMINAIS_EXCEL.json") as ARQUIVO:
            map_TERMINAIS = json.load(ARQUIVO)

        PERIODO_VIGENTE    = pd.read_csv("previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",   encoding='utf-8-sig', sep=';', index_col=0)
        TERMINAIS_ATIVOS   = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
        RESTRICOES_ATIVAS  = pd.read_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv", encoding='utf-8-sig', sep=';', index_col=0)

        lsTERMINAIS_ATIVOS      = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
        lsTERMINAIS_DESATIVADOS = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] == 0].index.tolist() 
        TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)

        TERMINAIS_COM_RESTRICAO = RESTRICOES_ATIVAS[RESTRICOES_ATIVAS['RESTRICAO'] > 0].index.tolist()
        TERMINAIS_SEM_RESTRICAO = RESTRICOES_ATIVAS[RESTRICOES_ATIVAS['RESTRICAO'] == 0].index.tolist()

        for TERMINAL in lsTERMINAIS_ATIVOS:
            
            if TERMINAL in map_TERMINAIS:

                #region OCULTANDO RESTRICAO SE NÃO HOUVER 
                
                if TERMINAL in TERMINAIS_SEM_RESTRICAO:
                    
                    LINHA_PCT    = map_TERMINAIS[TERMINAL]["LIMITES"]["FIM"]
                    LINHA_MOTIVO = map_TERMINAIS[TERMINAL]["LIMITES"]["FIM"] - 1
                    
                    NAVEGACAO.row_dimensions[LINHA_PCT].hidden = True 
                    NAVEGACAO.row_dimensions[LINHA_MOTIVO].hidden = True 


               
                #endregion

                DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
                DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]  

                LINHA_PREFIXO = map_TERMINAIS[TERMINAL]["LIMITES"]["INICIO"] + 2
                LINHA_VAGOES  = map_TERMINAIS[TERMINAL]["LIMITES"]["INICIO"] + 3

                #region INSERINDO VALORES
                for DIA in COLUNAS.keys():

                    DATA_ARQ = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA].iloc[0]['DATA_ARQ']

                    with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO_DESCARGA:
                        DESCARGA = json.load(ARQUIVO_DESCARGA)

                    #region INSERINDO PREFIXO E CHEGADA
                    for i in range(24):
                        
                        NAVEGACAO.cell(row =LINHA_PREFIXO, column=(i + COLUNAS[DIA]),   value=DESCARGA["PREFIXO"][i][0])
                        NAVEGACAO.cell(row =LINHA_VAGOES,  column=(i + COLUNAS[DIA]),   value=DESCARGA["CHEGADA"][i][0])
                        
                    #endregion

                    #region INSERINDO DESCARGAS
                    for DESCARGA_ATIVA in DESCARGAS_ATIVAS:
                        
                        FERROVIA = DESCARGA_ATIVA[0]
                        PRODUTO  = DESCARGA_ATIVA[1] 

                        LINHA_ENCOSTE       = map_TERMINAIS[TERMINAL][FERROVIA][PRODUTO]
                        LINHA_PRODUTIVIDADE = LINHA_ENCOSTE + 2

                        if DIA == "D":
                            SALDO_VIRADA = DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["INDICADORES"]["SALDO_DE_VIRADA"]
                            NAVEGACAO.cell(row =LINHA_ENCOSTE + 1, column=4,   value=SALDO_VIRADA)

                        for i in range(24):
                        
                            NAVEGACAO.cell(row =LINHA_ENCOSTE,         column=(i + COLUNAS[DIA]),   value=DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["ENCOSTE"][i][0])
                            NAVEGACAO.cell(row =LINHA_PRODUTIVIDADE,   column=(i + COLUNAS[DIA]),   value=DESCARGA["DESCARGAS"][FERROVIA][PRODUTO]["PRODUTIVIDADE"][i])


                    #endregion
                    


                    if TERMINAL in TERMINAIS_COM_RESTRICAO:

                        DESCARGAS_RESTRICOES    = RESTRICOES_ATIVAS.drop('RESTRICAO', axis=1)
                        PRODUTO_RESTRICAO       = DESCARGAS_RESTRICOES.loc[TERMINAL][DESCARGAS_RESTRICOES.loc[TERMINAL] > 0].index.tolist()

                        #É PARA PEGAR UMA RESTRICAO
                        FERROVIA_ALEATORA_DO_TERMINAL = next(iter(DESCARGA["DESCARGAS"]))

                        DESCARGA["RESTRICAO_PCT"] = DESCARGA["DESCARGAS"][FERROVIA_ALEATORA_DO_TERMINAL][PRODUTO_RESTRICAO[0]]["RESTRICAO"]

                        LINHA_PCT    = map_TERMINAIS[TERMINAL]["LIMITES"]["FIM"]
                        LINHA_MOTIVO = map_TERMINAIS[TERMINAL]["LIMITES"]["FIM"] - 1

                        for i in range(24):
                            if not  DESCARGA["RESTRICAO_PCT"][i] == 0:
                                NAVEGACAO.cell(row =LINHA_PCT,     column=(i + COLUNAS[DIA]),  value=DESCARGA["RESTRICAO_PCT"][i])
                                NAVEGACAO.cell(row =LINHA_MOTIVO,  column=(i + COLUNAS[DIA]),  value=DESCARGA["RESTRICAO_MOTIVO"][i])

                #endregion   

                #region OCULTANDO DESCARDAS DESATIVADAS

                DESCARGAS_DESATIVADAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] == 0].index.tolist()
                DESCARGAS_DESATIVADAS = [item.split('_') for item in DESCARGAS_DESATIVADAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]  
    
                for DESCARGA_DESATIVA in DESCARGAS_DESATIVADAS:

                    FERROVIA = DESCARGA_DESATIVA[0]
                    PRODUTO  = DESCARGA_DESATIVA[1] 

                    if FERROVIA in map_TERMINAIS[TERMINAL] and PRODUTO in map_TERMINAIS[TERMINAL][FERROVIA]:

                        LINHA_ENCOSTE       = map_TERMINAIS[TERMINAL][FERROVIA][PRODUTO]
                        LINHA_SALDO         = map_TERMINAIS[TERMINAL][FERROVIA][PRODUTO]  + 1
                        LINHA_PRODUTIVIDADE = map_TERMINAIS[TERMINAL][FERROVIA][PRODUTO]  + 2

                        NAVEGACAO.row_dimensions[LINHA_ENCOSTE].hidden       = True
                        NAVEGACAO.row_dimensions[LINHA_SALDO].hidden         = True
                        NAVEGACAO.row_dimensions[LINHA_PRODUTIVIDADE].hidden = True
                #endregion

        #region REMOVENDO TERMINAIS DESATIVOS
        for TERMINAL in lsTERMINAIS_DESATIVADOS:
            if TERMINAL in map_TERMINAIS:
                TAMANHO_TERMINAL = map_TERMINAIS[TERMINAL]["LIMITES"]
                for i in range(TAMANHO_TERMINAL["INICIO"], TAMANHO_TERMINAL["FIM"] +2):
                   
                    NAVEGACAO.row_dimensions[i].hidden = True            
        #endregion

    def inserir_restricao(self):


        RESTRICOES = Restricao.objects.all()
        wsRESTRICAO = self.PLANILHA['RESTRICAO']   

        for i, RESTRICAO in enumerate(RESTRICOES):

            i = i + 5 # É PQ COMEÇA NA LINHA 5

            wsRESTRICAO.cell(row = i, column=2,   value=i-5)
            wsRESTRICAO.cell(row = i, column=3,   value=RESTRICAO.terminal)
            wsRESTRICAO.cell(row = i, column=4,   value=RESTRICAO.mercadoria)

            wsRESTRICAO.cell(row = i, column=5,   value=RESTRICAO.comeca_em.replace(tzinfo=None))
            wsRESTRICAO.cell(row = i, column=6,   value=RESTRICAO.termina_em.replace(tzinfo=None))

            wsRESTRICAO.cell(row = i, column=7,   value=RESTRICAO.porcentagem)
            wsRESTRICAO.cell(row = i, column=8,   value=RESTRICAO.motivo)
            wsRESTRICAO.cell(row = i, column=9,   value=RESTRICAO.comentario)

    def inserir_folha_capa(self, USUARIO_LOGADO):
        
        HOME          = self.PLANILHA['HOME']
        
        HOME.cell(row = 6, column=5,  value=f"{USUARIO_LOGADO.first_name} {USUARIO_LOGADO.last_name}" )
        HOME.cell(row = 7, column=5,  value=USUARIO_LOGADO.email )
        HOME.cell(row = 8, column=5,  value=datetime.today())

    def inserir_previsao_subida(self):

        SUBIDA = self.PLANILHA['SUBIDA']

        QUERYSET = TremVazio.objects.filter(margem  = "DIREITA").order_by('previsao')

        for j, TREM in enumerate(QUERYSET):

            j = j + 4 # É PQ COMEÇA NA LINHA 5

            SUBIDA.cell(row = j, column=2,   value=j - 4)
            SUBIDA.cell(row = j, column=3,   value=TREM.prefixo)
            SUBIDA.cell(row = j, column=4,   value=TREM.ferrovia)
            SUBIDA.cell(row = j, column=5,   value=TREM.previsao.replace(tzinfo=None))
            SUBIDA.cell(row = j, column=6,   value=TREM.eot)

            SUBIDA.cell(row = j, column=7,    value=TREM.qt_graos)
            SUBIDA.cell(row = j, column=8,    value=TREM.qt_ferti)
            SUBIDA.cell(row = j, column=9,    value=TREM.qt_celul)
            SUBIDA.cell(row = j, column=10,   value=TREM.qt_acuca)
            SUBIDA.cell(row = j, column=11,   value=TREM.qt_contei)

            SUBIDA.cell(row = j, column=12,   value=TREM.loco_1)
            SUBIDA.cell(row = j, column=13,   value=TREM.loco_2)
            SUBIDA.cell(row = j, column=14,   value=TREM.loco_3)
            SUBIDA.cell(row = j, column=15,   value=TREM.loco_4)
            SUBIDA.cell(row = j, column=16,   value=TREM.loco_5)

        QUERYSET = TremVazio.objects.filter(margem  = "ESQUERDA").order_by('previsao')

        for j, TREM in enumerate(QUERYSET):

            j = j + 4 # É PQ COMEÇA NA LINHA 5

            SUBIDA.cell(row = j, column=18,   value=j - 4)
            SUBIDA.cell(row = j, column=19,   value=TREM.prefixo)
            SUBIDA.cell(row = j, column=20,   value=TREM.ferrovia)
            SUBIDA.cell(row = j, column=21,   value=TREM.previsao.replace(tzinfo=None))
            SUBIDA.cell(row = j, column=22,   value=TREM.eot)

            SUBIDA.cell(row = j, column=23,   value=TREM.qt_graos)
            SUBIDA.cell(row = j, column=24,   value=TREM.qt_ferti)
            SUBIDA.cell(row = j, column=25,   value=TREM.qt_celul)
            SUBIDA.cell(row = j, column=26,   value=TREM.qt_acuca)
            SUBIDA.cell(row = j, column=27,   value=TREM.qt_contei)

            SUBIDA.cell(row = j, column=28,   value=TREM.loco_1)
            SUBIDA.cell(row = j, column=29,   value=TREM.loco_2)
            SUBIDA.cell(row = j, column=30,   value=TREM.loco_3)
            SUBIDA.cell(row = j, column=31,   value=TREM.loco_4)
            SUBIDA.cell(row = j, column=32,   value=TREM.loco_5)
    
    def salvar(self):
        
        caminho_static  = os.path.join(settings.STATIC_URL, 'downloads')
        caminho_arquivo = os.path.join(caminho_static, "PLANILHA_DESCARGA.xlsm")
        self.PLANILHA.save(caminho_arquivo)

def gerar_planilha(USUARIO_LOGADO):
    



    PLANILHA = EXPORTAR_PLANILHA()
    PLANILHA.inserir_previsao()
    PLANILHA.inserir_navegacao()
    PLANILHA.inserir_restricao()
    PLANILHA.inserir_previsao_subida()
    PLANILHA.inserir_folha_capa(USUARIO_LOGADO)
    #PLANILHA.salvar()
    
    return PLANILHA.PLANILHA
    


