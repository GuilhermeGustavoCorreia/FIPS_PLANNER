from previsao_trens.models import Trem
from django.db.models import Q
import pandas as pd

def VALIDAR_DIVISAO_PREVISAO(ID_TREM, TREM_01, TREM_02):

    #VALIDAR
    #1. VALIDAR CONFLITO ENTRE AS DUAS NOVAS DIVISÕES
    #2. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)
    #3. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"

    VALIDACAO = {          
        "STATUS":       bool,
        "DESCRICAO":    str
    }
    #1.
    if ( (TREM_01["previsao"]   == TREM_02["previsao"]) and 
         (TREM_01["terminal"]   == TREM_02["terminal"]) and 
         (TREM_01["mercadoria"] == TREM_02["mercadoria"])):

        VALIDACAO["STATUS"] = False
        VALIDACAO["DESCRICAO"] = "As divisões não podem ser destinadas ao mesmo lugar com o mesmo produto."     

        return VALIDACAO

    #2.
    PERIODO_VIGENTE      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()

    DIVISOES = [TREM_01, TREM_02]

    for TREM in DIVISOES:

        TREM_DATA_ARQ   = TREM['previsao'].strftime('%Y-%m-%d')
        HORA            = TREM['previsao'].hour


        if not TREM_DATA_ARQ in LISTA_DATA_ARQ:
            VALIDACAO["STATUS"]    = False
            VALIDACAO["DESCRICAO"] = "O Trem só pode ser inserido dentro do período vigente (D-1 até D+4)." 

            return VALIDACAO
        
        POSICAO = LISTA_DATA_ARQ.index(TREM_DATA_ARQ)

        if POSICAO == 0 and HORA == 0:

            VALIDACAO["STATUS"]    = False
            VALIDACAO["DESCRICAO"] = "Não é possível inserir um trem neste horário específico." 
    
        EXISTE_TREM = Trem.objects.filter(
            ~Q(pk=ID_TREM),  # pk diferente de ID_TREM
            terminal=TREM["terminal"],
            previsao=TREM["previsao"]
        ).exists()

        #2.
        if EXISTE_TREM:
            
            FILTO = list(Trem.objects.filter(~Q(pk=ID_TREM), terminal=TREM["terminal"], previsao=TREM["previsao"]))[0]

            VALIDACAO["STATUS"]    = False
            VALIDACAO["DESCRICAO"] = f"O Trem { FILTO } esta já ocupando esta chegada."                    
        
            return VALIDACAO

    VALIDACAO = {     
        "STATUS":       True,
        "DESCRICAO":    "Trem validado"
    }

    return VALIDACAO

def VALIDAR_EDICAO_PREVISAO(TREM, ID_TREM):

    #VALIDAR
    #1. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)
    #2. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"


    VALIDACAO = {          
        "STATUS":       bool,
        "DESCRICAO":    str
    }

    VALIDACAO = {     
        "STATUS":       True,
        "DESCRICAO":    "Trem validado"
    }

    #1.
    PERIODO_VIGENTE      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()
    TREM_DATA_ARQ        = TREM['previsao'].strftime('%Y-%m-%d')
    HORA    = TREM['previsao'].hour

    if not TREM_DATA_ARQ in LISTA_DATA_ARQ:
        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = "O Trem só pode ser inserido dentro do período vigente (D-1 até D+4)." 

        return VALIDACAO
    
    POSICAO = LISTA_DATA_ARQ.index(TREM_DATA_ARQ)

    if POSICAO == 0 and HORA == 0:

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = "Não é possível inserir um trem neste horário específico." 
 
    EXISTE_TREM = Trem.objects.filter(
        ~Q(pk=ID_TREM),  # pk diferente de ID_TREM
        terminal=TREM["terminal"],
        previsao=TREM["previsao"]
    ).exists()
    
    #2.
    if EXISTE_TREM:
        
        FILTO = list(Trem.objects.filter(~Q(pk=ID_TREM), terminal=TREM["terminal"], previsao=TREM["previsao"]))[0]

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = f"O Trem { FILTO } esta já ocupando esta chegada."                    
    
    return VALIDACAO

def VALIDAR_NOVA_PREVISAO(TREM):

    #VALIDAR
    #1. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)
    #2. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL (É O MESMO TREM? => FAZER EDICAO)

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"


    VALIDACAO = {          
        "STATUS":       bool,
        "DESCRICAO":    str
    }

    VALIDACAO = {     
        "STATUS":       True,
        "DESCRICAO":    "Trem validado"
    }

    #1.
    PERIODO_VIGENTE      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()
    TREM_DATA_ARQ        = TREM['previsao'].strftime('%Y-%m-%d')
    HORA    = TREM['previsao'].hour

    if not TREM_DATA_ARQ in LISTA_DATA_ARQ:
        
        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = "O Trem só pode ser inserido dentro do período vigente (D-1 até D+4)." 

        return VALIDACAO
    
    POSICAO = LISTA_DATA_ARQ.index(TREM_DATA_ARQ)

    if POSICAO == 0 and HORA == 0:

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = "Não é possível inserir um trem neste horário específico." 
 
    EXISTE_TREM = Trem.objects.filter(terminal=TREM["terminal"], previsao=TREM["previsao"]).exists()
    
    #2.
    if EXISTE_TREM:
        
        FILTO = list(Trem.objects.filter(terminal=TREM["terminal"], previsao=TREM["previsao"]))[0]

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = f"O Trem { FILTO } esta já ocupando esta chegada."                    
    
    return VALIDACAO