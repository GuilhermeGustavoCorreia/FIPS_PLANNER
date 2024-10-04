
from django.shortcuts               import render, get_object_or_404, redirect
from django.http                    import HttpResponse, JsonResponse, Http404, QueryDict
from django.contrib                 import messages
from django.contrib.auth            import login as auth_login
from django.contrib.auth.forms      import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.urls                    import reverse
from django.forms.models            import model_to_dict
from django.db                      import transaction

from tempfile import NamedTemporaryFile


from .models                    import Trem, Restricao, TremVazio, Terminal, Mercadoria
from .forms                     import UploadFileForm, TremForm, RestricaoForm, TremVazioForm, CustomAuthenticationForm, TerminalForm, DividirTremForm
from .serializers               import TremSerializer, TremSerializerToSend
from rest_framework             import status, generics
from rest_framework.views       import APIView
from rest_framework.response    import Response

from    previsao_trens.packages.CONFIGURACAO.CARREGAR_PAGINA                        import ABRIR_TERMINAIS_ATIVOS
from    previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS                      import EDITAR_PARAMETROS, EDITAR_PARAMOS_SUBIDAS, EDITAR_PARAMOS_PXO, EDITAR_PARAMETROS_RESTRICAO
from    previsao_trens.packages.CONFIGURACAO.ATUALIZAR_DESCARGA                     import ATUALIZAR_DESCARGA
from    previsao_trens.packages.CONFIGURACAO.EXPORTAR_PLANILHA                      import gerar_planilha, gerar_planilha_antiga
from    previsao_trens.packages.CONFIGURACAO.BAIXAR_DETALHE                         import gerar_planilha_detalhe
from    previsao_trens.packages.CONFIGURACAO.INTEGRACAO_PLANNER_OFFLINE_GERAR       import dados_integracao
from    previsao_trens.packages.CONFIGURACAO.INTEGRACAO_PLANNER_OFFLINE_LER         import lerDados
import  previsao_trens.packages.descarga.CARREGAR_PAGINA                                                        as CARREGAR_DESCARGA
from    previsao_trens.packages.descarga.EDITAR_DESCARGA                            import NAVEGACAO_DESCARGA   as NAVEGACAO_DESCARGA
from    previsao_trens.packages.PROG_SUBIDA.CARREGAR_PAGINA                         import CARREGAR_PROG_SUBIDA
from    previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2                      import SUBIDA_DE_VAZIOS, EDITAR_SALDO_VIRADA_TERMINAL, EDITAR_BUFFER, EDITAR_SALDO_CONDENSADO
from    previsao_trens.packages.DETELHE.CARREGAR_PAGINA                             import CARREGAR_RELATORIO_DETALHE
from    previsao_trens.packages.RELATORIO_OCUPACAO.CARREGAR_PAGINA                  import CARREGAR_RELATORIO_OCUPACAO
from    previsao_trens.packages.RELATORIO_OCUPACAO.carregar_totais_detalhe          import  totais_detalhe
from    previsao_trens.packages.RELATORIO_OCUPACAO.DESCARGA_HTML                    import DESCARGA_HTML
from    previsao_trens.packages.RESTRICAO.VALIDAR                                   import VALIDAR_RESTRICAO

import  os
from    io          import TextIOWrapper
from    datetime    import datetime
import  json
import  csv
import  pandas as pd

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

@login_required
def editar_encoste(request):

    if request.method == 'POST':
        with transaction.atomic():  

            terminal    = request.POST.get('terminal', 0)
            ferrovia    = request.POST.get('ferrovia', 0)
            mercadoria  = request.POST.get('mercadoria', 0)
            
            hora = int(request.POST.get('hora', 0))
            

            try: 
                novo_valor  = int(request.POST.get('novo_valor', 0))
            except ValueError : 
                novo_valor  = 0
            data_arq    = request.POST.get('data_arq', 0)
 
            Descarga = NAVEGACAO_DESCARGA(terminal, ferrovia, mercadoria)
            descargas_atualizadas = Descarga.editar_encoste(hora, novo_valor, data_arq)

            return JsonResponse(descargas_atualizadas, safe=False)

#endregion

def custom_login_view(request):

    if request.user.is_authenticated:
        
        return redirect('navegacao')
    
    if request.method == 'POST':
        
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():

            auth_login(request, form.get_user())
            return redirect('navegacao')
        
    else:

        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})

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
                previsao__day=DATA.day,
                translogic=False

            ).order_by('posicao_previsao')
            if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
                tabelas_de_previsoes[linha['NM_DIA']] = queryset
    
    trens_sem_previsao = Trem.objects.filter(previsao__isnull=True, translogic=False).order_by('posicao_previsao')
    
    if trens_sem_previsao.exists():tabelas_de_previsoes["SEM PREVISÃO"] = trens_sem_previsao

    return tabelas_de_previsoes

