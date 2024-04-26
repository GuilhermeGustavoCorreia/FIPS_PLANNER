
from django.db              import transaction
from django.db.models       import F
from previsao_trens.models  import Trem

def AJUSTAR_POSICAO_CHEGADA(**kwargs):

    if  kwargs["ACAO"] == "INSERIR TREM":

        DATA = kwargs["TREM"]["previsao"]

        with transaction.atomic():  # Garante que as mudanças sejam atômicas
            Trem.objects.filter(
                    previsao__year=DATA.year,
                    previsao__month=DATA.month,
                    previsao__day=DATA.day
                ).update(posicao_previsao=F('posicao_previsao') + 1)


    elif kwargs["ACAO"] == "EXLUIR TREM":

        with transaction.atomic():  # Garante que as mudanças sejam atômicas
            Trem.objects.filter(
                posicao_previsao__gt=kwargs["POSICAO"],
                previsao__date=kwargs["PREVISAO_TREM_EXCLUIDO"]
            ).update(
                posicao_previsao=F('posicao_previsao') - 1
            )


    elif kwargs["ACAO"] == "EDITAR TREM":
        
        if kwargs['TREM_ANTIGO'].previsao.date() == kwargs['NOVO_TREM'].previsao.date():

            return kwargs['TREM_ANTIGO'].posicao_previsao


        #SE O NOVO TREM POSSUI DATA DIFERENTE
        #1. SE SIM, ENVIA-LO A NOVA PREVISAO COM POSICAO = 0

        DATA_ANTIGA = kwargs['TREM_ANTIGO'].previsao.date()
        DATA_NOVA   = kwargs['NOVO_TREM'].previsao.date()

        #   SOMAR +1 NA FILA DE TODOS QUE ESTAO NA NOVA PREVISAO
        with transaction.atomic(): 
            Trem.objects.filter(
                    previsao__year=DATA_NOVA.year,
                    previsao__month=DATA_NOVA.month,
                    previsao__day=DATA_NOVA.day
                ).update(posicao_previsao=F('posicao_previsao') + 1)
            
        #   ATUALIZAR A PREVISAO ANTIGA PARA TAMPAR GAP DE TREM QUE SAIU DA POSICAO
        with transaction.atomic():  
            Trem.objects.filter(
                posicao_previsao__gt=kwargs['TREM_ANTIGO'].posicao_previsao,
                previsao__date=DATA_ANTIGA
            ).update(
                posicao_previsao=F('posicao_previsao') - 1
            )

        return 0
    

    elif kwargs["ACAO"] == "DIVIDIR TREM":

        SAIDAS = {
            "POSICAO_01" : int,
            "POSICAO_02" : int
        }

        TREM_ANTIGO = kwargs["TREM_ANTIGO"]
        TREM_01     = kwargs["TREM_01"]
        TREM_02     = kwargs["TREM_02"]

        #CASOS 
        
        #TREM_ANTIGO  = TREM_01  = TREM_02
        if TREM_ANTIGO.previsao.date() == TREM_01["previsao"].date() == TREM_02["previsao"].date():
            print("CASO 01")
            SAIDAS["POSICAO_01"] = TREM_ANTIGO.posicao_previsao
            SAIDAS["POSICAO_02"] = TREM_ANTIGO.posicao_previsao + 1

            with transaction.atomic():  
                Trem.objects.filter(
                    posicao_previsao__gt= TREM_ANTIGO.posicao_previsao,
                    previsao__date      = TREM_ANTIGO.previsao
                ).update(
                    posicao_previsao=F('posicao_previsao') + 1
                )
            return SAIDAS
        
        #TREM_ANTIGO != TREM_01  = TREM_02
        if TREM_ANTIGO.previsao.date() != TREM_01["previsao"].date() == TREM_02["previsao"].date():
            print("CASO 02")
            SAIDAS["POSICAO_01"] = 0
            SAIDAS["POSICAO_02"] = 1

            DATA_NOVA = TREM_01["previsao"].date()

            with transaction.atomic():  
                Trem.objects.filter(
                    posicao_previsao__gt= TREM_ANTIGO.posicao_previsao,
                    previsao__date      = TREM_ANTIGO.previsao
                ).update(
                    posicao_previsao=F('posicao_previsao') - 1
                )

            with transaction.atomic(): 
                Trem.objects.filter(
                        previsao__year=DATA_NOVA.year,
                        previsao__month=DATA_NOVA.month,
                        previsao__day=DATA_NOVA.day
                    ).update(posicao_previsao=F('posicao_previsao') + 2)

            return SAIDAS
        
        #TREM_ANTIGO != TREM_01 != TREM_02
        if ((TREM_ANTIGO.previsao.date() != TREM_01["previsao"].date()) and
            (TREM_ANTIGO.previsao.date() != TREM_02["previsao"].date()) and
            (TREM_01["previsao"].date()  != TREM_02["previsao"].date()) ):

            print("CASO 03")
            print(f"{ TREM_ANTIGO.previsao.date() } \n { TREM_01["previsao"].date() } \n { TREM_02["previsao"].date() }")
            SAIDAS["POSICAO_01"] = 0
            SAIDAS["POSICAO_02"] = 0

            with transaction.atomic():  
                Trem.objects.filter(
                    posicao_previsao__gt= TREM_ANTIGO.posicao_previsao,
                    previsao__date      = TREM_ANTIGO.previsao
                ).update(
                    posicao_previsao=F('posicao_previsao') - 1
                )

            TRENS = [TREM_01, TREM_02]
            for TREM in TRENS:

                DATA_NOVA = TREM["previsao"].date()   

                with transaction.atomic(): 
                    Trem.objects.filter(
                            previsao__year=DATA_NOVA.year,
                            previsao__month=DATA_NOVA.month,
                            previsao__day=DATA_NOVA.day
                        ).update(posicao_previsao=F('posicao_previsao') + 1)

            return SAIDAS

        if TREM_ANTIGO.previsao.date() == TREM_01["previsao"].date() != TREM_02["previsao"].date():
            print("CASO 04")
            SAIDAS["POSICAO_01"] = TREM_ANTIGO.posicao_previsao
            SAIDAS["POSICAO_02"] = 0

            DATA_NOVA = TREM_02["previsao"].date()   

            with transaction.atomic(): 
                    Trem.objects.filter(
                            previsao__year=DATA_NOVA.year,
                            previsao__month=DATA_NOVA.month,
                            previsao__day=DATA_NOVA.day
                        ).update(posicao_previsao=F('posicao_previsao') + 1)  

            return SAIDAS     

        if TREM_ANTIGO.previsao.date() == TREM_02["previsao"].date() != TREM_01["previsao"].date():
            print("CASO 05")
            SAIDAS["POSICAO_02"] = TREM_ANTIGO.posicao_previsao
            SAIDAS["POSICAO_01"] = 0

            DATA_NOVA = TREM_01["previsao"].date()   

            with transaction.atomic(): 
                Trem.objects.filter(
                        previsao__year=DATA_NOVA.year,
                        previsao__month=DATA_NOVA.month,
                        previsao__day=DATA_NOVA.day
                    ).update(posicao_previsao=F('posicao_previsao') + 1)
            
            return SAIDAS
