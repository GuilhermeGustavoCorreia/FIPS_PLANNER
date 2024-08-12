import  json
from    openpyxl                import load_workbook
from    datetime                import datetime, timedelta, timezone
from    previsao_trens.models   import Trem, Restricao, TremVazio
import  pandas as pd
from    django.conf import settings
import  os

tipo_desc_linhas = {

            'TGG_RUMO_FARELO': 17, 
            'TGG_MRS_FARELO':  20, 
            'TGG_VLI_FARELO':  23,
            'TGG_RUMO_SOJA':   26, 
            'TGG_MRS_SOJA':    29, 
            'TGG_VLI_SOJA':    32,
            'TGG_RUMO_MILHO':  35, 
            'TGG_MRS_MILHO':   38, 
            'TGG_VLI_MILHO':   41,

            'TEG_RUMO_FARELO':  55,
            'TEG_MRS_FARELO':   58,
            'TEG_VLI_FARELO':   61,
            'TEG_RUMO_SOJA':    64,
            'TEG_MRS_SOJA':     67,
            'TEG_VLI_SOJA':     70,
            'TEG_RUMO_MILHO':   73,
            'TEG_MRS_MILHO':    76,
            'TEG_VLI_MILHO':    79,

            'TEAG_RUMO_FARELO':  93,
            'TEAG_MRS_FARELO':   96,
            'TEAG_VLI_FARELO':   99,
            'TEAG_RUMO_SOJA':   102,
            'TEAG_MRS_SOJA':    105,
            'TEAG_VLI_SOJA':    108,
            'TEAG_RUMO_MILHO':  111,
            'TEAG_MRS_MILHO':   114,
            'TEAG_VLI_MILHO':   117,

            'TEAG ACUCAR_RUMO_ACUCAR': 131,
            'TEAG ACUCAR_MRS_ACUCAR':  134,
            'TEAG ACUCAR_VLI_ACUCAR':  137,

            'CUTRALE_RUMO_FARELO':  151,
            'CUTRALE_MRS_FARELO':   154,
            'CUTRALE_VLI_FARELO':   157,
            'CUTRALE_RUMO_SOJA':    160,
            'CUTRALE_MRS_SOJA':     163,
            'CUTRALE_VLI_SOJA':     166,
            'CUTRALE_RUMO_MILHO':   169,
            'CUTRALE_MRS_MILHO':    172,
            'CUTRALE_VLI_MILHO':    175,

            'TIPLAM_RUMO_ACUCAR':   189,
            'TIPLAM_MRS_ACUCAR':    192,
            'TIPLAM_VLI_ACUCAR':    195,

            'TIPLAM_RUMO_FARELO':   209,
            'TIPLAM_MRS_FARELO':    212,
            'TIPLAM_VLI_FARELO':    215,
            'TIPLAM_RUMO_SOJA':     218,
            'TIPLAM_MRS_SOJA':      221,
            'TIPLAM_VLI_SOJA':      224,
            'TIPLAM_RUMO_MILHO':    227,
            'TIPLAM_MRS_MILHO':     230,
            'TIPLAM_VLI_MILHO':     233,

            'T39_RUMO_FARELO':      248,
            'T39_MRS_FARELO':       251,
            'T39_VLI_FARELO':       254,
            'T39_RUMO_SOJA':        257,
            'T39_MRS_SOJA':         260,
            'T39_VLI_SOJA':         263,
            'T39_RUMO_MILHO':       266,
            'T39_MRS_MILHO':        269,
            'T39_VLI_MILHO':        272,

            'TES_RUMO_FARELO':      286,
            'TES_MRS_FARELO':       289,
            'TES_VLI_FARELO':       292,
            'TES_RUMO_SOJA':        295,
            'TES_MRS_SOJA':         298,
            'TES_VLI_SOJA':         301,
            'TES_RUMO_MILHO':       304,
            'TES_MRS_MILHO':        307,
            'TES_VLI_MILHO':        310,

            'MOEGA V_RUMO_FARELO':  324,
            'MOEGA V_MRS_FARELO':   327,
            'MOEGA V_VLI_FARELO':   330,
            'MOEGA V_RUMO_SOJA':    333,
            'MOEGA V_MRS_SOJA':     336,
            'MOEGA V_VLI_SOJA':     339,
            'MOEGA V_RUMO_MILHO':   342,
            'MOEGA V_MRS_MILHO':    345,
            'MOEGA V_VLI_MILHO':    348,

            'MOEGA X_RUMO_FARELO':  362,
            'MOEGA X_MRS_FARELO':   365,
            'MOEGA X_VLI_FARELO':   368,
            'MOEGA X_RUMO_SOJA':    371,
            'MOEGA X_MRS_SOJA':     374,
            'MOEGA X_VLI_SOJA':     377,
            'MOEGA X_RUMO_MILHO':   380,
            'MOEGA X_MRS_MILHO':    383,
            'MOEGA X_VLI_MILHO':    386,

            'TGRAO_RUMO_FARELO':    400,
            'TGRAO_MRS_FARELO':     403,
            'TGRAO_VLI_FARELO':     406,
            'TGRAO_RUMO_SOJA':      409,
            'TGRAO_MRS_SOJA':       412,
            'TGRAO_VLI_SOJA':       415,
            'TGRAO_RUMO_MILHO':     418,
            'TGRAO_MRS_MILHO':      421,
            'TGRAO_VLI_MILHO':      424,

            'CLI_RUMO_FARELO':      438,
            'CLI_MRS_FARELO':       441,
            'CLI_VLI_FARELO':       444,
            'CLI_RUMO_SOJA':        447,
            'CLI_MRS_SOJA':         450,
            'CLI_VLI_SOJA':         453,
            'CLI_RUMO_MILHO':       456,
            'CLI_MRS_MILHO':        459,
            'CLI_VLI_MILHO':        462,

            'CLI ACUCAR_RUMO_ACUCAR':      476,
            'CLI ACUCAR_MRS_ACUCAR':       479,
            'CLI ACUCAR_VLI_ACUCAR':       482, #ESTE AQUI

            'TAC_RUMO_FARELO':   496,
            'TAC_MRS_FARELO':    499,
            'TAC_VLI_FARELO':    502,
            'TAC_RUMO_SOJA':     505,
            'TAC_MRS_SOJA':      508,
            'TAC_VLI_SOJA':      511,
            'TAC_RUMO_MILHO':    514,
            'TAC_MRS_MILHO':     517,
            'TAC_VLI_MILHO':     520,

            'TAC ACUCAR_RUMO_ACUCAR':   534,
            'TAC ACUCAR_MRS_ACUCAR':    537, #ESTE AQUI
            'TAC ACUCAR_VLI_ACUCAR':    540, #ESTE AQUI

            'T12A_RUMO_FARELO':         554,
            'T12A_MRS_FARELO':          557,
            'T12A_VLI_FARELO':          560,
            'T12A_RUMO_SOJA':           563,
            'T12A_MRS_SOJA':            566,
            'T12A_VLI_SOJA':            569,
            'T12A_RUMO_MILHO':          572,
            'T12A_MRS_MILHO':           575,
            'T12A_VLI_MILHO':           578,

            'SUZANO_RUMO_CELULOSE':   593,
            'SUZANO_MRS_CELULOSE':    597,

            'BRACELL_RUMO_CELULOSE':    610,
            'BRACELL_MRS_CELULOSE':     613,

            'DPW_RUMO_CELULOSE':        627,
            'DPW_MRS_CELULOSE':         633,
            'DPW_VLI_CELULOSE':         630,
        }

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
        HOME.cell(row = 8, column=5,  value=datetime.today() - timedelta(hours=4))

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
    