def carregar_previsao_trens(request, trem_form, tipo_formulario):

    context = {'TABELAS': carregar_tabela_de_previsoes(), 'form': trem_form, "TIPO_FORMULARIO": tipo_formulario}

    return render(request, 'previsao/criar_trem.html', context)

@login_required
def previsao_trens_view(request):
    
    trem_form            = TremForm()
    tipo_formulario      = None
    
    return carregar_previsao_trens(request, trem_form, tipo_formulario)

@login_required
def criar_trem_view(request):
    
    if request.method == 'POST':    
        
        form = TremForm(request.POST)
        
        if form.is_valid():

            trem  = form.save(commit=False)
            trem.created_by = request.user
            trem.save()

            return redirect('previsao_trens')
        
        else:

            tipo_formulario = "criar_trem"
            trem_form = TremForm(request.POST)   
            messages.error(request, form.errors) 
            return carregar_previsao_trens(request, trem_form, tipo_formulario)
    
    else: 
        
        return redirect('previsao_trens')

@login_required
def excluir_trem_view(request, id):
    
    try:
        
        trem = Trem.objects.get(pk=id)
        trem.delete()
   
    except Trem.DoesNotExist:
     
        pass

    return redirect('previsao_trens')
   
@login_required
def editar_trem(request, trem_id):

    tipo_formulario = "editar_trem"
    trem = get_object_or_404(Trem, pk=trem_id)

    if request.method == 'POST':
        
        with transaction.atomic():

            form = TremForm(request.POST, instance=trem) #considera o trem em edição

            if form.is_valid():

                trem  = form.save(commit=False)
                trem.created_by = request.user
                trem.save()

                return redirect('previsao_trens')
            
            else:

                trem_form = TremForm(request.POST)   
                messages.error(request, form.errors) 
                return carregar_previsao_trens(request, trem_form, tipo_formulario)
    
    else:
        

        trem.previsao = trem.previsao.strftime('%Y-%m-%dT%H:%M') if trem.previsao else None
        trem_form = TremForm(instance=trem)
         
    return carregar_previsao_trens(request, trem_form, tipo_formulario)

@login_required
def dividir_trem(request, trem_id):
    
    tipo_formulario = "dividir_trem"
    trem            = get_object_or_404(Trem, pk=trem_id)

    if request.method == 'POST':
        
        form = DividirTremForm(request.POST)

        if form.is_valid():

            data1 = {
                'prefixo'   : trem.prefixo,
                'os'        : trem.os,
                'origem'    : trem.origem,
                'local'     : trem.local,
                'destino'   : form.cleaned_data['destino1'],
                'mercadoria': form.cleaned_data['mercadoria1'],
                'terminal'  : form.cleaned_data['terminal1'],
                'vagoes'    : form.cleaned_data['vagoes1'],
                'previsao'  : form.cleaned_data['previsao1'],
                'ferrovia'  : trem.ferrovia
            }
            data2 = {
                'prefixo'   : trem.prefixo,
                'os'        : trem.os,
                'origem'    : trem.origem,
                'local'     : trem.local,
                'destino'   : form.cleaned_data['destino2'],
                'mercadoria': form.cleaned_data['mercadoria2'],
                'terminal'  : form.cleaned_data['terminal2'],
                'vagoes'    : form.cleaned_data['vagoes2'],
                'previsao'  : form.cleaned_data['previsao2'],
                'ferrovia'  : trem.ferrovia
            }

            trem.to_slice(data1, data2)
            
            return redirect('previsao_trens')
        
        else:

            trem_form = DividirTremForm(request.POST)   
            messages.error(request, form.errors) 
            print(form.errors)
            return carregar_previsao_trens(request, trem_form, tipo_formulario)
        
    else:

        trem_form = DividirTremForm(instance=trem)
       
        return carregar_previsao_trens(request, trem_form, tipo_formulario)

@login_required
def excluir_dia_inteiro(request, dia_logistico):

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    periodo_vigente      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
   
    data_arq             = periodo_vigente[periodo_vigente['NM_DIA'] == dia_logistico].iloc[0]['DATA_ARQ']
    data                 = datetime.strptime(data_arq, '%Y-%m-%d')

    trens = Trem.objects.filter(previsao__year=data.year, previsao__month=data.month, previsao__day=data.day).order_by('posicao_previsao')
    
    if trens.exists(): 
        
        for trem in trens:

            trem.delete()

    return redirect('previsao_trens')

