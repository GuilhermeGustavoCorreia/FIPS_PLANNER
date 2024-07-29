from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.redirect_to_login),

    path('restricao/',                  views.restricoes_view,      name="restricao"),
    path('restricao/criar_restricao',   views.criar_restricao_view, name="criar_restricao"),
    path('restricao/excluir_restricao/<int:id>/', views.excluir_restricao_view,        name="excluir_restricao"),
    
    path('restricao/editar/<int:id>/',  views.editar_restricao,         name="editar_restricao"),

    path('navegacao/',  views.navegacao,    name="navegacao"),
    path('profile/',    views.profile,      name="profile"),

    path('previsao/previsao_trens',                         views.previsao_trens_view,  name="previsao_trens"),
    path('previsao/previsao_trens/novo_trem_previsao',      views.criar_trem_view,      name="novo_trem_previsao"),
    path('previsao/previsao_trens/alterar_posicao',         views.alterar_posicao_view, name="alterar_posicao"),
    path('previsao/previsao_trens/excluir_trem/<int:id>/',  views.excluir_trem_view,    name="excluir_trem"),
    path('editar_trem/<int:trem_id>/',                      views.editar_trem,          name='editar_trem'),
    path('dividir_trem/<int:trem_id>/',                     views.dividir_trem,         name="dividir_trem"),
    path('upload/',                                         views.upload_file_view,     name='upload_file'),

    path('configuracao/',   views.configuracao,        name="configuracao"),
    
    path('detalhe/',                                views.detalhe,                  name="detalhe"),
    path('ocupacao_terminais/',                     views.ocupacao_terminais,       name="ocupacao_terminais"),

    path('programacao_subida/',                     views.programacao_subida,       name="programacao_subida"),
    path('previsao_subida/',                        views.previsao_subida_view,     name="previsao_subida"),
    path('excluir_trem_subida/<int:id_trem_vazio>/',           views.excluir_trem_subida_view,      name="excluir_trem_subida"),
]