#############################################################################################################

class PlanilhaAntiga:

    def __init__(self):

        self.planilha        = load_workbook("previsao_trens/src/DICIONARIOS/planilha_antiga.xlsm", keep_vba=True)
        self.periodo_vigente = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv",    sep=";", index_col=0)
        
        self.periodo_vigente = self.periodo_vigente.drop(self.periodo_vigente.index[0]) 

    def atualizar_data(self):

        linha       = self.periodo_vigente[self.periodo_vigente["NM_DIA"] == "D"]
        data_arq    = linha["DATA_ARQ"].values[0]
        datetime_D  = datetime.strptime(data_arq, "%Y-%m-%d")
  
        ws_previsao = self.planilha["Previsão"]
        ws_previsao["X5"].value = datetime_D.replace(tzinfo=None)

    def inserir_previsao(self):

        produtos_substituir  = { "SOJA": "Soja", "ACUCAR": "Açúcar", "MILHO": "Milho", "FARELO": "Farelo", "CELULOSE": "Celulose" }
        terminais_substituir = { "CLI": "RUMO", "CLI ACUCAR": "RUMO", "COPERSUCAR": "TAC", "TAC ACUCAR": "TAC", "MOEGA X": "Moega X", "MOEGA V": "Moega V", "T39": "Moega IV", "TGRAO": "Tgrão", "TEAG ACUCAR": "TEAG" }
        segmento             = { "SOJA": "Grão", "FARELO": "Grão", "MILHO": "Grão", "ACUCAR": "Açúcar", "CELULOSE": "Industrial", "CONTEINER": "Industrial", "KCL": "Fertilizante", "UREIA": "Fertilizante", "OUTROS": "Fertilizante"}
        linhas               = { "D": 15, "D+1": 54, "D+2": 100, "D+3": 173, "D+4": 250 }
        

        ws_criarTrem = self.planilha["Criar_Trem"]

        for _, linha in self.periodo_vigente.iterrows():

            data = datetime.strptime(linha['DATA_ARQ'], '%Y-%m-%d')
            dia_logistico = linha['NM_DIA']

            queryset = Trem.objects.filter( previsao__year=data.year, previsao__month=data.month, previsao__day=data.day ).order_by('posicao_previsao')

            if queryset.exists():

                i = 0
                linha = linhas[dia_logistico]
                
                for trem in queryset:
                    
                    terminal = trem.terminal
                    if terminal in terminais_substituir: terminal = terminais_substituir[terminal]
                    
                    mercadoria = trem.mercadoria
                    if mercadoria in produtos_substituir: mercadoria = produtos_substituir[mercadoria]

                    ws_criarTrem.cell(row=linha + i, column=5,  value=trem.ferrovia)
                    ws_criarTrem.cell(row=linha + i, column=6,  value=trem.os)
                    ws_criarTrem.cell(row=linha + i, column=7,  value=trem.prefixo)
                    ws_criarTrem.cell(row=linha + i, column=8,  value=trem.origem)
                    ws_criarTrem.cell(row=linha + i, column=9,  value=trem.destino)
                    ws_criarTrem.cell(row=linha + i, column=10, value=trem.previsao.replace(tzinfo=None))

                    ws_criarTrem.cell(row=linha + i, column=13, value=terminal)     
                    ws_criarTrem.cell(row=linha + i, column=14, value=segmento[trem.mercadoria])    
                    ws_criarTrem.cell(row=linha + i, column=15, value=mercadoria)   
                    ws_criarTrem.cell(row=linha + i, column=16, value=trem.vagoes)
  
                    i = i + 1

    def inserir_produtividade(self):

        ws_navegacao = self.planilha['Navegação']
        colunas      = { "D": 51, "D+1": 86, "D+2": 121, "D+3": 156, "D+4": 191}
        linhas_pedra = { "TGG":  14, "TEG":  52, "TEAG": 90, "TEAG ACUCAR": 128, "CUTRALE": 148, "T39": 245, "TES": 283, "MOEGA V": 231,"MOEGA X": 350,"TGRAO":  397,"CLI": 345,"CLI ACUCAR":473,"TAC": 493, "TAC ACUCAR": 531,"T12A":551,"SUZANO": 590,"BRACELL": 607}

        df_descargas_ativas  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
        ls_terminais_ativos  = df_descargas_ativas.index[df_descargas_ativas['TERMINAL'] != 0].tolist()

        for terminal in ls_terminais_ativos:

            if terminal in linhas_pedra:

                descargas_terminal = df_descargas_ativas.loc[terminal]
                descargas_ativas_terminal = [indice for indice, valor in descargas_terminal.items() if valor > 0]
                descargas_ativas_terminal.remove("TERMINAL")

                for tipo_desc in descargas_ativas_terminal:

                    linha_planinha = tipo_desc_linhas[f'{terminal}_{tipo_desc}']

                    ws_navegacao.row_dimensions[linhas_pedra[terminal]].hidden = False

                    ws_navegacao.row_dimensions[linha_planinha - 2].hidden = False
                    ws_navegacao.row_dimensions[linha_planinha - 1].hidden = False
                    ws_navegacao.row_dimensions[linha_planinha].hidden     = False

                    ferrovia = tipo_desc.split("_")[0]
                    produto  = tipo_desc.split("_")[1]

                    for _, linha in self.periodo_vigente.iterrows():

                        data_arq        = linha['DATA_ARQ']
                        dia_logistico   = linha['NM_DIA']
                        
                        
                        with open(f"previsao_trens/src/DESCARGAS/{ terminal }/descarga_{ data_arq }.json") as json_descarga:
                            descarga = json.load(json_descarga)

                        if dia_logistico == "D":

                            saldo_virada = descarga["DESCARGAS"][ferrovia][produto]["INDICADORES"]["SALDO_DE_VIRADA"]
                            ws_navegacao.cell(row=(linha_planinha - 1), column=15, value=saldo_virada)
                        
                        linha_produtividade = descarga["DESCARGAS"][ferrovia][produto]["PRODUTIVIDADE"]

                        for i, produtividade in enumerate(linha_produtividade):

                            ws_navegacao.cell(row=linha_planinha, column=colunas[dia_logistico] + i, value=produtividade)       

    def inserir_restricao(self):

        ws_restricao = self.planilha['Restrição']      

        primeira_linha = 6

        restricoes = Restricao.objects.all()
   
        terminais_substituir = {'CLI': 'RUMO', 'COPERSUCAR': 'TAC', 'MOEGA X': 'Moega X', 'MOEGA V': 'Moega V','T39': 'Moega IV','TAC ACUCAR': 'TAC','CLI ACUCAR': 'RUMO','TEAG ACUCAR': 'TEAG',}
        segmentos_substituir = {'SOJA': 'Grão', 'FARELO': 'Grão', 'MILHO': 'Grão', 'ACUCAR': 'Açúcar','CELULOSE': 'Indústrial'}
        
        for i, restricao in enumerate(restricoes):       

            terminal = restricao.terminal
            if terminal in terminais_substituir: terminal = terminais_substituir[terminal]

            segmento = restricao.mercadoria
            if segmento in segmentos_substituir: segmento = segmentos_substituir[segmento]

            ws_restricao.cell(row=(primeira_linha + i), column=13, value=terminal)
            ws_restricao.cell(row=(primeira_linha + i), column=14, value=segmento)
            ws_restricao.cell(row=(primeira_linha + i), column=15, value=restricao.comeca_em.replace(tzinfo=None))
            ws_restricao.cell(row=(primeira_linha + i), column=16, value=restricao.termina_em.replace(tzinfo=None))
            ws_restricao.cell(row=(primeira_linha + i), column=17, value=restricao.motivo)       
            ws_restricao.cell(row=(primeira_linha + i), column=18, value=restricao.porcentagem)

def gerar_planilha_antiga():

    Planilha = PlanilhaAntiga()
    Planilha.atualizar_data()
    Planilha.inserir_previsao()
    Planilha.inserir_produtividade()
    Planilha.inserir_restricao()

    return Planilha.planilha