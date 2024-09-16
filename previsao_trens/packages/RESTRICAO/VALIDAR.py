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

    
    return VALIDACAO