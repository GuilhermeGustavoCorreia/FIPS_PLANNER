
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts               import redirect
from django.urls                    import reverse
from django.forms.models            import model_to_dict

from django.db import transaction

from .models        import Trem, Restricao, TremVazio
from .forms         import TremForm, RestricaoForm, TremVazioForm
from django.contrib import messages

from    previsao_trens.packages.CONFIGURACAO.CARREGAR_PAGINA    import ABRIR_TERMINAIS_ATIVOS
from    previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS  import EDITAR_PARAMETROS, EDITAR_PARAMOS_SUBIDAS, EDITAR_PARAMOS_PXO
from    previsao_trens.packages.CONFIGURACAO.ATUALIZAR_DESCARGA import ATUALIZAR_DESCARGA
from    previsao_trens.packages.CONFIGURACAO.EXPORTAR_PLANILHA  import BAIXAR_PLANILHA 
from    previsao_trens.packages.CONFIGURACAO.BAIXAR_DETALHE     import BAIXAR_DETALHE
from    previsao_trens.packages.CONFIGURACAO.INTEGRACAO_PLANNER_OFFLINE_GERAR     import    BAIXAR_DADOS
from    previsao_trens.packages.CONFIGURACAO.INTEGRACAO_PLANNER_OFFLINE_LER       import    lerDados

from    previsao_trens.packages.CRIAR_TREM.VALIDAR           import VALIDAR_NOVA_PREVISAO, VALIDAR_EDICAO_PREVISAO, VALIDAR_DIVISAO_PREVISAO
from    previsao_trens.packages.CRIAR_TREM.ATUALIZAR_POSICAO import AJUSTAR_POSICAO_CHEGADA, ALTERAR_POSICAO

import  previsao_trens.packages.descarga.CARREGAR_PAGINA as CARREGAR_DESCARGA
from    previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as NAVEGACAO_DESCARGA

from previsao_trens.packages.PROG_SUBIDA.CARREGAR_PAGINA    import CARREGAR_PROG_SUBIDA, CARREGAR_PREVISAO_SUBIDA
from previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA    import editarSaldoViradaVazios, editarSaldoViradaVaziosNaLinha

from previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2     import SUBIDA_DE_VAZIOS, EDITAR_SALDO_VIRADA_TERMINAL, EDITAR_BUFFER, EDITAR_SALDO_CONDENSADO, Condensados
from previsao_trens.packages.DETELHE.CARREGAR_PAGINA            import CARREGAR_RELATORIO_DETALHE
from previsao_trens.packages.RELATORIO_OCUPACAO.CARREGAR_PAGINA import CARREGAR_RELATORIO_OCUPACAO
from previsao_trens.packages.RELATORIO_OCUPACAO.DESCARGA_HTML   import DESCARGA_HTML
from previsao_trens.packages.RESTRICAO.VALIDAR                  import VALIDAR_RESTRICAO

from    .forms      import UploadFileForm
from    io          import TextIOWrapper
from    datetime    import datetime, time
import  json
import  pandas as pd

import  csv

from django.http import QueryDict


def REQUEST_PARA_DICT(request):
    # Combina os parâmetros GET e POST em um único dicionário
    request_params = QueryDict('', mutable=True)
    request_params.update(request.GET)
    request_params.update(request.POST)
    
    # Converte o QueryDict para um dicionário normal
    return dict(request_params)

def redirect_to_login(request):
    
    return redirect(reverse('login'))


