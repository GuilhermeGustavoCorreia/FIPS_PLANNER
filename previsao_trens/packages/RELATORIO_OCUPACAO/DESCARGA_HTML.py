import json
import pandas as pd





def MONTAR_HTML(DESCARGA, TERMINAL, DIA_LOGISTICO, DATA_ARQ, INFOS):

    HEADER = f"""<table class="tabela__descarga" id="{ TERMINAL }_{ DATA_ARQ }">  
                    <tbody>

                        <tr class="LINHA_TITULOS">

                            <td rowspan="5" colspan="2" class="NOME_TERMINAL">{ TERMINAL }</td>
                            <td rowspan="2" class="DIA_TERMINAL">{ DIA_LOGISTICO }</td>

                            <td colspan="6" class="PERIODO_TERMINAL">01h - 07h</td>
                            <td colspan="6" class="PERIODO_TERMINAL">07h - 13h</td>
                            <td colspan="6" class="PERIODO_TERMINAL">13h - 19h</td>
                            <td colspan="6" class="PERIODO_TERMINAL">19h - 01h</td>

                            <td rowspan="3" colspan="2" class="TITLO_TOTAIS">TOTAIS</td>

                        </tr>

                        <tr class="LINHA_HORAS">  

                            <td>01h</td>
                            <td>02h</td>
                            <td>03h</td>  
                            <td>04h</td>
                            <td>05h</td>
                            <td>06h</td>
                            <td>07h</td>
                            <td>08h</td>
                            <td>09h</td>  
                            <td>10h</td>
                            <td>11h</td>
                            <td>12h</td>
                            <td>13h</td>
                            <td>14h</td>
                            <td>15h</td>
                            <td>16h</td>  
                            <td>17h</td>
                            <td>18h</td>
                            <td>19h</td>
                            <td>20h</td> 
                            <td>21h</td>
                            <td>22h</td>
                            <td>23h</td>
                            <td>24h</td>  

                        </tr>  
                        """
    
    #region LINHA SALDO (PREFIXO)
    LINHA_SALDO = """<tr class="LINHA_SALDO">
                        <td>Saldo</td>"""

    for PREFIXO in DESCARGA["PREFIXO"]:

        if PREFIXO[0] != 0 : LINHA_SALDO += f"<td>{ PREFIXO[0] }</td>"
        else            : LINHA_SALDO += "<td></td>"           
    
    LINHA_SALDO += "</tr>" 
    #endregion

    #region LINHA CHEGADA (VAGOES) 
    LINHA_CHEGADA = """<tr class="LINHA_SALDO">
                        <td>Chegada</td>"""

    for CHEGADA in DESCARGA["CHEGADA"]:

        if CHEGADA[0] != 0  : LINHA_CHEGADA += f"<td>{ CHEGADA[0] }</td>"
        else                : LINHA_CHEGADA += "<td></td>"           
    
    LINHA_CHEGADA += "<td>Ofrt.</td><td>Pdra</td></tr>" 
    #endregion

    #region LINHA PEDRA
    LINHA_PEDRA = """<tr class="LINHA_PEDRA">
                        <td>Pedra</td>"""
    print()
    print(f"CHEGADA: {DESCARGA["CHEGADA"]}")
    print(f"PEDRA: {DESCARGA["PEDRA"]}")

    for PEDRA in DESCARGA["PEDRA"]:
        print(f"chg { CHEGADA } pdr { PEDRA } ")
        if CHEGADA[0] != 0  : 
            try: 
                LINHA_PEDRA +=  f"<td>{ PEDRA[0] }</td>" 
            except: 
                LINHA_PEDRA +=  "<td></td>"  
        else                : LINHA_PEDRA += "<td></td>"           
    
    LINHA_PEDRA += f"<td>{ DESCARGA["INDICADORES"]["TOTAL_SALDO"] }</td><td>{ DESCARGA["INDICADORES"]["TOTAL_PEDRA"] }</td></tr>" 
    #endregion

    DESCARGAS = ""

    for FERROVIA, CONTEUDO_FERROVIA in DESCARGA["DESCARGAS"].items():
        for PRODUTO, CONTEUDO_PRODUTO in CONTEUDO_FERROVIA.items():
            

            #region LINHA ENCOSTE
            DESCARGAS += f"""<tr class="LINHA_ENCOSTE">
                                    <td class="FERROVIA_{ FERROVIA }" rowspan=3>{ FERROVIA }</td>
                                    <td rowspan=2 class="PRODUTO">{ PRODUTO }</td>
                                    <td >Saldo</td>"""

            for ENCOSTE in CONTEUDO_PRODUTO["ENCOSTE"]:
                if ENCOSTE[0] == 0: ENCOSTE[0] = ""
                
                DESCARGAS += f""" <td style="font-weight: bold;">{ ENCOSTE[0] }</td>"""

                                   
            DESCARGAS += f"""<td colspan="2" class="TITULO_CHEGADA_{ FERROVIA }">Chegada</td>
            </tr>"""
            #endregion

            #region LINHA SALDO
            DESCARGAS += f"""<tr class="LINHA_SALDO_DESCARGA">
                                    <td data-ferrovia="{ FERROVIA }" data-produto="{ PRODUTO }" headers="SALDO_VIRADA" name="SALDO_DE_VIRADA_D">{ CONTEUDO_PRODUTO["INDICADORES"]["SALDO_DE_VIRADA"] }</td>"""

            for SALDO in CONTEUDO_PRODUTO["SALDO"]:
                if SALDO == 0: SALDO = ""
                
                DESCARGAS += f""" <td>{ SALDO }</td>"""

                                   
            DESCARGAS += f"""<td colspan="2" class="VALOR_ENCOSTE_{ FERROVIA }">{ CONTEUDO_PRODUTO["INDICADORES"]["TOTAL_CHEGADA"] }</td>
            </tr>"""
            #endregion

            #region LINHA PRODUTIVIDADE

            DESCARGAS +=    f"""<tr name="LINHA_PRODUTIVIDADE" class="LINHA_PRODUTIVIDADE_{ FERROVIA }">  
                                    <td class="PRODUTIVIDADE_PADRAO_{ FERROVIA }" data-ferrovia="{ FERROVIA }" data-produto="{ PRODUTO }" name="EDITAR_CONSTANTE_PRODUTIVIDADE">{ INFOS[TERMINAL]["PRODUTIVIDADE"][FERROVIA][PRODUTO] }</td>
                                    <td id="{ PRODUTO }_{ FERROVIA }"></td>"""


            for PRODUTIVIDADE in CONTEUDO_PRODUTO["PRODUTIVIDADE"]:
                if PRODUTIVIDADE == 0: PRODUTIVIDADE = ""
                
                DESCARGAS += f""" <td class="PRODUTIVIDADE_{ FERROVIA }"  >{ PRODUTIVIDADE }</td>"""


            DESCARGAS += f"""<td><div class="SETA_PRODUTIVIDADE_{ FERROVIA }">➔</div></td><td class="VALOR_PRODUTIVIDADE_{ FERROVIA}">{ CONTEUDO_PRODUTO["INDICADORES"]["TOTAL_PRODUTIVIDADE"] }</td>       
                                </tr>"""

            #endregion


    #region LINHA TOTAIS DE PEDRAS 
    LINHA_TOTAIS_PEDRA = \
    f"""<tr class="LINHAS_TOTAIS_PEDRAS">

        <td colspan="5"></td>
        <td class="TOTAL_FERROVIA_RUMO" data-periodo="1">   { DESCARGA["INDICADORES"]["PEDRAS"]["RUMO"]["P1"]  }</td>
        <td class="TOTAL_FERROVIA_MRS"  data-periodo="1">   { DESCARGA["INDICADORES"]["PEDRAS"]["MRS"]["P1"]   }</td>
        <td class="TOTAL_FERROVIA_VLI"  data-periodo="1">   { DESCARGA["INDICADORES"]["PEDRAS"]["VLI"]["P1"]   }</td>
        <td class="TITLO_TOTAIS"        data-periodo="1">   { DESCARGA["INDICADORES"]["PEDRAS"]["TOTAL"]["P1"] }</td>

        <td  colspan="2"></td>
        <td class="TOTAL_FERROVIA_RUMO" data-periodo="2">   { DESCARGA["INDICADORES"]["PEDRAS"]["RUMO"]["P2"]  }</td>
        <td class="TOTAL_FERROVIA_MRS"  data-periodo="2">   { DESCARGA["INDICADORES"]["PEDRAS"]["MRS"]["P2"]   }</td>
        <td class="TOTAL_FERROVIA_VLI"  data-periodo="2">   { DESCARGA["INDICADORES"]["PEDRAS"]["VLI"]["P2"]   }</td>
        <td class="TITLO_TOTAIS"        data-periodo="2">   { DESCARGA["INDICADORES"]["PEDRAS"]["TOTAL"]["P2"] }</td>

        <td  colspan="2"></td>
        <td class="TOTAL_FERROVIA_RUMO" data-periodo="3">   { DESCARGA["INDICADORES"]["PEDRAS"]["RUMO"]["P3"]  }</td>
        <td class="TOTAL_FERROVIA_MRS"  data-periodo="3">   { DESCARGA["INDICADORES"]["PEDRAS"]["MRS"]["P3"]   }</td>
        <td class="TOTAL_FERROVIA_VLI"  data-periodo="3">   { DESCARGA["INDICADORES"]["PEDRAS"]["VLI"]["P3"]   }</td>
        <td class="TITLO_TOTAIS"        data-periodo="3">   { DESCARGA["INDICADORES"]["PEDRAS"]["TOTAL"]["P3"] }</td>

        <td  colspan="2"></td>
        <td class="TOTAL_FERROVIA_RUMO" data-periodo="4">   { DESCARGA["INDICADORES"]["PEDRAS"]["RUMO"]["P4"]  }</td>
        <td class="TOTAL_FERROVIA_MRS"  data-periodo="4">   { DESCARGA["INDICADORES"]["PEDRAS"]["MRS"]["P4"]   }</td>
        <td class="TOTAL_FERROVIA_VLI"  data-periodo="4">   { DESCARGA["INDICADORES"]["PEDRAS"]["VLI"]["P4"]   }</td>
        <td class="TITLO_TOTAIS"        data-periodo="4">   { DESCARGA["INDICADORES"]["PEDRAS"]["TOTAL"]["P4"] }</td>

        </tr>"""

    #endregion

    #region LINHA RESTRICAO
    LINHA_RESTRICAO = ""

    if "RESTRICAO_PCT" in DESCARGA:

        LINHA_RESTRICAO = """<tr class="LINHA_MOTIVO">
                                <td colspan=3 rowspan="2" class="EXCLAMACAO_RESTRICAO">
                                    RESTRIÇÃO
                                </td>"""
    
        for MOTIVO in DESCARGA["RESTRICAO_MOTIVO"]:
                            
            if MOTIVO == 0: MOTIVO = "."              
            
            LINHA_RESTRICAO += f"""<td class="RESTRICAO_ATIVA"> {MOTIVO} </td>"""            
                        
        LINHA_RESTRICAO += """<td colspan=2 rowspan="2" class="FIM_RESTRICAO">
                                <svg fill="#FFFFFF" height="50px" width="50px" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="-24.86 -24.86 360.53 360.53" xml:space="preserve" stroke="#FFFFFFF" stroke-width="6.21612">
                                    <g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g>
                                    <g id="SVGRepo_iconCarrier"> <path d="M305.095,229.104L186.055,42.579c-6.713-10.52-18.172-16.801-30.652-16.801c-12.481,0-23.94,6.281-30.651,16.801 L5.711,229.103c-7.145,11.197-7.619,25.39-1.233,37.042c6.386,11.647,18.604,18.883,31.886,18.883h238.079 c13.282,0,25.5-7.235,31.888-18.886C312.714,254.493,312.24,240.301,305.095,229.104z M155.403,253.631 c-10.947,0-19.82-8.874-19.82-19.82c0-10.947,8.874-19.821,19.82-19.821c10.947,0,19.82,8.874,19.82,19.821 C175.223,244.757,166.349,253.631,155.403,253.631z M182.875,115.9l-9.762,65.727c-1.437,9.675-10.445,16.353-20.119,14.916 c-7.816-1.161-13.676-7.289-14.881-14.692l-10.601-65.597c-2.468-15.273,7.912-29.655,23.185-32.123 c15.273-2.468,29.655,7.912,32.123,23.185C183.284,110.192,183.268,113.161,182.875,115.9z"></path> </g>
                                </svg>
                            </td>
                        </tr>"""
                        
        LINHA_RESTRICAO += """ <tr class="LINHA_PCT">"""
                         
        for RESTRICAO in DESCARGA["RESTRICAO_PCT"]:                    
            if RESTRICAO == 0: RESTRICAO = "."  
                            
            LINHA_RESTRICAO += f"""<td class="RESTRICAO_ATIVA">{ RESTRICAO }</td>"""

        LINHA_RESTRICAO += "</tr>"
    
    #endregion

    DESCARGA_HTML = HEADER + LINHA_SALDO + LINHA_CHEGADA + LINHA_PEDRA + DESCARGAS + LINHA_TOTAIS_PEDRA + LINHA_RESTRICAO

    return DESCARGA_HTML

