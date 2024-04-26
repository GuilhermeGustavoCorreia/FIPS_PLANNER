from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts               import redirect
from django.urls                    import reverse
from django.forms.models            import model_to_dict

from django.db import transaction

from .models        import Trem, Restricao
from .forms         import TremForm, RestricaoForm
from django.contrib import messages

from    previsao_trens.packages.CONFIGURACAO.CARREGAR_PAGINA    import ABRIR_TERMINAIS_ATIVOS
from    previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS  import EDITAR_PARAMETROS
from    previsao_trens.packages.CONFIGURACAO.ATUALIZAR_DESCARGA import ATUALIZAR_DESCARGA

from    previsao_trens.packages.CRIAR_TREM.VALIDAR           import VALIDAR_NOVA_PREVISAO, VALIDAR_EDICAO_PREVISAO, VALIDAR_DIVISAO_PREVISAO
from    previsao_trens.packages.CRIAR_TREM.CARREGAMENTOS     import CARREGAR_PREVISOES
from    previsao_trens.packages.CRIAR_TREM.ATUALIZAR_POSICAO import AJUSTAR_POSICAO_CHEGADA
import previsao_trens.packages.descarga.CARREGAR_PAGINA as CARREGAR_DESCARGA

from    previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as NAVEGACAO_DESCARGA

import json

def redirect_to_login(request):
    
    return redirect(reverse('login'))

@login_required
def navegacao(request):

    if request.method == 'POST':
        with transaction.atomic():
            
            
            REQUISICAO =  dict(request.POST)

            PARAMETROS = {
                'TERMINAL'  :   REQUISICAO['TERMINAL'][0], 
                'DATA_ARQ'  :   REQUISICAO['DATA_ARQ'][0], 
                'PRODUTO'   :   REQUISICAO['PRODUTO'][0], 
                'FERROVIA'  :   REQUISICAO['FERROVIA'][0], 
                'CELULAS'   :   [int(valor) for valor in REQUISICAO['CELULAS[]']] , 
                'VALOR'     :   int(REQUISICAO['VALOR'][0]), 
               
            }

            print(PARAMETROS)
            Descarga = NAVEGACAO_DESCARGA(PARAMETROS["TERMINAL"], PARAMETROS["FERROVIA"], PARAMETROS["PRODUTO"]) 
            Descarga.EDITAR_PRODUTIVIDADE(PARAMETROS)

    DESCARGAS = CARREGAR_DESCARGA.PAGINA_COMPLETA()
    return render(request, 'navegacao.html', {"descargas": DESCARGAS})

@login_required
def profile(request):

    return render(request, 'user/profile.html')

#region PAGINA CRIAR TREM
@login_required
def criar_trem(request):

    form = TremForm()  # Instancia um formulário vazio para ser usado no modal
    
    TABELAS = CARREGAR_PREVISOES()

    return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': form})

@login_required
def novo_trem_previsao(request):
    
    TABELAS = CARREGAR_PREVISOES()
    form = TremForm()
    if request.method == 'POST':

        with transaction.atomic():

            #ABSTRAINDO OS DADOS DO NOVO TREM
            FORM_NOVO_TREM = TremForm(request.POST)
            FORM_NOVO_TREM.posicao_previsao = 0
    
            #VALIDAR O TREM NA DESCARGA
            if FORM_NOVO_TREM.is_valid(): 

                #VALIDAR
                #1. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL (É O MESMO TREM?)
                #2. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)

                NOVO_TREM = FORM_NOVO_TREM.cleaned_data

                CRITERIOS_AVALIADOS = VALIDAR_NOVA_PREVISAO(NOVO_TREM)

                if CRITERIOS_AVALIADOS["STATUS"] == False:

                    messages.error(request, CRITERIOS_AVALIADOS["DESCRICAO"])
                    return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': form})

                AJUSTAR_POSICAO_CHEGADA(ACAO="INSERIR TREM",TREM=NOVO_TREM)
                FORM_NOVO_TREM.save()

                NAVEGACAO = NAVEGACAO_DESCARGA(NOVO_TREM["terminal"], NOVO_TREM["ferrovia"], NOVO_TREM["mercadoria"]) #4
                NAVEGACAO.EDITAR_TREM(NOVO_TREM, "INSERIR")

                TABELAS = CARREGAR_PREVISOES()

                messages.success(request, 'Trem adicionado com sucesso!')
                return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': form})  

            else:
                messages.error(request, NOVO_TREM.errors)
    else:

        form = TremForm()
    return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS,  'form': form})

@login_required
def excluir_trem(request, id):

    # Tenta encontrar o trem pelo ID e excluí-lo.
    # CUIDADO AO EXCLUIR UM TREM QUE NÃO ESTA NA DESCARGA

    try:
        with transaction.atomic():
            trem = Trem.objects.get(pk=id)
            
            trem.delete()
            
            TREM_ANTIGO = model_to_dict(trem)

            NAVEGACAO = NAVEGACAO_DESCARGA(TREM_ANTIGO["terminal"], TREM_ANTIGO["ferrovia"], TREM_ANTIGO["mercadoria"]) #5
            NAVEGACAO.EDITAR_TREM(TREM_ANTIGO, "REMOVER")
            
            POSICAO_TREM  = trem.posicao_previsao
            PREVISAO_TREM = trem.previsao.date()

            AJUSTAR_POSICAO_CHEGADA(ACAO="EXLUIR TREM", PREVISAO_TREM_EXCLUIDO=PREVISAO_TREM, POSICAO=POSICAO_TREM)

            messages.success(request, 'Trem excluído com sucesso!')

    except Trem.DoesNotExist:

        messages.error(request, 'Trem não encontrado.')
    
    # Redireciona para a página da lista de trens.
    return redirect('criar_trem')

