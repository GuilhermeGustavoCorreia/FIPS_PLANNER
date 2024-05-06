import pandas as pd

def VALIDAR_RESTRICAO(RESTRICAO):

    #VALIDAR SE O INICIO É EM D-1 EM DIANTE
    #VALIDAR SE NÃO EXISTE OUTRA RESTRIÇÃO COM PARAMETROS DE CONFLITO

    VALIDACAO = {          
        "STATUS":       bool,
        "DESCRICAO":    str
    }

    VALIDACAO = {          
        "STATUS":       True,
        "DESCRICAO":    "Ok."
    }


    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"

    PERIODO_VIGENTE      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()
    print(RESTRICAO["comeca_em"], type(RESTRICAO["comeca_em"]))
    RESTRICAO_DATA_ARQ = RESTRICAO["comeca_em"].strftime('%Y-%m-%d')


    if not RESTRICAO_DATA_ARQ in LISTA_DATA_ARQ:

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = "A Restrição só pode ser iniciada dentro do período vigente (D-1 até D+4)." 

    
    return VALIDACAO
    