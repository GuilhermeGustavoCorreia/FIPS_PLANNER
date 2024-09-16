import json
import pandas as pd
from datetime import datetime, timedelta
import os
from django.conf import settings
from    previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as NAVEGACAO_DESCARGA
from django.db.models import Q
from previsao_trens.packages.PROG_SUBIDA import CALCULAR_SUBIDA

from previsao_trens.models        import Restricao

def ATUALIZAR_DESCARGA():

    PATH_PERIODO_VIGENTE        = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    PATH_MODELO_DESCARGA        = "previsao_trens/src/DICIONARIOS/MODELO_DESCARGA.json"
    DIRETORIO_DESCARGAS         = "previsao_trens/src/DESCARGAS"

    #TERMINAIS DESCARGA
    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        dict_TERMINAIS = json.load(ARQUIVO_DESCARGA)

    #ATUALIZAR PERIODO VIGENTE
    PERIODO_VIGENTE     = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    ULTIMO_DIA_ANTIGO   = datetime.strptime(PERIODO_VIGENTE.iloc[-1]["DATA_ARQ"], "%Y-%m-%d")   #OBTENDO O ANTIGO D+4

    PERIODO_VIGENTE['DATA_ARQ'] = PERIODO_VIGENTE['DIA_LOGISTICO'].apply(lambda x: (datetime.now() + timedelta(days=x)).strftime("%Y-%m-%d"))
    ULTIMO_DIA_NOVO             = datetime.strptime(PERIODO_VIGENTE.iloc[-1]["DATA_ARQ"], "%Y-%m-%d")     #OBTENDO O NOVO D+4
    PERIODO_VIGENTE.to_csv(PATH_PERIODO_VIGENTE, sep=";")
    
    LISTA_DATA_ARQ       = PERIODO_VIGENTE['DATA_ARQ'].tolist()
    ARQUIVOS_ATUALIZADOS = [f'descarga_{data}.json' for data in LISTA_DATA_ARQ]
    #ATUALIZANDO AS DESCARGAS

    #VAMOS COPIAR O MODELO DE DESCARGA
    with open(PATH_MODELO_DESCARGA) as ARQUIVO_DESCARGA:
        MODELO_DESCARGA = json.load(ARQUIVO_DESCARGA)

    #REMOVER A DESCARGA

    UMA_DESCARGA = MODELO_DESCARGA["DESCARGAS"]["FERROVIA"]["PRODUTO"]
    del MODELO_DESCARGA["DESCARGAS"]["FERROVIA"]

    #region ATUALIZANDO DESCARGAS [rgb(101,170,177, 0.3)]
    
    for TERMINAL in dict_TERMINAIS:
        
        # CRIANDO MODELO DE DESCARGA CONFORME CADA TERMINAL {#bcbcbc, 9
        DESCARGA_TERMINAL = {}
        DESCARGA_TERMINAL = MODELO_DESCARGA

        for FERROVIA in dict_TERMINAIS[TERMINAL]["FERROVIA"]:
            DESCARGA_TERMINAL["DESCARGAS"][FERROVIA] = {}

            for PRODUTO in dict_TERMINAIS[TERMINAL]["PRODUTOS"]:                          
                DESCARGA_TERMINAL["DESCARGAS"][FERROVIA][PRODUTO] = UMA_DESCARGA


        #region CRIANDO PASTA DO TERMINAL [rgb(255,77,197, 0.2)]
        DIRETORIO_TERMINAL = os.path.join(DIRETORIO_DESCARGAS, TERMINAL)           
        if not os.path.exists(DIRETORIO_TERMINAL):
            os.mkdir(DIRETORIO_TERMINAL)

        #endregion
        
        DESCARGAS_NA_PASTA_DO_TEMRINAL = (os.listdir(DIRETORIO_TERMINAL))
        
        #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in DESCARGAS_NA_PASTA_DO_TEMRINAL:
            if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   

                ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_TERMINAL, ARQUIVO)
                os.remove(ARQUIVO_EXCEDENTE)  
        #endregion
        
        #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in ARQUIVOS_ATUALIZADOS:
            if ARQUIVO not in DESCARGAS_NA_PASTA_DO_TEMRINAL:

                DESCARGA_TERMINAL["TERMINAL"] = TERMINAL
                DESCARGA_TERMINAL["DATA"]     = ARQUIVO.split("_")[1].split(".")[0]
            
                with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
                    json.dump(DESCARGA_TERMINAL, ARQUIVO_NOME, indent=4)
        
        #endregion              
       
    #region ATUALIZANDO RESTRIÇÕES [rgb(255,77,197, 0.3)]
    restricoes = Restricao.objects.filter(Q(aplicacao_status="PARCIALMENTE_INSERIDA") | Q(aplicacao_status="NAO_INSERIDA"))

    for restricao in restricoes:   

        restricao.delete()
        restricao.save()

    #endregion

    #endregion

    #SUBIDA 
       
    DIRETORIO_SUBIDA                = "previsao_trens/src/SUBIDA"
    PARAMETROS_TERMINAIS_ESPECIAIS  = "PARAMETROS/TERMINAIS_ESPECIAIS.json"

    with open(os.path.join(DIRETORIO_SUBIDA, PARAMETROS_TERMINAIS_ESPECIAIS)) as ARQUIVO_DESCARGA: 
        TERMINAIS_ESPECIAIS = json.load(ARQUIVO_DESCARGA)

    #region ATUALIZANDO TERMINAIS ESPECIAIS [rgb(101,170,177, 0.3)] 
    for TERMINAL, CONTEUDO in TERMINAIS_ESPECIAIS["JUNTAR"].items():
            
        #region CRIANDO MODELO DE DESCARGA CONFORME CADA TERMINAL [rgb(255,77,197, 0.2)]
        DESCARGA_TERMINAL = {}
        DESCARGA_TERMINAL = MODELO_DESCARGA

        for FERROVIA in CONTEUDO["SAIDA"]["FERROVIA"]:
            DESCARGA_TERMINAL["DESCARGAS"][FERROVIA] = {}

            for PRODUTO in CONTEUDO["SAIDA"]["PRODUTOS"]:
                DESCARGA_TERMINAL["DESCARGAS"][FERROVIA][PRODUTO] = UMA_DESCARGA
        #endregion

        #region CRIANDO PASTA DO TERMINAL [rgb(255,77,197, 0.2)]
        DIRETORIO_TERMINAL = os.path.join(DIRETORIO_SUBIDA, F"TERMINAIS_ADAPTADOS/{ TERMINAL }")           
        if not os.path.exists(DIRETORIO_TERMINAL):
            os.mkdir(DIRETORIO_TERMINAL)
        #endregion
        
        DESCARGAS_NA_PASTA_DO_TEMRINAL = (os.listdir(DIRETORIO_TERMINAL))
        
        #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in DESCARGAS_NA_PASTA_DO_TEMRINAL:
            if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   
                
                ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_TERMINAL, ARQUIVO)
                os.remove(ARQUIVO_EXCEDENTE) 
        #endregion
        
        #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in ARQUIVOS_ATUALIZADOS:
            if ARQUIVO not in DESCARGAS_NA_PASTA_DO_TEMRINAL:

                DESCARGA_TERMINAL["TERMINAL"] = TERMINAL
                DESCARGA_TERMINAL["DATA"]     = ARQUIVO.split("_")[1].split(".")[0]

                with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
                    json.dump(DESCARGA_TERMINAL, ARQUIVO_NOME, indent=4)
        #endregion

    #endregion

    TERMINAIS_DESCONDIDERADOS = TERMINAIS_ESPECIAIS["REMOVER"]
    TERMINAIS_ESPECIAIS_NOVOS = os.listdir(os.path.join(DIRETORIO_SUBIDA, "TERMINAIS_ADAPTADOS")) 

    DIRETORIO_SUBIDA                = "previsao_trens/src/SUBIDA"
    PARAMETROS_TERMINAIS_ESPECIAIS  = "PARAMETROS/TERMINAIS_ESPECIAIS.json" 
    
    with open(os.path.join(DIRETORIO_SUBIDA, "DICIONARIOS/MODELO_SUBIDA.json")) as ARQUIVO_SUBIDA: 
        MODELO_TERMINAL_SUBIDA = json.load(ARQUIVO_SUBIDA)
    
    UMA_SUBIDA = MODELO_TERMINAL_SUBIDA["SUBIDA"]["FERROVIA"]["PRODUTO"]
    del MODELO_TERMINAL_SUBIDA["SUBIDA"]["FERROVIA"]

    TERMINAIS_SUBIDA = [item for item in dict_TERMINAIS.keys() if item not in TERMINAIS_DESCONDIDERADOS]

    TERMINAIS_SUBIDA.extend(TERMINAIS_ESPECIAIS_NOVOS)

    ARQUIVOS_ATUALIZADOS = [f'subida_{data}.json' for data in LISTA_DATA_ARQ]
    
    #region ATUALIZANDO SUBIDA DE TERMINAIS [rgb(101,170,177, 0.3)] 
    for TERMINAL in TERMINAIS_SUBIDA:

        try:    
            
            SEGMENTO  = dict_TERMINAIS[TERMINAL]["SEGMENTO"]
            FERROVIAS = dict_TERMINAIS[TERMINAL]["FERROVIA"]
            PATIO     = dict_TERMINAIS[TERMINAL]["PATIO"]
        
        except KeyError:
            
            SEGMENTO  = TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["SEGMENTO"]
            FERROVIAS = TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["FERROVIA"]
            PATIO     = TERMINAIS_ESPECIAIS["JUNTAR"][TERMINAL]["SAIDA"]["PATIO"]
            
        SUBIDA_TERMINAL = {}
        SUBIDA_TERMINAL = MODELO_TERMINAL_SUBIDA

        #region CRIANDO MODELO DE DESCARGA CONFORME CADA TERMINAL [rgb(255,77,197, 0.2)]
        for FERROVIA in FERROVIAS:
            
            SUBIDA_TERMINAL["SUBIDA"][FERROVIA] = {}
            SUBIDA_TERMINAL["SUBIDA"][FERROVIA][SEGMENTO] = UMA_SUBIDA
            
        #endregion
        
        #region CRIANDO PASTA DO TERMINAL [rgb(255,77,197, 0.2)]
        DIRETORIO_TERMINAL = os.path.join(DIRETORIO_SUBIDA, f"TERMINAIS_SUBIDA/{ TERMINAL }")           
        if not os.path.exists(DIRETORIO_TERMINAL):
            os.mkdir(DIRETORIO_TERMINAL)
        #endregion

        ARQUIVOS_NA_PASTA_DO_TEMRINAL = (os.listdir(DIRETORIO_TERMINAL))

        #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in ARQUIVOS_NA_PASTA_DO_TEMRINAL:
            if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   
                
                ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_TERMINAL, ARQUIVO)
                os.remove(ARQUIVO_EXCEDENTE) 
        #endregion
        
        #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
        for ARQUIVO in ARQUIVOS_ATUALIZADOS:
            if ARQUIVO not in ARQUIVOS_NA_PASTA_DO_TEMRINAL:

                SUBIDA_TERMINAL["TERMINAL"] = TERMINAL
                SUBIDA_TERMINAL["SEGMENTO"] = SEGMENTO
                SUBIDA_TERMINAL["PATIO"]    = PATIO
                SUBIDA_TERMINAL["DATA"]     = ARQUIVO.split("_")[1].split(".")[0]

                with open(os.path.join(DIRETORIO_TERMINAL, ARQUIVO), 'w') as ARQUIVO_NOME:
                    json.dump(SUBIDA_TERMINAL, ARQUIVO_NOME, indent=4)
        #endregion
 
 #endregion

    #region ATUALIZANDO CONDENSADOS DE SUBIDA [rgb(101,170,177, 0.3)]
    
    DIRETORIO_CONDENSADOS  = os.path.join(DIRETORIO_SUBIDA, "CONDENSADOS")
    PATH_MODELO_CONDENSADO = os.path.join(DIRETORIO_SUBIDA, "DICIONARIOS/MODELO_CONDENSADO.json")
    ARQUIVOS_ATUALIZADOS   = [f'condensado_{data}.json' for data in LISTA_DATA_ARQ] 
    
    with open(PATH_MODELO_CONDENSADO) as ARQUIVO_DESCARGA:
        MODELO_CONDENSADO = json.load(ARQUIVO_DESCARGA)
    
    ARQUIVOS_NA_PASTA_DOS_CONDENSADOS = (os.listdir(DIRETORIO_CONDENSADOS))
    
    #region CRIANDO MODELO DA LINHA 4K [rgb(255,77,197, 0.1)]
    # for FERROVIA in FERROVIAS:
        
    #     SUBIDA_TERMINAL["SUBIDA"][FERROVIA] = {}
    #     SUBIDA_TERMINAL["SUBIDA"][FERROVIA][SEGMENTO] = UMA_SUBIDA
            
    #endregion

    #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_NA_PASTA_DOS_CONDENSADOS:
        if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   

            ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_CONDENSADOS, ARQUIVO)
            os.remove(ARQUIVO_EXCEDENTE) 
    #endregion


    #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_ATUALIZADOS:

        if ARQUIVO not in ARQUIVOS_NA_PASTA_DOS_CONDENSADOS:

            with open(os.path.join(DIRETORIO_CONDENSADOS, ARQUIVO), 'w') as ARQUIVO_NOME:
                json.dump(MODELO_CONDENSADO, ARQUIVO_NOME, indent=4)
    #endregion
    
    #endregion

    #region ATUALIZANDO LINHA 4K [rgb(101,170,177, 0.3)]

    DIRETORIO_LINHA_4K   = os.path.join(DIRETORIO_SUBIDA, "LINHAS/LINHA_4K")
    PATH_MODELO_LINHA_4K = os.path.join(DIRETORIO_SUBIDA, "DICIONARIOS/MODELO_LINHA_4K.json")
    ARQUIVOS_ATUALIZADOS = [f'linha_4k_{data}.json' for data in LISTA_DATA_ARQ] 

    with open(PATH_MODELO_LINHA_4K) as ARQUIVO_LINHA_4K:
            MODELO_LINHA_4K = json.load(ARQUIVO_LINHA_4K)

    with open(os.path.join(DIRETORIO_SUBIDA, "PARAMETROS/LINHAS.json")) as ARQUIVO_LINHA_4K: 
        jsLINHAS= json.load(ARQUIVO_LINHA_4K)

    UMA_SUBIDA = MODELO_LINHA_4K["SUBIDA"]["FERROVIA"]["PRODUTO"]
    del MODELO_LINHA_4K["SUBIDA"]["FERROVIA"]

    ARQUIVOS_NA_PASTA_DA_LINHA_4K = (os.listdir(DIRETORIO_LINHA_4K))

    #region CRIANDO MODELO DA LINHA 4K [rgb(255,77,197, 0.2)]

    SUBIDA_LINHA = {}
    SUBIDA_LINHA = MODELO_LINHA_4K

    for FERROVIA in jsLINHAS["LINHA_4K"]["FERROVIAS"]:
        SUBIDA_LINHA["SUBIDA"][FERROVIA] = {}

        for PRODUTO in jsLINHAS["LINHA_4K"]["SEGMENTOS"]:                          
            SUBIDA_LINHA["SUBIDA"][FERROVIA][PRODUTO] = UMA_SUBIDA
            
        #endregion

    #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_NA_PASTA_DA_LINHA_4K:
        if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   

            ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_LINHA_4K, ARQUIVO)
            os.remove(ARQUIVO_EXCEDENTE) 
    #endregion


    #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_ATUALIZADOS:

        if ARQUIVO not in ARQUIVOS_NA_PASTA_DA_LINHA_4K:

            with open(os.path.join(DIRETORIO_LINHA_4K, ARQUIVO), 'w') as ARQUIVO_NOME:
                json.dump(SUBIDA_LINHA, ARQUIVO_NOME, indent=4)
    #endregion
    
