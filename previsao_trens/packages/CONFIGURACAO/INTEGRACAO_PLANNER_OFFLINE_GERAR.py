import  os
import  json
import  pandas              as pd
from    django.conf         import settings
from    datetime            import datetime
from previsao_trens.models  import Trem, Restricao


def formatar_restricao(restricao):
    
    return {
        'TERMINAL'      : restricao.terminal,
        'SEGMENTO'      : restricao.mercadoria,
        'INICIO'        : restricao.comeca_em.strftime('%Y-%m-%d %H:%M:%S'),
        'FINAL'         : restricao.termina_em.strftime('%Y-%m-%d %H:%M:%S'),
        'PCT'           : restricao.porcentagem,
        'MOTIVO'        : restricao.motivo,
        'COMENTARIO'    : restricao.comentario
    }

def BAIXAR_DADOS():


    PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
    PERIODO_VIGENTE = PERIODO_VIGENTE.drop(PERIODO_VIGENTE.index[0])
    LISTA_DATA_ARQ  = PERIODO_VIGENTE["DATA_ARQ"].tolist()
    
    TERMINAIS_ATIVOS        = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    lst_TERMINAIS_ATIVOS    = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)

    JSON = {
        "HEADER"     : {},
        "RESTRICOES" : [], 
        "PREVISOES"  : {"D": [],"D+1": [],"D+2": [],"D+3": [],"D+4": [], "SEM_PREVISAO": []},
        "DESCARGAS"	 : {"D": {},"D+1": {},"D+2": {},"D+3": {},"D+4": {}}
    }

    with open("previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        DICT_TERMINAIS = json.load(ARQUIVO_DESCARGA)

    #region INSERINDO AS DESCARGAS
    for TERMINAL in lst_TERMINAIS_ATIVOS:

        DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
        DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]

        FERROVIAS_ATIVAS = {
            "RUMO": [],
            "MRS" : [],
            "VLI" : []
        }

        for ATIVO in DESCARGAS_ATIVAS:

            for FERROVIA in FERROVIAS_ATIVAS:
                if ATIVO[0] == FERROVIA: FERROVIAS_ATIVAS[FERROVIA].append(ATIVO[1]) 

        for DATA_ARQ in LISTA_DATA_ARQ:
            
            with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO_DESCARGA:
                DESCARGA = json.load(ARQUIVO_DESCARGA)


            for FERROVIA in FERROVIAS_ATIVAS:
                DESCARGA["DESCARGAS"][FERROVIA] = {chave: valor for chave, valor in DESCARGA["DESCARGAS"][FERROVIA].items() if chave in FERROVIAS_ATIVAS[FERROVIA]}

            PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
            LINHA           = PERIODO_VIGENTE[PERIODO_VIGENTE['DATA_ARQ'] == DATA_ARQ]
            DIA_LOGISTICO   = LINHA['NM_DIA'].values[0]

            JSON["DESCARGAS"][DIA_LOGISTICO][TERMINAL] = f"""{ DESCARGA }"""

    #endregion

    #region INSERINDO AS PREVISOES (nao existem trem sem previsoes)

    for _, LINHA in PERIODO_VIGENTE.iterrows():

        DATA = datetime.strptime(LINHA['DATA_ARQ'], '%Y-%m-%d')

        queryset = Trem.objects.filter(
            previsao__year  = DATA.year,
            previsao__month = DATA.month,
            previsao__day   = DATA.day
        ).order_by('posicao_previsao')
        if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
    
            JSON["PREVISOES"][LINHA['NM_DIA']] = [
                {
                    'PREFIXO'           : trem.prefixo,
                    'OS'                : trem.os,
                    'VAGOES'            : trem.vagoes,
                    'MERCADORIA'        : trem.mercadoria,
                    'ORIGEM'            : trem.origem,
                    'SB_ATUAL'          : '--',  # Este valor deve ser ajustado conforme necessário
                    'DESTINO'           : trem.destino,
                    'TERMINAL_DESTINO'  : trem.terminal,
                    'PREVISAO'          : trem.previsao.strftime('%Y-%m-%d %H:%M:%S'),
                    'PREVISAO_DATA'     : trem.previsao.strftime('%d/%m/%Y'),
                    'PREVISAO_HORA'     : trem.previsao.strftime('%H:%M')
                }
                for trem in queryset
            ]
    #endregion

    #region INSERINDO AS RESTRICOES (nao existem trem sem previsoes)
    
    JSON["RESTRICOES"] = [formatar_restricao(restricao) for restricao in Restricao.objects.all()]
    

    #endregion

    caminho_static  = os.path.join(settings.STATIC_ROOT, 'downloads')
    caminho_arquivo = os.path.join(caminho_static, "DADOS.json")
    
    print(caminho_static)
    
    with open(caminho_arquivo, 'w') as ARQUIVO_NOME:
        json.dump(JSON, ARQUIVO_NOME, indent=4)


    return caminho_arquivo  