#region NAVEGACAO
@login_required
def navegacao(request):
    
    if request.method == 'POST':
        with transaction.atomic():  
               
            REQUISICAO =  dict(request.POST)
            ACAO = REQUISICAO["ACAO"][0]

            if ACAO == "EDITAR_PRODUTIVIDADE":

                PARAMETROS = {
                    'TERMINAL'  :   REQUISICAO['TERMINAL'][0], 
                    'DATA_ARQ'  :   REQUISICAO['DATA_ARQ'][0], 
                    'PRODUTO'   :   REQUISICAO['PRODUTO'][0], 
                    'FERROVIA'  :   REQUISICAO['FERROVIA'][0], 
                    'CELULAS'   :   [int(valor) for valor in REQUISICAO['CELULAS[]']], #EM ACAO=="EDITAR_SALDO_DE_VIRADA" ISTO NAO É USADO.
                    'VALOR'     :   int(REQUISICAO['VALOR'][0]),      
                }

                    
                Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                DESCARGAS = Descarga.EDITAR_PRODUTIVIDADE(PARAMETROS)

                return JsonResponse(DESCARGAS, safe=False)


            if ACAO == "EDITAR_SALDO_DE_VIRADA":

                PARAMETROS = {
                    'TERMINAL'  :   REQUISICAO['TERMINAL'][0], 
                    'DATA_ARQ'  :   REQUISICAO['DATA_ARQ'][0], 
                    'PRODUTO'   :   REQUISICAO['PRODUTO'][0], 
                    'FERROVIA'  :   REQUISICAO['FERROVIA'][0], 
                    
                    'VALOR'     :   int(REQUISICAO['VALOR'][0]),      
                }

                Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                DESCARGAS = Descarga.EDITAR_SALDO_VIRADA(PARAMETROS)

                return JsonResponse(DESCARGAS, safe=False)

            if ACAO == "EDITAR_CONSTANTE_PRODUTIVIDADE":

                PARAMETROS = {
                    'TERMINAL'  :   REQUISICAO['TERMINAL'][0], 
                    'DATA_ARQ'  :   REQUISICAO['DATA_ARQ'][0], 
                    'PRODUTO'   :   REQUISICAO['PRODUTO'][0], 
                    'FERROVIA'  :   REQUISICAO['FERROVIA'][0], 
                    
                    'VALOR'     :   int(REQUISICAO['VALOR'][0]),      
                }

                with open("previsao_trens/src/DICIONARIOS/TERMINAIS.json") as ARQUIVO_DESCARGA:
                    TERMINAIS_INFOS = json.load(ARQUIVO_DESCARGA)

                TERMINAIS_INFOS[PARAMETROS["TERMINAL"]]["PRODUTIVIDADE"][PARAMETROS["FERROVIA"]][PARAMETROS["PRODUTO"]] = PARAMETROS["VALOR"]

                with open("previsao_trens/src/DICIONARIOS/TERMINAIS.json", 'w') as ARQUIVO_NOME:
                    json.dump(TERMINAIS_INFOS, ARQUIVO_NOME, indent=4)

                Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
                Descarga.ATUALIZAR_CALCULO()

    DESCARGAS = CARREGAR_DESCARGA.PAGINA_COMPLETA()
    return render(request, 'navegacao.html', {"CONTEUDO_NAVEGACAO": DESCARGAS})
#endregion


@login_required
def profile(request):

    return render(request, 'user/profile.html')

#region PAGINA CRIAR TREM

tipo_formulario : str
trem_form       : object


def carregar_tabela_de_previsoes():
    
    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    periodo_vigente = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
    
    tabelas_de_previsoes = {}

    for _, linha in periodo_vigente.iterrows():

            DATA = datetime.strptime(linha['DATA_ARQ'], '%Y-%m-%d')

            queryset = Trem.objects.filter(
                previsao__year=DATA.year,
                previsao__month=DATA.month,
                previsao__day=DATA.day
            ).order_by('posicao_previsao')
            if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
                tabelas_de_previsoes[linha['NM_DIA']] = queryset

    return tabelas_de_previsoes

def carregar_previsao_trens(request, trem_form, tipo_formulario):

    tabelas_de_previsoes = carregar_tabela_de_previsoes()

    return render(request, 'previsao/criar_trem.html', {'TABELAS': tabelas_de_previsoes, 'form': trem_form, "TIPO_FORMULARIO": tipo_formulario})

@login_required
def previsao_trens_view(request):

    trem_form            = TremForm()
    tipo_formulario      = None
    
    return carregar_previsao_trens(request, trem_form, tipo_formulario)

@login_required
def alterar_posicao_view(request):

    PARAMETROS = {
                "DIA_LOGISTICO" : request.POST.get('DIA_LOGISTICO'),
                "POSICAO_A"     : int(request.POST.get('POSICAO_A')),
                "POSICAO_B"     : int(request.POST.get('POSICAO_B')),
                "TREM"          : request.POST.get('TREM'),
            }
    
    ALTERAR_POSICAO(PARAMETROS)
    
    return redirect('previsao_trens')

@login_required
def criar_trem_view(request):
    
    if request.method == 'POST':    
       
        trem_form = TremForm()
        resultado = Trem.criar_trem(request.POST, request.user)

        if resultado["status"]:
            messages.success(request, resultado["descricao"])
            return redirect('previsao_trens')
        
        else:

            if resultado["descricao"]:  messages.error(request, resultado["descricao"])
            if resultado["errors"]:     messages.error(request, resultado["errors"])
            
            tipo_formulario = "CRIAR_TREM"
            trem_form = TremForm(request.POST)


        return carregar_previsao_trens(request, trem_form, tipo_formulario)
    
    else: 
        
        return redirect('previsao_trens')

@login_required
def excluir_trem_view(request, id):
    

    trem = get_object_or_404(Trem, pk=id)
    trem.excluir_trem()
    
    return redirect('previsao_trens')
    