#endregion

    #region ATUALIZANDO BUFFER´S

    with open(os.path.join(DIRETORIO_SUBIDA, "DICIONARIOS/MODELO_BUFFER.json")) as ARQUIVO: 
        MODELO_BUFFER = json.load(ARQUIVO)

    DIRETORIO_BUFFER        = os.path.join(DIRETORIO_SUBIDA, "BUFFER")
    ARQUIVOS_ATUALIZADOS    = [f'buffer_{ data }.json' for data in LISTA_DATA_ARQ]
    ARQUIVOS_NO_DIRETORIO   = (os.listdir(DIRETORIO_BUFFER))

    #region EXCLUINDO ANTIGOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_NO_DIRETORIO:
        if ARQUIVO not in ARQUIVOS_ATUALIZADOS:   

            ARQUIVO_EXCEDENTE = os.path.join(DIRETORIO_BUFFER, ARQUIVO)
            os.remove(ARQUIVO_EXCEDENTE) 
    #endregion

    #region CRIANDO NOVOS [rgb(255,77,197, 0.2)]
    for ARQUIVO in ARQUIVOS_ATUALIZADOS:
        if ARQUIVO not in ARQUIVOS_NO_DIRETORIO:

            with open(os.path.join(DIRETORIO_BUFFER, ARQUIVO), 'w') as ARQUIVO_NOME:
                json.dump(MODELO_BUFFER, ARQUIVO_NOME, indent=4)
    #endregion

    #endregion