#region ajax
@login_required
def alterar_posicao_view(request):
 
    id_trem      = request.POST.get('trem')
    new_position = int(request.POST.get('new_position'))
    
    with transaction.atomic():

        trem = Trem.objects.get(pk=id_trem)
        trem.update_position(new_position)   

        return JsonResponse({'status': 'success', 'message': 'Posição atualizada com sucesso!'})

def get_terminals(request):

    mercadoria_id   = request.GET.get('mercadoria')
    mercadoria      = Mercadoria.objects.get(id=mercadoria_id)
    terminais       = Terminal.objects.filter(segmento=mercadoria.segmento).values('id', 'nome')
   
    return JsonResponse(list(terminais), safe=False)

#endregion

class APITremCreateView(APIView): 
    
    def post(self, request):
        
        Trem.objects.filter(translogic=True).delete()
    
        if isinstance(request.data, list):
            
            # Caso seja uma lista de objetos
            serializer = TremSerializer(data=request.data, many=True)
        else:
            
            # Caso seja um único objeto
            serializer = TremSerializer(data=request.data)
        
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APITremList(generics.ListAPIView):
    
    queryset         = Trem.objects.all()
    serializer_class = TremSerializerToSend

@login_required
def previsao_164_view(request):

    trens = Trem.objects.filter(previsao__isnull=True, translogic=True)

    return render(request, 'previsao_164.html', {'trens': trens})

def previsao_164_atualizar_view(request):
    
    Trem.update_nitro()

    return redirect("previsao_164")

#endregion

#region RESTRICOES

@login_required
def carregar_restricoes(request, restricao_form, tipo_formulario):

    restricoes = Restricao.objects.all()

    return render(request, 'RESTRICOES.html', {'RESTRICOES': restricoes, 'FORMULARIO': restricao_form, "TIPO_FORMULARIO": tipo_formulario})

@login_required
def restricoes_view(request):

    restricao_form  = RestricaoForm()
    tipo_formulario = None

    return carregar_restricoes(request, restricao_form, tipo_formulario)

@login_required
def criar_restricao_view(request):
    
    if request.method == 'POST':
        
        form = RestricaoForm(request.POST)

        if form.is_valid():

            restricao = form.save(commit=False)
            restricao.created_by = request.user
            restricao.save()
               
            return redirect('restricao')
        
        else:

            messages.error(request, form.errors)

            return carregar_restricoes(request, form, "CRIAR")

    else: 
        return redirect('restricao')
   
@login_required
def excluir_restricao_view(request, id):
 
    try: 

        restricao = Restricao.objects.get(pk=id)
        restricao.excluir_restricao() 

    except Restricao.DoesNotExist:  
        
        pass

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

    restricao = get_object_or_404(Restricao, pk=id)

    #ESTA ENVIANDO A EDICAO
    if request.method == 'POST':

        form = RestricaoForm(request.POST, instance=restricao)   

        if form.is_valid():

            restricao  = form.save(commit=False)
            restricao.created_by = request.user
            restricao.save()

        else:

            messages.error(request, form.errors)
        
        return redirect('restricao')

    #ABRINDO O FORMULARIO DE EDICAO
    else:

        # Cria um dicionário com os dados do trem
        DADOS_RESTRICAO = {
            "mercadoria":      restricao.mercadoria,
            "terminal":        restricao.terminal,
            "comeca_em":       restricao.comeca_em.strftime('%Y-%m-%d %H:%M'),
            "termina_em":      restricao.termina_em.strftime('%Y-%m-%d %H:%M'),
            "porcentagem":     restricao.porcentagem,
            "motivo":          restricao.motivo,
            "comentario":      restricao.comentario

        }
        
        # Retorna os dados como JSON
        return JsonResponse(DADOS_RESTRICAO)

#endregion

@login_required
def detalhe(request):

    RELATORIO = CARREGAR_RELATORIO_DETALHE()

    return render(request, 'RELATORIO_DETALHE.html', {"RELATORIO": RELATORIO})

