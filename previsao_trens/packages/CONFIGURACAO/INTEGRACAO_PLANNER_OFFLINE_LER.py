import  os
import  json
import  pandas as pd
import  warnings

from    previsao_trens.models                                   import Trem, Restricao, Mercadoria, Terminal
from    previsao_trens.packages.descarga.EDITAR_DESCARGA        import NAVEGACAO_DESCARGA
from    datetime                                                import datetime, timedelta
from    previsao_trens.forms                                    import TremForm
from    previsao_trens.packages.CONFIGURACAO.ATUALIZAR_DESCARGA import ATUALIZAR_DESCARGA

# Ignorando FutureWarning específico

def _json_to_form_data(json_data):
    form_data = {
        'prefixo'   : json_data.get('PREFIXO', ''),
        'os'        : json_data.get('OS', 0),
        'origem'    : json_data.get('ORIGEM', ''),
        'local'     : json_data.get('SB_ATUAL', ''),
        'destino'   : json_data.get('DESTINO', ''),
        'terminal'  : Terminal.objects.get(nome=json_data.get('TERMINAL_DESTINO', '')), 
        'encoste'   : (datetime.strptime(json_data.get('PREVISAO', ''), "%Y-%m-%d %H:%M:%S") + timedelta(hours=Terminal.objects.get(nome=json_data.get('TERMINAL_DESTINO', '')).tempo_encoste)),
        'mercadoria': Mercadoria.objects.get(nome=json_data.get('MERCADORIA', '')),
        'vagoes'    : json_data.get('VAGOES', 0),
        'previsao'  : json_data.get('PREVISAO', ''),
        'ferrovia'  : json_data.get('FERROVIA', ''),
        'comentario': '',  # Adicione um campo comentário vazio ou conforme necessário
    }
    return form_data

def _ajustar_trem(json_data):

    if json_data["MERCADORIA"] == "CONTEINER": json_data["FERROVIA"] = "MRS"
    
    return json_data

