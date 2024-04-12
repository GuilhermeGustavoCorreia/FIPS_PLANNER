from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_login),
    path('navegacao/',  views.navegacao,    name="navegacao"),
    path('profile/',    views.profile,      name="profile"),

    path('previsao/criar_trem',                       views.criar_trem,          name="criar_trem"),
    path('previsao/criar_trem/novo_trem_previsao',    views.novo_trem_previsao,  name="novo_trem_previsao"),
    path('previsao/criar_trem/excluir_trem/<int:id>/', views.excluir_trem,        name="excluir_trem"),
]