def DESCARGA_HTML(TERMINAL, DIA_LOGISTICO):

    #region ABRINDO DADOS NECESSÁRIOS
    PERIODO_VIGENTE     = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
    RESTRICOES_ATIVAS   = pd.read_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv", encoding='utf-8-sig', sep=';', index_col=0)
    
    TERMINAIS_ATIVOS    = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
    TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)
    

    LINHA       = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO]
    DATA_ARQ    = LINHA['DATA_ARQ'].values[0]
    
    with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO_DESCARGA:
        jsDESCARGA = json.load(ARQUIVO_DESCARGA)


    with open(f"previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
        INFOS = json.load(ARQUIVO_DESCARGA)
    #endregion

    #region ABRINDO ITENS QUE ESTÃO ATIVOS
    DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
    DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS]                                                   # <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]

    DESCARGAS_RESTRICOES    = RESTRICOES_ATIVAS.drop('RESTRICAO', axis=1)  
    PRODUTO_RESTRICAO       = DESCARGAS_RESTRICOES.loc[TERMINAL][DESCARGAS_RESTRICOES.loc[TERMINAL] > 0].index.tolist() # <-- ['ACUCAR']
    #endregion

    #region LENDO AS DESCARGAS ATIVAS
    FERROVIAS_ATIVAS = { "RUMO": [], "MRS" : [], "VLI" : [] }

    for ATIVO in DESCARGAS_ATIVAS:
        for FERROVIA in FERROVIAS_ATIVAS:
            if ATIVO[0] == FERROVIA: FERROVIAS_ATIVAS[FERROVIA].append(ATIVO[1]) 
    #endregion

    if len(DESCARGAS_ATIVAS) == 0:
        return ""

    #region LENDO AS RESTRICAOES ATIVAS
    FERROVIA_ALEATORA_DO_TERMINAL = next(iter(jsDESCARGA["DESCARGAS"]))
    if len(PRODUTO_RESTRICAO) > 0: 
        jsDESCARGA["RESTRICAO_PCT"] = jsDESCARGA["DESCARGAS"][FERROVIA_ALEATORA_DO_TERMINAL][PRODUTO_RESTRICAO[0]]["RESTRICAO"]
    #endregion

    #region FILTRANDO jsDESCARGA
    for FERROVIA in FERROVIAS_ATIVAS:
        jsDESCARGA["DESCARGAS"][FERROVIA] = {chave: valor for chave, valor in jsDESCARGA["DESCARGAS"][FERROVIA].items() if chave in FERROVIAS_ATIVAS[FERROVIA]}

    #endregion

    return MONTAR_HTML(jsDESCARGA, TERMINAL, DIA_LOGISTICO, DATA_ARQ, INFOS)