@login_required
def editar_trem(request, trem_id):

    TABELAS = CARREGAR_PREVISOES()

    #ESTA ENVIANDO A EDICAO
    if request.method == 'POST':
        form = TremForm(request.POST)

        if form.is_valid():
            
            #VALIDANDO SE NOVO TREM ATENDE CRITÉRIOS
            CRITERIOS_AVALIADOS = VALIDAR_EDICAO_PREVISAO(form.cleaned_data, trem_id)
            if not CRITERIOS_AVALIADOS["STATUS"]:

                messages.error(request, CRITERIOS_AVALIADOS["DESCRICAO"])
                return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': form})

            # Remover o trem antigo após capturar posição
            TREM_ANTIGO = Trem.objects.get(pk=trem_id)        
            NOVO_TREM   = form.save(commit=False)
       
            NOVO_TREM.posicao_previsao = AJUSTAR_POSICAO_CHEGADA(ACAO="EDITAR TREM", TREM_ANTIGO = TREM_ANTIGO, NOVO_TREM=NOVO_TREM)
            
            #ISSO TEM QUE SER AS ULTIMAS COISAS A SE FAZER
            TREM_ANTIGO.delete()
            NOVO_TREM.save()

            #EDITANDO NA DESCARGA
            NAVEGACAO_A = NAVEGACAO_DESCARGA(TREM_ANTIGO["terminal"], TREM_ANTIGO["ferrovia"], TREM_ANTIGO["mercadoria"])
            NAVEGACAO_A.EDITAR_TREM(model_to_dict(TREM_ANTIGO), "REMOVER")

            NAVEGACAO_B = NAVEGACAO_DESCARGA(NOVO_TREM["terminal"], NOVO_TREM["ferrovia"], NOVO_TREM["mercadoria"])
            NAVEGACAO_B.EDITAR_TREM(model_to_dict(NOVO_TREM), "INSERIR")

            messages.success(request, "Trem editado com sucesso.")
            return redirect('criar_trem')
        else:
            messages.error(request, form.errors)
            return render(request, 'previsao/criar_trem.html', {'TABELAS': TABELAS, 'form': form})
    
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

        #PRIMEIRO VAMOS DEFINIR AS POSICOES DE CADA ELEMENTO DIVIDIDO

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

            print(f"POSICOES: { POSICOES }")

            TREM_01.posicao_previsao = POSICOES["POSICAO_01"]
            TREM_02.posicao_previsao = POSICOES["POSICAO_02"]

            TREM_ORIGINAL.delete()

            TREM_01.save()
            TREM_02.save()

            #EDITANDO NA DESCARGA
            NAVEGACAO_A = NAVEGACAO_DESCARGA(TREM_ORIGINAL["terminal"], TREM_ORIGINAL["ferrovia"], TREM_ORIGINAL["mercadoria"]) #1
            NAVEGACAO_A.EDITAR_TREM(model_to_dict(TREM_ORIGINAL), "REMOVER")

            NAVEGACAO_B = NAVEGACAO_DESCARGA(TREM_01["terminal"], TREM_01["ferrovia"], TREM_01["mercadoria"]) #2
            NAVEGACAO_B.EDITAR_TREM(model_to_dict(TREM_01), "INSERIR")

            NAVEGACAO_C = NAVEGACAO_DESCARGA(TREM_02["terminal"], TREM_02["ferrovia"], ["mercadoria"]) #3
            NAVEGACAO_C.EDITAR_TREM(model_to_dict(TREM_02), "INSERIR")

        else: 

            return JsonResponse({'error': 'Dados inválidos'}, status=400)

        return redirect("criar_trem")

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
#endregion

@login_required
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

                    NAVEGACAO = NAVEGACAO_DESCARGA(NOVA_RESTRICAO["terminal"], None, NOVA_RESTRICAO["mercadoria"]) #RESTRICAO NAO TEM FERROVIA
                    NAVEGACAO.EDITAR_RESTRICAO(NOVA_RESTRICAO, "INSERIR")

                    FORM_NOVA_RESTRICAO.save()

    return render(request, 'RESTRICOES.html', {'RESTRICOES': RESTRICOES, 'FORMULARIO': FORMULARIO})

@login_required
def excluir_restricao(request, id):

    with transaction.atomic():
        
        RESTRICAO = Restricao.objects.get(pk=id)

        RESTRICAO.delete()
            
        RESTRICAO_ANTIGA = model_to_dict(RESTRICAO)
        print(RESTRICAO_ANTIGA)
        NAVEGACAO = NAVEGACAO_DESCARGA(RESTRICAO_ANTIGA["terminal"], None, RESTRICAO_ANTIGA["mercadoria"]) #RESTRICAO NAO TEM FERROVIA
        NAVEGACAO.EDITAR_RESTRICAO(RESTRICAO_ANTIGA, "REMOVER")

        return redirect('restricao')


@login_required
def configuracao(request):

    if request.method == 'POST':
        
        ACAO = request.POST.get('ACAO', 0)

        if ACAO == "EDITAR_CONFIGURACAO":

            PARAMETROS = {
                "NOVO_VALOR":   request.POST.get('novo_valor',  0),
                "LINHA":        request.POST.get('linha',       0),
                "COLUNA":       request.POST.get('coluna',      0),
                "TABELA":       request.POST.get('tabela',      0),
            }


            return HttpResponse(EDITAR_PARAMETROS(PARAMETROS))

        if ACAO == "ATUALIZAR_DESCARGA":

            ATUALIZAR_DESCARGA()

            return HttpResponse("FUNCAO OK")
        
    TERMIANIS_ATIVOS = ABRIR_TERMINAIS_ATIVOS()



    return render(request, 'configuracao.html', {'terminais_ativos': TERMIANIS_ATIVOS})