@login_required
def editar_trem(request, trem_id):

    TABELAS = carregar_tabela_de_previsoes()
    TIPO_FORMULARIO = "EDITAR_TREM"
    #ESTA ENVIANDO A EDICAO
    if request.method == 'POST':
        with transaction.atomic():
            FORMULARIO_NOVO_TREM = TremForm(request.POST)

            if FORMULARIO_NOVO_TREM.is_valid():
                
                #VALIDANDO SE NOVO TREM ATENDE CRITÉRIOS
                CRITERIOS_AVALIADOS = VALIDAR_EDICAO_PREVISAO(FORMULARIO_NOVO_TREM.cleaned_data, trem_id)
                if not CRITERIOS_AVALIADOS["STATUS"]:

                    messages.error(request, CRITERIOS_AVALIADOS["DESCRICAO"])
                    return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': FORMULARIO_NOVO_TREM, "TIPO_FORMULARIO": TIPO_FORMULARIO})

                # Remover o trem antigo após capturar posição
                TREM_ANTIGO = Trem.objects.get(pk=trem_id) 
                dict_TREM_ANTIGO = model_to_dict(TREM_ANTIGO)       
                
                NOVO_TREM   = FORMULARIO_NOVO_TREM.save(commit=False)
                NOVO_TREM.created_by = request.user
                NOVO_TREM.posicao_previsao = AJUSTAR_POSICAO_CHEGADA(ACAO="EDITAR TREM", TREM_ANTIGO = TREM_ANTIGO, NOVO_TREM=NOVO_TREM)
                dict_NOVO_TREM = model_to_dict(NOVO_TREM)
                
                #ISSO TEM QUE SER AS ULTIMAS COISAS A SE FAZER
                TREM_ANTIGO.delete()
                
                NOVO_TREM.save()
                dict_NOVO_TREM["ID"] = NOVO_TREM.id

                #EDITANDO NA DESCARGA
                try:
                    NAVEGACAO_A = NAVEGACAO_DESCARGA(dict_TREM_ANTIGO["terminal"], dict_TREM_ANTIGO["ferrovia"], dict_TREM_ANTIGO["mercadoria"])
                    NAVEGACAO_A.EDITAR_TREM(dict_TREM_ANTIGO, "REMOVER")

                except IndexError :
                    NAVEGACAO_A = NAVEGACAO_DESCARGA(dict_TREM_ANTIGO["terminal"], dict_TREM_ANTIGO["ferrovia"], dict_TREM_ANTIGO["mercadoria"], DIA_ANTERIOR=True)
                    NAVEGACAO_A.EDITAR_TREM(dict_TREM_ANTIGO, "REMOVER")
    
                try:    
                    NAVEGACAO_B = NAVEGACAO_DESCARGA(dict_NOVO_TREM["terminal"], dict_NOVO_TREM["ferrovia"], dict_NOVO_TREM["mercadoria"])
                    NAVEGACAO_B.EDITAR_TREM(dict_NOVO_TREM, "INSERIR")

                except IndexError :
                    NAVEGACAO_B = NAVEGACAO_DESCARGA(dict_NOVO_TREM["terminal"], dict_NOVO_TREM["ferrovia"], dict_NOVO_TREM["mercadoria"], DIA_ANTERIOR=True)
                    NAVEGACAO_B.EDITAR_TREM(dict_NOVO_TREM, "INSERIR")

                messages.success(request, "Trem editado com sucesso.")
                return redirect('previsao_trens')
            else:
                messages.error(request, FORMULARIO_NOVO_TREM.errors)
                return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': FORMULARIO_NOVO_TREM, "TIPO_FORMULARIO": TIPO_FORMULARIO})
    
    #ABRINDO O FORMULARIO DE EDICAO
    else:
        
        # Busca o objeto Trem, ou retorna um erro 404 se não encontrado
        trem = get_object_or_404(Trem, pk=trem_id)
        
        # Cria um dicionário com os dados do trem
        trem_data = {
            "prefixo":      trem.prefixo,
            "os":           trem.os,
            "vagoes":       trem.vagoes,
            "mercadoria":   trem.mercadoria,
            "origem":       trem.origem,
            "local":        trem.local,
            "destino":      trem.destino,
            "terminal":     trem.terminal,
            "previsao":     trem.previsao.strftime('%Y-%m-%d %H:%M'),  # Formatação de data e hora
            "comentario":   trem.comentario,
            "ferrovia":     trem.ferrovia,
        }
        
        # Retorna os dados como JSON
        return JsonResponse(trem_data)

