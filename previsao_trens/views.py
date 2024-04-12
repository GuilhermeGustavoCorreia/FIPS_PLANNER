from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.contrib.auth.decorators import login_required
from rolepermissions.roles import assign_role
from django.shortcuts import redirect
from django.urls import reverse

def redirect_to_login(request):
    
    return redirect(reverse('login'))

@login_required
def navegacao(request):

    return render(request, 'navegacao.html')

@login_required
def profile(request):

    return render(request, 'user/profile.html')



from .models import Trem
from .forms  import TremForm
from django.contrib import messages
@login_required
def criar_trem(request):


    trens = Trem.objects.all()  # Busca todos os trens no banco de dados
    form = TremForm()  # Instancia um formulário vazio para ser usado no modal

    if request.method == 'POST':
        form = TremForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trem adicionado com sucesso!')
        else:
            messages.error(request, 'Erro na validação. Verifique os dados inseridos.')
    
    return render(request, 'previsao/criar_trem.html', {'trens': trens, 'form': form})

@login_required
def novo_trem_previsao(request):

    if request.method == 'POST':
        form = TremForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trem adicionado com sucesso!')
        else:
            messages.error(request, 'Erro na validação. Verifique os dados inseridos.')
    else:
        form = TremForm()
    return render(request, 'previsao/criar_trem.html', {'form': form})

@login_required
def excluir_trem(request, id):
    # Tenta encontrar o trem pelo ID e excluí-lo.
    try:
        trem = Trem.objects.get(pk=id)
        trem.delete()
        messages.success(request, 'Trem excluído com sucesso!')
    except Trem.DoesNotExist:
        messages.error(request, 'Trem não encontrado.')
    
    # Redireciona para a página da lista de trens.
    return redirect('criar_trem')