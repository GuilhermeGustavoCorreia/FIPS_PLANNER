from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from django.shortcuts               import redirect
from django.urls                    import reverse
from django.forms.models            import model_to_dict

from .models        import Trem
from .forms         import TremForm
from django.contrib import messages

from    previsao_trens.packages.CONFIGURACAO.CARREGAR_PAGINA    import ABRIR_TERMINAIS_ATIVOS
from    previsao_trens.packages.CONFIGURACAO.EDITAR_PARAMETROS  import EDITAR_PARAMETROS
from    previsao_trens.packages.CONFIGURACAO.ATUALIZAR_DESCARGA import ATUALIZAR_DESCARGA

from    previsao_trens.packages.CRIAR_TREM.VALIDAR import VALIDAR_NOVA_PREVISAO

import previsao_trens.packages.descarga.CARREGAR_PAGINA as CARREGAR_DESCARGA

from    previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as NAVEGACAO_DESCARGA

def redirect_to_login(request):
    
    return redirect(reverse('login'))


@login_required
def navegacao(request):

    DESCARGAS = CARREGAR_DESCARGA.PAGINA_COMPLETA()
    return render(request, 'navegacao.html', {"descargas": DESCARGAS})

@login_required
def profile(request):

    return render(request, 'user/profile.html')



@login_required
def criar_trem(request):


    trens = Trem.objects.all()  # Busca todos os trens no banco de dados
    form = TremForm()  # Instancia um formulário vazio para ser usado no modal
 
    return render(request, 'previsao/criar_trem.html', {'trens': trens, 'form': form})

@login_required
def novo_trem_previsao(request):
    
    trens = Trem.objects.all()
    
    if request.method == 'POST':

        #ABSTRAINDO OS DADOS DO NOVO TREM
        form = TremForm(request.POST)

        #VALIDAR O TREM NA DESCARGA
        if form.is_valid(): 

            #VALIDAR
            #1. EXISTE UM TREM CHEGANDO NESTA HORA NESTE TERMINAL (É O MESMO TREM?)
            #2. O TREM ESTA CHEGANDO EM UM PERÍODO VÁLIDO? (DATA EM D-2 ou D-1 em 00:00  OU DATA > D+4)

            CRITERIOS_AVALIADOS = VALIDAR_NOVA_PREVISAO(form.cleaned_data)

            if CRITERIOS_AVALIADOS["STATUS"] == False:

                messages.error(request, CRITERIOS_AVALIADOS["DESCRICAO"])
                return render(request, 'previsao/criar_trem.html', {'trens': trens, 'form': form})


            NAVEGACAO = NAVEGACAO_DESCARGA()
            NAVEGACAO.EDITAR_TREM(form.cleaned_data, "INSERIR")

            form.save()

            messages.success(request, 'Trem adicionado com sucesso!')

        else:
            messages.error(request, 'Erro na validação. Verifique os dados inseridos.')
    else:

        form = TremForm()
    return render(request, 'previsao/criar_trem.html', {'trens': trens, 'form': form})

@login_required
def excluir_trem(request, id):

    # Tenta encontrar o trem pelo ID e excluí-lo.
    # CUIDADO AO EXCLUIR UM TREM QUE NÃO ESTA NA DESCARGA

    try:
        trem = Trem.objects.get(pk=id)
        
        NAVEGACAO = NAVEGACAO_DESCARGA()
        NAVEGACAO.EDITAR_TREM(model_to_dict(trem), "REMOVER")
        
        trem.delete()
        messages.success(request, 'Trem excluído com sucesso!')

    except Trem.DoesNotExist:

        messages.error(request, 'Trem não encontrado.')
    
    # Redireciona para a página da lista de trens.
    return redirect('criar_trem')




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