@login_required
def dividir_trem(request, trem_id):
    
    TREM_ORIGINAL = get_object_or_404(Trem, pk=trem_id)

    if request.method == 'POST':
        with transaction.atomic():
            
            # PRIMEIRO VAMOS DEFINIR AS POSICOES DE CADA ELEMENTO DIVIDIDO
            # Definindo dados dos novos trens
            TREM_01 = {
                "prefixo"          : TREM_ORIGINAL.prefixo,
                "os"               : TREM_ORIGINAL.os,
                "origem"           : TREM_ORIGINAL.origem,
                "local"            : TREM_ORIGINAL.local,
                "posicao_previsao" : 1,
                "ferrovia"         : TREM_ORIGINAL.ferrovia,
                "comentario"       : TREM_ORIGINAL.comentario,

                "destino"     :request.POST.get('destino_01'),
                "terminal"    :request.POST.get('terminal_01'),
                "mercadoria"  :request.POST.get('mercadoria_01'),
                "vagoes"      :request.POST.get('vagoes_01', 0),
                "previsao"    :request.POST.get('previsao_01'), 
            }

            TREM_02 = {
                "prefixo"          : TREM_ORIGINAL.prefixo,
                "os"               : TREM_ORIGINAL.os,
                "origem"           : TREM_ORIGINAL.origem,
                "local"            : TREM_ORIGINAL.local,
                "posicao_previsao" : 2,
                "ferrovia"         : TREM_ORIGINAL.ferrovia,
                "comentario"       : TREM_ORIGINAL.comentario,

                "destino"     :request.POST.get('destino_02'),
                "terminal"    :request.POST.get('terminal_02'),
                "mercadoria"  :request.POST.get('mercadoria_02'),
                "vagoes"      :request.POST.get('vagoes_02', 0),
                "previsao"    :request.POST.get('previsao_02'), 
            }
            
            FRM_TREM_01 = TremForm(TREM_01)
            FRM_TREM_02 = TremForm(TREM_02)

            if FRM_TREM_01.is_valid() and FRM_TREM_02.is_valid():
                
                CRITERIOS_AVALIADOS = VALIDAR_DIVISAO_PREVISAO(trem_id, FRM_TREM_01.cleaned_data, FRM_TREM_02.cleaned_data)  

                if CRITERIOS_AVALIADOS["STATUS"] == False:

                    messages.error(request, CRITERIOS_AVALIADOS["DESCRICAO"])
                    return redirect("criar_trem")

                POSICOES = AJUSTAR_POSICAO_CHEGADA(ACAO="DIVIDIR TREM", TREM_ANTIGO=TREM_ORIGINAL, TREM_01=FRM_TREM_01.cleaned_data, TREM_02=FRM_TREM_02.cleaned_data)
                
                TREM_01 = FRM_TREM_01.save(commit = False)
                TREM_02 = FRM_TREM_02.save(commit = False)

                TREM_01.created_by = request.user
                TREM_02.created_by = request.user

                TREM_01.posicao_previsao = POSICOES["POSICAO_01"]
                TREM_02.posicao_previsao = POSICOES["POSICAO_02"]

                dict_TREM_ORIGINAL  = model_to_dict(TREM_ORIGINAL)
                dict_TREM_01        = model_to_dict(TREM_01)
                dict_TREM_02        = model_to_dict(TREM_02)

                TREM_ORIGINAL.delete()
                
                TREM_01.save()
                TREM_02.save()
                
                dict_TREM_01["ID"] = TREM_01.id
                dict_TREM_02["ID"] = TREM_02.id

                #EDITANDO NA DESCARGA
                NAVEGACAO_A = NAVEGACAO_DESCARGA(dict_TREM_ORIGINAL["terminal"], dict_TREM_ORIGINAL["ferrovia"], dict_TREM_ORIGINAL["mercadoria"]) #1
                NAVEGACAO_A.EDITAR_TREM(dict_TREM_ORIGINAL, "REMOVER")

                NAVEGACAO_B = NAVEGACAO_DESCARGA(dict_TREM_01["terminal"], dict_TREM_01["ferrovia"], dict_TREM_01["mercadoria"]) #2
                NAVEGACAO_B.EDITAR_TREM(dict_TREM_01, "INSERIR")

                NAVEGACAO_C = NAVEGACAO_DESCARGA(dict_TREM_02["terminal"], dict_TREM_02["ferrovia"], dict_TREM_02["mercadoria"]) #3
                NAVEGACAO_C.EDITAR_TREM(dict_TREM_02, "INSERIR")

            else: 

                return JsonResponse({'error': 'Dados inválidos'}, status=400)

            return redirect("previsao_trens")

    else:
        trem_data = {
                "prefixo":      TREM_ORIGINAL.prefixo,
                "os":           TREM_ORIGINAL.os,
                "vagoes":       TREM_ORIGINAL.vagoes,
                "mercadoria":   TREM_ORIGINAL.mercadoria,
                "origem":       TREM_ORIGINAL.origem,
                "local":        TREM_ORIGINAL.local,
                "destino":      TREM_ORIGINAL.destino,
                "terminal":     TREM_ORIGINAL.terminal,
                "previsao":     TREM_ORIGINAL.previsao.strftime('%Y-%m-%d %H:%M'),  # Formatação de data e hora
                "comentario":   TREM_ORIGINAL.comentario,
                "ferrovia":     TREM_ORIGINAL.ferrovia,
            }


        with open(f"previsao_trens/src/DICIONARIOS/PRODUTOS_E_TERMINAIS.json") as ARQUIVO_DESCARGA:
            PROD_TERMINA = json.load(ARQUIVO_DESCARGA)

        SAIDAS = {
            "TREM": trem_data,
            "produtos_terminais": PROD_TERMINA
        }

        return JsonResponse(SAIDAS)

