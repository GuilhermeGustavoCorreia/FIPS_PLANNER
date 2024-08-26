from django.contrib import admin
from django.urls import path
from . import views


url_terminais = [
                
                    path('terminais_list/',                         views.terminais_list_view,      name='terminais_list'),
                    path('create_terminal/',                        views.create_terminal_view,     name='create_terminal'),
                    path('terminal_content/<int:terminal_id>/',     views.content_terminal_view,    name='terminal_content')
                ]

url_previsao = [

    path('previsao/previsao_trens',                                     views.previsao_trens_view,  name="previsao_trens"),
    
    path('previsao/previsao_trens/novo_trem_previsao',                  views.criar_trem_view,      name="novo_trem_previsao"),   
    path('previsao/previsao_trens/excluir_trem/<int:id>/',              views.excluir_trem_view,    name="excluir_trem"),   
    path('previsao/editar_trem/<int:trem_id>',                          views.editar_trem,          name='editar_trem'),
    path('previsao/dividir_trem/<int:trem_id>',                                 views.dividir_trem,         name="dividir_trem"),
    
    path('previsao/previsao_trens/excluir_tabela/<str:dia_logistico>',  views.excluir_dia_inteiro,  name="excluir_dia_inteiro"),
    path('previsao/previsao_trens/alterar_posicao',                     views.alterar_posicao_view, name="alterar_posicao"),
    path('get-terminals/',                                              views.get_terminals,        name='get_terminals'),
]

url_navegacao = [

    path('navegacao/',                  views.navegacao,            name="navegacao"),
    path('navegacao/editar_encoste',    views.editar_encoste,       name="editar_encoste"),
]

urlpatterns = [

    path('', views.redirect_to_login),
    path('accounts/login/', views.custom_login_view, name='login'),

    path('restricao/',                  views.restricoes_view,      name="restricao"),
    path('restricao/criar_restricao',   views.criar_restricao_view, name="criar_restricao"),
    path('restricao/excluir_restricao/<int:id>/', views.excluir_restricao_view,        name="excluir_restricao"),
    
    path('restricao/editar/<int:id>/',  views.editar_restricao,         name="editar_restricao"),

    
    path('profile/',    views.profile,      name="profile"),

 
    path('upload/',                                             views.upload_file_view,     name='upload_file'),

    #PAGINA CONFIGURACAO
    path('configuracao/',               views.configuracao,                     name = "configuracao"),
    path('baixar_integracao/',          views.baixar_integracao_view,           name = "baixar_integracao"), 
    path('baixar_planilha/',            views.baixar_planilha_view,             name = "baixar_planilha"),
    path('baixar_planilha_antiga/',     views.baixar_planilh_antiga_view,       name = "baixar_planilha_antiga"),
    path('baixar_detalhe/',             views.baixar_planilha_detalhe_view,     name = "baixar_detalhe"),

    #RELATORIOS
    path('detalhe/',                                views.detalhe,                  name="detalhe"),
    path('ocupacao_terminais/',                     views.ocupacao_terminais,       name="ocupacao_terminais"),
   
    path('programacao_subida/',                     views.programacao_subida,       name="programacao_subida"),
    path('previsao_subida/',                        views.previsao_subida_view,     name="previsao_subida"),

    path('previsao_subida/criar_trem_subida',                  views.criar_trem_subida_view,        name="criar_trem_subida"),
    path('excluir_trem_subida/<int:id_trem_vazio>/',           views.excluir_trem_subida_view,      name="excluir_trem_subida"),

] + url_terminais + url_previsao + url_navegacao