class AtualizandoSistema:

    def limparPrevisao():
        
        trens = Trem.objects.all()
        
        for trem in trens:
            
            trem.delete()

    def inserirNovosTrens(novos_trens, usuario_logado):
        
        for dia_log in novos_trens:
            print(dia_log)
            if len(novos_trens[dia_log]) > 0:

                
                novos_trens[dia_log].reverse()
                for dict_trem in novos_trens[dia_log]:
                    
                    print(f"\t  { dict_trem["PREFIXO"] } { dict_trem["TERMINAL_DESTINO"] } { dict_trem["MERCADORIA"] } ")
                    
                    dict_trem = _ajustar_trem(dict_trem)

                    form_trem = TremForm(_json_to_form_data(dict_trem))
                    
                    if form_trem.is_valid():
                        
                        trem  = form_trem.save(commit=False)
                        trem.created_by = usuario_logado
                        trem.save()

                    else:
                        print(f"erro ao inserir o trem: {dict_trem["PREFIXO"]} - {form_trem.errors}")
                        
    def limparRestricao():

        restricoes = Restricao.objects.all()
        
        for restricao in restricoes:

            restricao.excluir_restricao()

    def inserirNovasRestricoes(novas_restricoes, usuario_logado):

        for dict_restricao in novas_restricoes:

            form_restricao = Restricao.json_to_form(dict_restricao)
            Restricao.criar_restricao(form_restricao, usuario_logado)

    def limparSaldosVirada():
       
        PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        linha           = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == "D"]
        data_arq        = linha['DATA_ARQ'].values[0]

        terminais = os.listdir("previsao_trens/src/DESCARGAS")
        print(terminais)
        for terminal in terminais:

            with open(f"previsao_trens/src/DESCARGAS/{ terminal }/descarga_{ data_arq }.json") as ARQUIVO_DESCARGA:
                descarga = json.load(ARQUIVO_DESCARGA)

            for ferrovia in descarga["DESCARGAS"]:

                for produto in descarga["DESCARGAS"][ferrovia]:

                    descarga["DESCARGAS"][ferrovia][produto]["INDICADORES"]["SALDO_DE_VIRADA"] = 0

                    PARAMETROS = {
                    'TERMINAL'  :   terminal, 
                    'DATA_ARQ'  :   data_arq, 
                    'PRODUTO'   :   produto, 
                    'FERROVIA'  :   ferrovia, 
                    
                    'VALOR'     :   0,      
                    }
                    try:
                        Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                        Descarga.EDITAR_SALDO_VIRADA(PARAMETROS) 
                    except Exception as e:
                        print(f"[erro] - limparSaldosVirada: {e} - [{ PARAMETROS}]")



    def ativarTerminais(json_descargas_ativas):

        descargas_ativas_offline = pd.DataFrame.from_dict(json_descargas_ativas, orient='index')
        idx_restricao = descargas_ativas_offline.columns.get_loc('RESTRICAO')
        
        # Dividir o DataFrame em duas partes
        terminais_ativos_offline    = descargas_ativas_offline.iloc[:, :idx_restricao]
        restricoes_ativas_offline   = descargas_ativas_offline.iloc[:, idx_restricao:]
        
        TERMINAIS_ATIVOS  = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
        RESTRICOES_ATIVAS = pd.read_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv", encoding='utf-8-sig', sep=';', index_col=0)
         
        #TERMINAIS_ATIVOS
        common_index    = TERMINAIS_ATIVOS.index.intersection(terminais_ativos_offline.index)
        common_columns  = TERMINAIS_ATIVOS.columns.intersection(terminais_ativos_offline.columns)

        TERMINAIS_ATIVOS.loc[common_index, common_columns] = terminais_ativos_offline.loc[common_index, common_columns]
        
        #RESTRICOES_ATIVAS 
        common_index    = RESTRICOES_ATIVAS.index.intersection(restricoes_ativas_offline.index)
        common_columns  = RESTRICOES_ATIVAS.columns.intersection(restricoes_ativas_offline.columns)

        RESTRICOES_ATIVAS.loc[common_index, common_columns] = restricoes_ativas_offline.loc[common_index, common_columns]

        #region CORRIGINDO ERROS CASO TERMINAL ATIVO SEM DESCARGA ( E RESTRICAO ATIVA SEM PRODUTO)

        #if 'TERMINAL' not in TERMINAIS_ATIVOS.columns: TERMINAIS_ATIVOS['TERMINAL'] = 0
        
        for index, row in TERMINAIS_ATIVOS.iterrows():
            sum_columns = 0
            for col in TERMINAIS_ATIVOS.columns[1:]:

                if pd.to_numeric(row[col], errors='coerce') == row[col]:
                    sum_columns += pd.to_numeric(row[col])
                else:
                    sum_columns += 0  # Se não for numérico, adicionar 0
    

            TERMINAIS_ATIVOS.at[index, 'TERMINAL'] = sum_columns

        

        for index, row in RESTRICOES_ATIVAS.iterrows():

            sum_columns = 0
            
            for col in RESTRICOES_ATIVAS.columns[1:]:

                if pd.to_numeric(row[col], errors='coerce') == row[col]:
                    sum_columns += pd.to_numeric(row[col])
                else:
                    sum_columns += 0  
            

            RESTRICOES_ATIVAS.at[index, 'RESTRICAO'] = sum_columns
        #endregion

        TERMINAIS_ATIVOS.loc["SBR", "RUMO_CONTEINER"]     = 0
        TERMINAIS_ATIVOS.loc["TECONDI", "RUMO_CONTEINER"] = 0

        TERMINAIS_ATIVOS.to_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",   sep=";")
        RESTRICOES_ATIVAS.to_csv("previsao_trens/src/PARAMETROS/RESTRICOES_ATIVAS.csv", sep=";")

    def inserirSaldosVidada(js_saldos_virada):

        PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        linha           = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == "D"]
        DATA_ARQ        = linha['DATA_ARQ'].values[0]

        TERMINAIS_ATIVOS    = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
        lst_terminais_ativos = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()
        
        saldos_de_virada_offline = pd.DataFrame.from_dict(js_saldos_virada, orient='index')   

        for TERMINAL in lst_terminais_ativos:

            DESCARGAS_ATIVAS = saldos_de_virada_offline.loc[TERMINAL][saldos_de_virada_offline.loc[TERMINAL] > 0].index.tolist()
            DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]
              
            for ATIVO in DESCARGAS_ATIVAS:

                if TERMINAL == "SBR"     and ATIVO[1] == "RUMO": ATIVO[1] = "MRS"
                if TERMINAL == "TECONDI" and ATIVO[1] == "RUMO": ATIVO[1] = "MRS"

                saldo = saldos_de_virada_offline.at[TERMINAL, f"SLD_{ATIVO[1]}_{ATIVO[2]}"]      

                PARAMETROS = {
                    'TERMINAL'  :   TERMINAL, 
                    'DATA_ARQ'  :   DATA_ARQ, 
                    'PRODUTO'   :   ATIVO[2], 
                    'FERROVIA'  :   ATIVO[1], 
                    
                    'VALOR'     :   int(saldo),      
                }
                try:
                    Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                    Descarga.EDITAR_SALDO_VIRADA(PARAMETROS)   
                except Exception as e:
                    print(f"[erro] - limparSaldosVirada: {e} - [{ PARAMETROS}]") 
                        
    def inserirProdutividade(json_descargas):
        print("inserindo produtividade")
        with warnings.catch_warnings():
            
            warnings.simplefilter("ignore", category=FutureWarning)
            
            TERMINAIS_ATIVOS    = pd.read_csv("previsao_trens/src/PARAMETROS/DESCARGAS_ATIVAS.csv",  encoding='utf-8-sig', sep=';', index_col=0)
            lst_terminais_ativos = TERMINAIS_ATIVOS[TERMINAIS_ATIVOS['TERMINAL'] > 0].index.tolist()  
            TERMINAIS_ATIVOS.drop('TERMINAL', axis=1, inplace=True)

            lst_terminais_ativos = list(set(lst_terminais_ativos).intersection(list(json_descargas["D"].keys())))
            print(f"terminais ativos: {lst_terminais_ativos}")
            for DIA_LOGISTICO in list(json_descargas.keys()):

                PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
                linha           = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == DIA_LOGISTICO]
                DATA_ARQ        = linha['DATA_ARQ'].values[0]

                for TERMINAL in lst_terminais_ativos:
                    print(f"\t {TERMINAL}")
                    DESCARGAS_ATIVAS = TERMINAIS_ATIVOS.loc[TERMINAL][TERMINAIS_ATIVOS.loc[TERMINAL] > 0].index.tolist()
                    DESCARGAS_ATIVAS = [item.split('_') for item in DESCARGAS_ATIVAS] #  <-- [['RUMO', 'FARELO'], ['RUMO', 'SOJA'], ['MRS', 'SOJA'], ['RUMO', 'MILHO']]
                
                    with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json") as ARQUIVO:
                        DESCARGA = json.load(ARQUIVO)  
                    

                    try:
                        json_string     = json_descargas[DIA_LOGISTICO][TERMINAL].strip('"')
                        json_string     = json_string.replace('\'', '"')
                        json_string     = json_string.replace('nan', '0')    
                        descarga_dict    = json.loads(json_string)
                    except json.JSONDecodeError as e:
                        print(f"Erro na linha {e.lineno}, coluna {e.colno}: {e.msg}")
                        # Exibir uma parte do JSON próximo ao erro para inspeção
                        erro_index = e.pos
                        erro_vizinho = 50  # número de caracteres a mostrar ao redor do erro
                        print(json_string[max(0, erro_index-erro_vizinho):erro_index+erro_vizinho])


                    descarga_offline = pd.DataFrame.from_dict(descarga_dict, orient='index') 
                    descarga_offline.drop(columns=['TOTAIS'], inplace=True)
                    descarga_offline.replace('-', 0, inplace=True)

                    for ATIVO in DESCARGAS_ATIVAS:

                        try:

                            produtividade_offline = descarga_offline.loc[f"{ATIVO[0]}_{ATIVO[1]}_prod"].tolist()
                            produtividade_offline = [int(float(x)) for x in produtividade_offline]
                            
                            if TERMINAL == "SBR"     and ATIVO[0] == "RUMO": ATIVO[0] = "MRS"
                            if TERMINAL == "TECONDI" and ATIVO[0] == "RUMO": ATIVO[0] = "MRS"
                            
                            DESCARGA["DESCARGAS"][ATIVO[0]][ATIVO[1]]["PRODUTIVIDADE"] = produtividade_offline
                            DESCARGA["DESCARGAS"][ATIVO[0]][ATIVO[1]]["EDITADO"] = [1] * 24
                        except KeyError:
                            pass
                    
                    with open(f"previsao_trens/src/DESCARGAS/{ TERMINAL }/descarga_{ DATA_ARQ }.json", 'w') as ARQUIVO:
                        json.dump(DESCARGA, ARQUIVO, indent=4)

    def atualizarCalculos():
        
        PERIODO_VIGENTE = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        linha           = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == "D"]
        data_arq        = linha['DATA_ARQ'].values[0]

        terminais = os.listdir("previsao_trens/src/DESCARGAS")

        for terminal in terminais:

            with open(f"previsao_trens/src/DESCARGAS/{ terminal }/descarga_{ data_arq }.json") as ARQUIVO_DESCARGA:
                descarga = json.load(ARQUIVO_DESCARGA)

            for ferrovia in descarga["DESCARGAS"]:

                for produto in descarga["DESCARGAS"][ferrovia]:

                    PARAMETROS = {
                        'TERMINAL'  :   terminal, 
                        'DATA_ARQ'  :   data_arq, 
                        'PRODUTO'   :   produto, 
                        'FERROVIA'  :   ferrovia,       
                        'VALOR'     :   descarga["DESCARGAS"][ferrovia][produto]["INDICADORES"]["SALDO_DE_VIRADA"],      
                    }
                    try:
                        Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                        Descarga.EDITAR_SALDO_VIRADA(PARAMETROS) 
                    except Exception as e:
                        print(f"[erro] - limparSaldosVirada: {e} - [{ PARAMETROS}]")

def lerDados(JSON, usuario_logado):

    ATUALIZAR_DESCARGA()

    
    
    
    AtualizandoSistema.limparPrevisao()
    AtualizandoSistema.limparRestricao()
    
    AtualizandoSistema.inserirNovosTrens(JSON["PREVISOES"], usuario_logado)
    AtualizandoSistema.inserirNovasRestricoes(JSON["RESTRICOES"], usuario_logado)
    
    
    AtualizandoSistema.ativarTerminais(JSON["DESCARGAS_ATIVAS"])
    
    AtualizandoSistema.limparSaldosVirada()
    AtualizandoSistema.inserirSaldosVidada(JSON["SALDOS_VIRADA"])   
    AtualizandoSistema.inserirProdutividade(JSON["DESCARGAS"])
    AtualizandoSistema.atualizarCalculos()