@login_required
def upload_file_view(request):

    if request.method == 'POST':
        with transaction.atomic():
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file    = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
                reader  = csv.DictReader(file, delimiter=';')
                
                for index, row in enumerate(reader):

                    datetime_str = f"{row['PREVISAO_DATA']} {row['PREVISAO_HORA']}"
                    previsao_datetime = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M")

                    trem = Trem(

                        os=int(row['OS']),
                        prefixo=row['PREFIXO'],
                        origem=row['ORIGEM'],
                        local=row['SB_ATUAL'],
                        destino=row['DESTINO'],
                        terminal=row['TERMINAL_DESTINO'],
                        mercadoria=row['MERCADORIA'],
                        vagoes=int(row['VAGOES']),
                        previsao=previsao_datetime,
                        ferrovia=row['FERROVIA'],
                        comentario='Ola',  # Valor padrão ou adicione lógica para comentários
                        posicao_previsao=index,  # Definindo o índice da linha como posicao_previsao
                        created_by = request.user
                    )
                    trem.save()
                    
                    trem_dict = model_to_dict(trem)
                    trem_dict['ID'] = trem.id

                    navegacao = NAVEGACAO_DESCARGA(trem_dict['terminal'], trem_dict['ferrovia'], trem_dict['mercadoria'], DIA_ANTERIOR=True)
                    navegacao.EDITAR_TREM(trem_dict, "INSERIR")

                    
                return redirect('configuracao')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

#endregion



#region RESTRICOES
@login_required

def carregar_restricoes(request, restricao_form, tipo_formulario):

    restricoes = Restricao.objects.all()

    return render(request, 'RESTRICOES.html', {'RESTRICOES': restricoes, 'FORMULARIO': restricao_form, "TIPO_FORMULARIO": tipo_formulario})

def restricoes_view(request):

    restricao_form  = RestricaoForm()
    tipo_formulario = None

    return carregar_restricoes(request, restricao_form, tipo_formulario)

def criar_restricao_view(request):
    
    if request.method == 'POST':
        
        resultado = Restricao.criar_restricao(request.POST, request.user)
        
        if resultado["status"]: 
            
            return redirect('restricao')
        
        else:

            if resultado["descricao"]:  messages.error(request, resultado["descricao"])
            if resultado["errors"]:     messages.error(request, resultado["errors"])

            return carregar_restricoes(request, resultado["form"], "CRIAR")

    else: return redirect('restricao')
   
@login_required
def excluir_restricao_view(request, id):

    restricao = get_object_or_404(Restricao, pk=id)
    
    try: restricao.excluir_restricao() 
    except Exception as e:  pass

    return redirect('restricao')

def restricao(request):

    FORMULARIO = RestricaoForm()
    RESTRICOES = Restricao.objects.all()

    if request.method == 'POST':
        TIPO_FORMULARIO = request.POST.get('TIPO_FORMULARIO')
        
        if TIPO_FORMULARIO == "CRIAR":
            with transaction.atomic():
                FORM_NOVA_RESTRICAO = RestricaoForm(request.POST)
                
                if FORM_NOVA_RESTRICAO.is_valid():


                    NOVA_RESTRICAO = FORM_NOVA_RESTRICAO.cleaned_data
                    VALIDAR = VALIDAR_RESTRICAO(NOVA_RESTRICAO)

                    if VALIDAR["STATUS"] == False:
                        messages.error(request, VALIDAR["DESCRICAO"])
                        return render(request, 'RESTRICOES.html', {'RESTRICOES': RESTRICOES, 'FORMULARIO': FORM_NOVA_RESTRICAO, "TIPO_FORMULARIO": TIPO_FORMULARIO})

                    try:
                        NAVEGACAO = NAVEGACAO_DESCARGA(NOVA_RESTRICAO["terminal"], None, NOVA_RESTRICAO["mercadoria"]) #RESTRICAO NAO TEM FERROVIA
                        NAVEGACAO.EDITAR_RESTRICAO(NOVA_RESTRICAO, "INSERIR")
                    except KeyError:
                        NAVEGACAO = NAVEGACAO_DESCARGA(NOVA_RESTRICAO["terminal"], None, NOVA_RESTRICAO["mercadoria"], DIA_ANTERIOR=True) #RESTRICAO NAO TEM FERROVIA
                        NAVEGACAO.EDITAR_RESTRICAO(NOVA_RESTRICAO, "INSERIR")

                    FORM_NOVA_RESTRICAO.save()

        if TIPO_FORMULARIO == "EDITAR":
            with transaction.atomic():
                
                ID_RESTRICAO_ANTIGA = request.POST.get('ID_EDICAO')

                FORM_EDICAO_RESTRICAO = RestricaoForm(request.POST)

                if FORM_EDICAO_RESTRICAO.is_valid():

                    EDICAO_RESTRICAO = FORM_EDICAO_RESTRICAO.cleaned_data
                    VALIDAR = VALIDAR_RESTRICAO(EDICAO_RESTRICAO)

                    if VALIDAR["STATUS"] == False:
                        messages.error(request, VALIDAR["DESCRICAO"])
                        return render(request, 'RESTRICOES.html', {'RESTRICOES': RESTRICOES, 'FORMULARIO': FORM_EDICAO_RESTRICAO, "TIPO_FORMULARIO": TIPO_FORMULARIO})
                    
                    
                    MODEL_RESTRICAO_ANTIGA = Restricao.objects.get(pk=ID_RESTRICAO_ANTIGA)
                    RESTRICAO_ANTIGA = model_to_dict(MODEL_RESTRICAO_ANTIGA)
                    
                    MODEL_RESTRICAO_ANTIGA.delete()

                    NAVEGACAO = NAVEGACAO_DESCARGA(RESTRICAO_ANTIGA["terminal"], None, RESTRICAO_ANTIGA["mercadoria"]) #RESTRICAO NAO TEM FERROVIA
                    NAVEGACAO.EDITAR_RESTRICAO(RESTRICAO_ANTIGA, "REMOVER")

                    try:
                        
                        NAVEGACAO = NAVEGACAO_DESCARGA(EDICAO_RESTRICAO["terminal"], None, EDICAO_RESTRICAO["mercadoria"]) #RESTRICAO NAO TEM FERROVIA
                        NAVEGACAO.EDITAR_RESTRICAO(EDICAO_RESTRICAO, "INSERIR")

                    except KeyError:

                        NAVEGACAO = NAVEGACAO_DESCARGA(EDICAO_RESTRICAO["terminal"], None, EDICAO_RESTRICAO["mercadoria"], DIA_ANTERIOR=True) #RESTRICAO NAO TEM FERROVIA
                        NAVEGACAO.EDITAR_RESTRICAO(EDICAO_RESTRICAO, "INSERIR")

                    

                    FORM_EDICAO_RESTRICAO.save()
            
            return render(request, 'RESTRICOES.html', {'RESTRICOES': RESTRICOES, 'FORMULARIO': FORM_EDICAO_RESTRICAO, "TIPO_FORMULARIO": TIPO_FORMULARIO})

    return render(request, 'RESTRICOES.html', {'RESTRICOES': RESTRICOES, 'FORMULARIO': FORMULARIO})

