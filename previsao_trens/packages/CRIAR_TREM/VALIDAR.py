from previsao_trens.models import Trem
from django.db.models import F
import pandas as pd



def VALIDAR_NOVA_PREVISAO(TREM):

    #VALIDAR
    #1. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)
    #2. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL (É O MESMO TREM? => FAZER EDICAO)


    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"


    VALIDACAO = {
            
            "STATUS":       bool,
            "ACAO":         str,
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
        VALIDACAO["DESCRICAO"] = f"O Trem só pode ser inserido dentro do período vigente (D-1 até D+4)." 

        return VALIDACAO
    
    POSICAO = LISTA_DATA_ARQ.index(TREM_DATA_ARQ)

    if POSICAO == 0 and HORA == 0:

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = f"Não é possível inserir um trem neste horário específico." 
 
    EXISTE_TREM = Trem.objects.filter(terminal=TREM["terminal"], previsao=TREM["previsao"]).exists()
    
    #2.
    if EXISTE_TREM:
        
        FILTO = list(Trem.objects.filter(terminal=TREM["terminal"], previsao=TREM["previsao"]))[0]

        VALIDACAO["STATUS"]    = False
        VALIDACAO["DESCRICAO"] = f"O Trem { FILTO } esta já ocupando esta chegada."                    
    
    return VALIDACAO