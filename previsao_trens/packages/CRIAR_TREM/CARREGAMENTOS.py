import pandas as pd
from datetime import datetime
from previsao_trens.models        import Trem

def CARREGAR_PREVISOES():

    PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
    PERIODO_VIGENTE = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)

    TABELAS = {}

    for _, LINHA in PERIODO_VIGENTE.iterrows():

            DATA = datetime.strptime(LINHA['DATA_ARQ'], '%Y-%m-%d')

            queryset = Trem.objects.filter(
                previsao__year=DATA.year,
                previsao__month=DATA.month,
                previsao__day=DATA.day
            ).order_by('posicao_previsao')
            if queryset.exists():  # Adiciona ao dicionário apenas se o queryset não estiver vazio
                TABELAS[LINHA['NM_DIA']] = queryset

    return TABELAS