@login_required
def editar_restricao(request, id):

    #ESTA ENVIANDO A EDICAO
    if request.method == 'POST':
        FORMULARIO = RestricaoForm(request.POST)    
        if FORMULARIO.is_valid():
            
            print(FORMULARIO.cleaned_data)

        else:

            messages.error(request, FORMULARIO.errors)
            return redirect('restricao')

    #ABRINDO O FORMULARIO DE EDICAO
    else:

        RESTRICAO = get_object_or_404(Restricao, pk=id)
        
        # Cria um dicionário com os dados do trem
        DADOS_RESTRICAO = {
            "mercadoria":      RESTRICAO.mercadoria,
            "terminal":        RESTRICAO.terminal,
            "comeca_em":       RESTRICAO.comeca_em.strftime('%Y-%m-%d %H:%M'),
            "termina_em":      RESTRICAO.termina_em.strftime('%Y-%m-%d %H:%M'),
            "porcentagem":     RESTRICAO.porcentagem,
            "motivo":          RESTRICAO.motivo,
            "comentario":      RESTRICAO.comentario

        }
        
        # Retorna os dados como JSON
        return JsonResponse(DADOS_RESTRICAO)

#endregion


@login_required
def detalhe(request):

    RELATORIO = CARREGAR_RELATORIO_DETALHE()

    return render(request, 'RELATORIO_DETALHE.html', {"RELATORIO": RELATORIO})

@login_required
def configuracao(request):

    FORM_CSV = UploadFileForm()
    
    if request.method == 'POST':
        
        ACAO = request.POST.get('ACAO', 0)

        if      ACAO == "DESCARGAS_ATIVAS":

            PARAMETROS = {
                "NOVO_VALOR":   request.POST.get('novo_valor',  0),
                "LINHA":        request.POST.get('linha',       0),
                "COLUNA":       request.POST.get('coluna',      0),
                "TABELA":       request.POST.get('tabela',      0),
            }

            return HttpResponse(EDITAR_PARAMETROS(PARAMETROS))

        elif    ACAO == "SUBIDAS_ATIVAS":

            PARAMETROS = {
                "NOVO_VALOR":   request.POST.get('NOVO_VALOR', 0),
                "FERROVIA":     request.POST.get('FERROVIA'  , 0),
                "TERMINAL":     request.POST.get('TERMINAL'  , 0)
            }

            return HttpResponse(EDITAR_PARAMOS_SUBIDAS(PARAMETROS))
        
        elif    ACAO == "PXO":

            PARAMETROS = {
                "NOVO_VALOR":   request.POST.get('NOVO_VALOR', 0),
                "TIPO":         request.POST.get('TIPO'  , 0),
                "TERMINAL":     request.POST.get('TERMINAL'  , 0)
            }

            return HttpResponse(EDITAR_PARAMOS_PXO(PARAMETROS))

        elif    ACAO == "ATUALIZAR_DESCARGA":

            ATUALIZAR_DESCARGA()

            return HttpResponse("FUNCAO OK")
        
        elif    ACAO == "INSERIR_DADOS_OFFLINE":
            
            FORM = UploadFileForm(request.POST, request.FILES)
            if FORM.is_valid():
                    
                ARQUIVO = TextIOWrapper(request.FILES['file'].file, encoding=request.encoding)
                JSON    = json.load(ARQUIVO)
                lerDados(JSON, request.user)

       

    TERMIANIS_ATIVOS = ABRIR_TERMINAIS_ATIVOS()

    if request.method == 'GET':
        print(request)
        ACAO = request.GET.get('ACAO', 0)

        if  ACAO == "BAIXAR_PLANILHA":

            DONWLOAD_STATUS = BAIXAR_PLANILHA(request.user)

            JsonResponse(DONWLOAD_STATUS)

        elif  ACAO == "BAIXAR_DETALHE":

            DONWLOAD_STATUS = BAIXAR_DETALHE()

            JsonResponse(DONWLOAD_STATUS)
        
        elif  ACAO == "GERAR_DADOS_OFFLINE":

            BAIXAR_DADOS()

    return render(request, 'configuracao.html', {'terminais_ativos': TERMIANIS_ATIVOS, "FORM_CSV": FORM_CSV})