#region CONFIGURACAO

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
        
        elif    ACAO == "RESTRICOES_ATIVAS":
            
            PARAMETROS = {
                "NOVO_VALOR"    : request.POST.get('novo_valor', 0),
                "MERCADORIA"    : request.POST.get('coluna'    , 0),
                "TERMINAL"      : request.POST.get('linha'     , 0)
            }

            return HttpResponse(EDITAR_PARAMETROS_RESTRICAO(PARAMETROS))
        
        elif    ACAO == "PXO":
            
            PARAMETROS = {
                "NOVO_VALOR":   request.POST.get('NOVO_VALOR', 0),
                "TIPO":         request.POST.get('TIPO'      , 0),
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

    return render(request, 'configuracao.html', {'terminais_ativos': TERMIANIS_ATIVOS, "FORM_CSV": FORM_CSV})

@login_required
def baixar_integracao_view(request):

    json_data = dados_integracao()
    
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.json"'

    return response

@login_required
def baixar_planilha_view(request):
    

    try:
        planilha_sistema = gerar_planilha(request.user)

        with NamedTemporaryFile(delete=False, suffix=".xlsm") as tmp:
            
            planilha_sistema.save(tmp.name)
            tmp.seek(0)
            
            now = datetime.now()

            response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="planilha_planner_{now.year}-{now.month}-{now.day}_{now.hour}h_{now.minute}min_{now.second}sec.xlsm"'

            tmp.close()

            try:    os.unlink(tmp.name)
            except PermissionError: pass

            return response
        
    except Exception as e:
        raise Http404(f"Erro ao baixar o arquivo: {e}")

@login_required
def baixar_planilh_antiga_view(request):
 
    try:
        
        planilha_antiga = gerar_planilha_antiga()

        with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:

            planilha_antiga.save(tmp.name)
            tmp.seek(0)

            response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename("previsao_trens/src/DICIONARIOS/Porto_Santos_2021 ajustada 2.xlsx")}'

            tmp.close()

            try:    os.unlink(tmp.name)
            except PermissionError: pass

            return response
        
    except Exception as e:
        raise Http404(f"Erro ao baixar o arquivo: {e}")
 
@login_required
def baixar_planilha_detalhe_view(request):

    try:
        planilha_detalhe = gerar_planilha_detalhe()

        with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:

            planilha_detalhe.save(tmp.name)
            tmp.seek(0)

            response = HttpResponse(tmp.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename("previsao_trens/src/DICIONARIOS/RELATORIO_DETALHE.xlsx")}'

            tmp.close()

            try:    os.unlink(tmp.name)
            except PermissionError: pass

            return response
        
    except Exception as e:

        raise Http404(f"Erro ao baixar o arquivo: {e}")

@login_required
def upload_file_view(request):

    with transaction.atomic():
     
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            file = request.FILES['file']

            TremVazio.read_excel(file, request.user)
                    
            return redirect('previsao_subida')
        
    return redirect('configuracao')

#endregion

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
    
    return render(request, 'programacao_subida.html', {"TABELAS_SUBIDA": TABELAS_SUBIDA, "FORM": FORM_NOVO_TREM})


#region RELATORIO OCUPACAO
@login_required
def ocupacao_terminais(request):
  
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        acao = request.GET.get('acao')
        
        if acao == "baixar_total_detalhe":
           
            dia_logistico = request.GET.get('dia_logistico')
    
            html_totais_relatorio_detalhe = totais_detalhe(dia_logistico)
            
            return JsonResponse({"html_totais_relatorio_detalhe": html_totais_relatorio_detalhe})

        if acao == "vizualizar_descarga":
            
            dia_logistico   = request.GET.get('dia_logistico')
            terminal        = request.GET.get('terminal')

            if terminal == "MOEGA X" or terminal == "MOEGA V":

                DESCARGA = DESCARGA_HTML("MOEGA X", dia_logistico) + "<tr><td colspan=29 class='pula__linha'>.</td></tr>"
                DESCARGA = DESCARGA + DESCARGA_HTML("MOEGA V", dia_logistico)
                
                return HttpResponse(DESCARGA) 
            
            else:

                DESCARGA = DESCARGA_HTML(terminal, dia_logistico)
                return HttpResponse(DESCARGA)

    else:

        #CARREGA A PAGINA
        RELATORIO = CARREGAR_RELATORIO_OCUPACAO()
        return render(request, 'RELATORIO_OCUPACAO.html', {"RELATORIO": RELATORIO}) 

#endregion

#region PROGRAMACAO DE SUBIDA

def carregar_tabela_de_previsoes_subida():

    trens_margem_direita  = TremVazio.objects.filter(margem='Direita').order_by('previsao')
    trens_margem_esquerda = TremVazio.objects.filter(margem='Esquerda').order_by('previsao')

    return {"direita": trens_margem_direita, "esquerda": trens_margem_esquerda}

