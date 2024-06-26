from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.redirect_to_login),

    path('restricao/',  views.restricao,    name="restricao"),

    path('restricao/excluir/<int:id>/', views.excluir_restricao,        name="excluir_restricao"),
    path('restricao/editar/<int:id>/',  views.editar_restricao,         name="editar_restricao"),

    path('navegacao/',  views.navegacao,    name="navegacao"),
    path('profile/',    views.profile,      name="profile"),

    path('previsao/criar_trem',                        views.criar_trem,          name="criar_trem"),
    path('previsao/criar_trem/novo_trem_previsao',     views.novo_trem_previsao,  name="novo_trem_previsao"),
    path('previsao/criar_trem/excluir_trem/<int:id>/', views.excluir_trem,        name="excluir_trem"),
    path('editar_trem/<int:trem_id>/',                 views.editar_trem,         name='editar_trem'),
    path('dividir_trem/<int:trem_id>/',                views.dividir_trem,        name="dividir_trem"),
    path('upload/',                                    views.upload_file_view,    name='upload_file'),

    path('configuracao/',   views.configuracao,        name="configuracao"),
    path('detalhe/',        views.detalhe,             name="detalhe"),

    path('programacao_subida/',                     views.programacao_subida,     name="programacao_subida"),
    path('previsao_subida/',                        views.previsao_subida,        name="previsao_subida"),
    path('editar_trem_subida/<int:id>/',            views.editar_trem_subida,     name="editar_trem_subida"),
]