@login_required
def programacao_subida(request):
    
    if request.method == 'POST':

        REQUISICAO  = dict(request.POST) 

        if "ACAO" in REQUISICAO: 

            ACAO = REQUISICAO["ACAO"][0]
            
            if ACAO ==  "EDITAR_SALDO_VIRADA_TERMINAL": 
                
                #AQUI PARA PODER AGILIZAR A ENTREGA, TAMBÉM ENVIA SALDO DE VIRADA DA LINHA 4K TERMINAL = L4K    
                
                PARAMETROS = {

                    "TERMINAL":     REQUISICAO["TERMINAL"][0],
                    "SEGMENTO":     REQUISICAO["SEGMENTO"][0],
                    "FERROVIA":     REQUISICAO["FERROVIA"][0],
                    "NOVO_VALOR":   REQUISICAO["NOVO_VALOR"][0]

                }
                
                EDITAR_SALDO_VIRADA_TERMINAL(PARAMETROS)
                SUBIDA_DE_VAZIOS().ATUALIZAR()

            if ACAO == "CRIAR_TREM_SUBIDA":
                
                FORM_NOVO_TREM = TremVazioForm(request.POST)
                
                if FORM_NOVO_TREM.is_valid():

                    PARAMETROS = {

                        "PREFIXO"       : REQUISICAO['prefixo'][0],
                        "FERROVIA"      : REQUISICAO['ferrovia'][0],
                        "HORA"          : REQUISICAO['HORA'][0],
                        "MARGEM"        : REQUISICAO['MARGEM'][0],
                        "DIA_LOGISTICO" : REQUISICAO['DIA_LOGISTICO'][0],
                        "QT_GRAOS"      : REQUISICAO['qt_graos'][0],
                        "QT_FERTI"      : REQUISICAO['qt_ferti'][0],
                        "QT_CELUL"      : REQUISICAO['qt_celul'][0],
                        "QT_ACUCA"      : REQUISICAO['qt_acuca'][0],
                        "QT_CONTE"      : REQUISICAO['qt_contei'][0],

                    }

                    NOVO_TREM        = FORM_NOVO_TREM.save(commit=False)
                    NOVO_TREM.margem = PARAMETROS["MARGEM"]

                    PERIODO_VIGENTE     = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
                    LINHA               = PERIODO_VIGENTE[PERIODO_VIGENTE['NM_DIA'] == PARAMETROS["DIA_LOGISTICO"]]
                    DATA_ARQ            = LINHA['DATA_ARQ'].values[0]

                    DATA = datetime.strptime(DATA_ARQ, "%Y-%m-%d")
                    HORA = time(int(PARAMETROS["HORA"]), 0)
                    NOVO_TREM.previsao = datetime.combine(DATA, HORA)

                    NOVO_TREM.save()
                    Condensados().inserirTrem(PARAMETROS)

                else:

                    messages.error(request, FORM_NOVO_TREM.errors)

            if ACAO == "EDITAR_BUFFER":

                PARAMETROS = {
                    "HORA"          : REQUISICAO["HORA"][0],
                    "MARGEM"        : REQUISICAO["MARGEM"][0],
                    "FERROVIA"      : REQUISICAO["FERROVIA"][0],
                    "NOVO_VALOR"    : REQUISICAO["NOVO_VALOR"][0],
                    "DIA_LOGISTICO" : REQUISICAO["DIA_LOGISTICO"][0]
                }

                EDITAR_BUFFER(PARAMETROS)
                SUBIDA_DE_VAZIOS().ATUALIZAR()

            if ACAO == "EDITAR_SALDO_CONDENSADOS":

                PARAMETROS = {

                    "MARGEM"        : REQUISICAO["MARGEM"][0],
                    "SEGMENTO"      : REQUISICAO["SEGMENTO"][0],
                    "FERROVIA"      : REQUISICAO["FERROVIA"][0],
                    "NOVO_VALOR"    : REQUISICAO["NOVO_VALOR"][0]
                    
                }
                EDITAR_SALDO_CONDENSADO(PARAMETROS)
                SUBIDA_DE_VAZIOS().ATUALIZAR()
            
            if ACAO == "ATUALIZAR_SUBIDA":
                SUBIDA_DE_VAZIOS().ATUALIZAR()
   
    
    TABELAS_SUBIDA = CARREGAR_PROG_SUBIDA()
    FORM_NOVO_TREM = TremVazioForm()
    
    return render(request, 'OPERACAO/PROG_SUBIDA.html', {"TABELAS_SUBIDA": TABELAS_SUBIDA, "FORM": FORM_NOVO_TREM})