def carregar_previsao_trem_subida(request, form, tipo_formulario):

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    periodo_vigente      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)
   
    data_arq_D           = periodo_vigente[periodo_vigente['NM_DIA'] == "D"].iloc[0]['DATA_ARQ']
    data_arq_D1          = periodo_vigente[periodo_vigente['NM_DIA'] == "D+1"].iloc[0]['DATA_ARQ']

    with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ data_arq_D }.json") as ARQUIVO:
        condensados_d = json.load(ARQUIVO)
        
    with open(f"previsao_trens/src/SUBIDA/CONDENSADOS/condensado_{ data_arq_D1 }.json") as ARQUIVO:
        condensados_d1 = json.load(ARQUIVO)
    
    previsoes = carregar_tabela_de_previsoes_subida()

    return render(request, 'previsao_subida.html', {'previsoes': previsoes, 'form': form, 'condensados': {'D': condensados_d, 'D+1': condensados_d1}, "dias": {"D": data_arq_D, "D+1": data_arq_D1}, 'tipo_formulario': tipo_formulario})

@login_required
def previsao_subida_view(request):
 
    form             = TremVazioForm()
    tipo_formulario  = None
    carregar_previsao_trem_subida(request, form, tipo_formulario)

    return carregar_previsao_trem_subida(request, form, tipo_formulario)

@login_required
def criar_trem_subida_view(request):
    
    if request.method == 'POST':

        form = TremVazioForm(request.POST)
        
        if form.is_valid():
            
            trem  = form.save(commit=False)
            trem.created_by = request.user
            trem.prefixo    = trem.prefixo.upper()
            trem.save()

            return redirect('previsao_subida')
        
        else:
            
            tipo_formulario = "criar_trem_subida"
            messages.error(request, form.errors) 
                    
            return carregar_previsao_trem_subida(request, form, tipo_formulario)
    
    else:
        
        form = TremForm()

    return redirect('previsao_subida')     

@login_required   
def excluir_trem_subida_view(request, id_trem_vazio):

    try:
        
        trem = TremVazio.objects.get(pk=id_trem_vazio)
        trem.delete()
    
    except TremVazio.DoesNotExist:
     
        pass

    return redirect('previsao_subida')

@login_required
def excluir_tabela_subida_view(request, margem):

    trens_vazios = TremVazio.objects.filter(margem=margem)
    
    if trens_vazios.exists(): 
        
        for trem_vazio in trens_vazios:

            trem_vazio.delete()

    return redirect('previsao_subida')


@login_required   
def editar_trem_subida_view(request, id_trem_vazio):
      
    if request.method == 'POST':
        
        with transaction.atomic():
            
            trem_vazio_antigo = get_object_or_404(TremVazio, pk=id_trem_vazio)
            
            form = TremVazioForm(request.POST, instance=trem_vazio_antigo)
            
            if form.is_valid():

                trem_vazio_antigo = get_object_or_404(TremVazio, pk=id_trem_vazio)
                trem_vazio_antigo.delete()

                form = TremVazioForm(request.POST)

                trem_vazio  = form.save(commit=False)
                trem_vazio.created_by = request.user
                trem_vazio.save()

            else:

                print(form.errors)

            return redirect('previsao_subida')

    else:

        trem_vazio = get_object_or_404(TremVazio, pk=id_trem_vazio)
        trem_vazio.previsao = trem_vazio.previsao.strftime('%Y-%m-%dT%H:%M') 
        
        form = TremVazioForm(instance=trem_vazio)

        tipo_formulario = "editar_trem_subida"
    
        return carregar_previsao_trem_subida(request, form, tipo_formulario)

#endregion

#region Terminais

@login_required
def terminais_list_view(request):
    
    terminais = Terminal.objects.all()

    return render(request, 'terminais/terminais_list.html', {'terminais': terminais})

@login_required
def create_terminal_view(request):

    if request.method == 'POST':
        form = TerminalForm(request.POST)
        
        if form.is_valid():

            terminal        = form.save(commit=False)
            ultimo_terminal = Terminal.objects.order_by('-ordem').first()

            if ultimo_terminal:
                terminal.ordem = ultimo_terminal.ordem + 1
            else:
                terminal.ordem = 1

            terminal.save()
            return redirect('terminais_list')
        else:
            messages.error(request, form.errors)   

    form = TerminalForm()

    return render(request, 'terminais/create_terminal.html', {'form': form})

@login_required
def content_terminal_view(request, terminal_id):

    terminal = get_object_or_404(Terminal, id=terminal_id)
    return render(request, 'terminais/terminal_content.html', {'terminal': terminal})

#endregion