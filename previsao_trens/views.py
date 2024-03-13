from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario
from django.contrib.auth.decorators import login_required



@login_required
def navegacao(request):

    return render(request, 'navegacao.html')