@login_required
def editar_trem_subida(request, id):

    TREM = TremVazio.objects.get(pk=id)
    FORM = TremVazioForm(instance=TREM)

    TABELAS = CARREGAR_PREVISAO_SUBIDA()

    return render(request, 'OPERACAO/PREVISAO_SUBIDA.html', {'form': FORM, "TABELAS": TABELAS, 'MODAL_OPEN': True})

@login_required
def ocupacao_terminais(request):
  
    REQUISICAO = REQUEST_PARA_DICT(request)
    

    if "ACAO" in  REQUISICAO:
        
        ACAO = REQUISICAO["ACAO"][0]

        if ACAO == "VIZUALIZAR_DESCARGA":

            if REQUISICAO["TERMINAL"][0] == "MOEGA X" or REQUISICAO["TERMINAL"][0] == "MOEGA V":

                DESCARGA = DESCARGA_HTML("MOEGA X", REQUISICAO["DIA_LOGISTICO"][0]) + "<tr><td colspan=29 class='pula__linha'>.</td></tr>"
                DESCARGA = DESCARGA + DESCARGA_HTML("MOEGA V", REQUISICAO["DIA_LOGISTICO"][0])
                
                return HttpResponse(DESCARGA) 
            
            else:

                DESCARGA = DESCARGA_HTML(REQUISICAO["TERMINAL"][0], REQUISICAO["DIA_LOGISTICO"][0])
                return HttpResponse(DESCARGA)

    else:

        #CARREGA A PAGINA
        RELATORIO = CARREGAR_RELATORIO_OCUPACAO()
        return render(request, 'RELATORIO_OCUPACAO.html', {"RELATORIO": RELATORIO}) 

@login_required
def previsao_subida(request):
    
    MODAL_OPEN = False

    form = TremVazioForm()
    
    if request.method == 'POST': 
        
        REQUISICAO  = dict(request.POST) 
        ACAO        = REQUISICAO["ACAO"][0]

        if ACAO == "CRIAR_TREM":

            with transaction.atomic():
                
                FORM_NOVO_TREM = TremVazioForm(request.POST)
                
                if FORM_NOVO_TREM.is_valid():

                    FORM_NOVO_TREM.save()

                else:

                    messages.error(request, FORM_NOVO_TREM.errors)  

        if ACAO == "EDITAR_TREM":  

            with transaction.atomic():
                
                ID_TREM = REQUISICAO["ID_TREM"][0]

                FORM_NOVO_TREM = TremVazioForm(request.POST) 
                if FORM_NOVO_TREM.is_valid():

                    TREM_ANTIGO = TremVazio.objects.get(pk=ID_TREM) 
                    TREM_ANTIGO.delete()

                    FORM_NOVO_TREM.save()
                    
        if ACAO == "EXCLUIR_TREM": 

            ID_TREM = REQUISICAO["ID_TREM"][0]
            TREM_ANTIGO = TremVazio.objects.get(pk=ID_TREM) 

            DATA_ARQ = TREM_ANTIGO.previsao.strftime("%Y-%m-%d")
            try:
                PERIODO_VIGENTE     = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
                LINHA               = PERIODO_VIGENTE[PERIODO_VIGENTE['DATA_ARQ'] == DATA_ARQ]
                DIA_LOGISTICO       = LINHA['NM_DIA'].values[0]
                
                PARAMETROS = {

                            "PREFIXO"       : 0,
                            "FERROVIA"      : TREM_ANTIGO.ferrovia,
                            "HORA"          : TREM_ANTIGO.previsao.hour,
                            "MARGEM"        : TREM_ANTIGO.margem,
                            "DIA_LOGISTICO" : DIA_LOGISTICO,
                            "QT_GRAOS"      : 0,
                            "QT_FERTI"      : 0,
                            "QT_CELUL"      : 0,
                            "QT_ACUCA"      : 0,
                            "QT_CONTE"      : 0,

                }
                
                Condensados().inserirTrem(PARAMETROS)

            except IndexError:
                pass
                

            
            TREM_ANTIGO.delete()

    elif request.method == 'GET': 

        REQUISICAO  = dict(request.GET)

        if "ACAO" in REQUISICAO: 

            ACAO = REQUISICAO["ACAO"][0]

            if ACAO == "ACESSAR_TREM":

                ID_TREM = REQUISICAO["ID_TREM"][0]
                
                TREM = TremVazio.objects.get(pk=ID_TREM)
                TREM = model_to_dict(TREM)
                TREM["previsao"] = TREM["previsao"].strftime('%Y-%m-%d %H:%M')

                return JsonResponse(TREM)

    TABELAS = CARREGAR_PREVISAO_SUBIDA()

    return render(request, 'OPERACAO/PREVISAO_SUBIDA.html', {'form': form, "TABELAS": TABELAS, 'MODAL_OPEN': MODAL_OPEN})