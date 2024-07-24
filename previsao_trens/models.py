from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

from    django.forms.models                                  import model_to_dict


from    django.db import transaction

#UserProfile
class Usuario(AbstractUser):

    foto        = models.ImageField(upload_to="fotos_de_perfil", blank=True, default='anonimo.jpg' )
    USERNAME_FIELD = 'username'  # Define o campo usado para fazer login
    
    # REQUIRED_FIELDS deve conter todos os campos adicionais necessários além de username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Adicione 'nome' aos campos necessários
    
    def __str__(self):

        return  self.username

class Trem(models.Model):

    prefixo     = models.CharField(max_length=100)
    os          = models.IntegerField()
    origem      = models.CharField(max_length=50)
    local       = models.CharField(max_length=50)
    destino     = models.CharField(max_length=50)
    terminal    = models.CharField(max_length=50)
    mercadoria  = models.CharField(max_length=50)
    vagoes      = models.IntegerField()
    previsao    = models.DateTimeField()
    ferrovia    = models.CharField(max_length=50, choices=[('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')])
    comentario  = models.CharField(max_length=100)
    
    posicao_previsao = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    def excluir_trem(self):

        # Tenta encontrar o trem pelo ID e excluí-lo.
        # CUIDADO AO EXCLUIR UM TREM QUE NÃO ESTÁ NA DESCARGA

        from previsao_trens.packages.descarga.EDITAR_DESCARGA       import NAVEGACAO_DESCARGA
        from previsao_trens.packages.CRIAR_TREM.ATUALIZAR_POSICAO   import AJUSTAR_POSICAO_CHEGADA

        try:
            with transaction.atomic():
                
                TREM_ANTIGO = model_to_dict(self)
                print(f"Deletando: { TREM_ANTIGO }")
                self.delete()

                try:  
                    try:
                        
                        NAVEGACAO = NAVEGACAO_DESCARGA(TREM_ANTIGO["terminal"], TREM_ANTIGO["ferrovia"], TREM_ANTIGO["mercadoria"]) #5
                        NAVEGACAO.EDITAR_TREM(TREM_ANTIGO, "REMOVER")
                    
                    except:

                        NAVEGACAO = NAVEGACAO_DESCARGA(TREM_ANTIGO["terminal"], TREM_ANTIGO["ferrovia"], TREM_ANTIGO["mercadoria"], DIA_ANTERIOR=True) #5
                        NAVEGACAO.EDITAR_TREM(TREM_ANTIGO, "REMOVER")

                except IndexError:
                    pass

                POSICAO_TREM = TREM_ANTIGO['posicao_previsao']
                PREVISAO_TREM = TREM_ANTIGO['previsao'].date()


                AJUSTAR_POSICAO_CHEGADA(ACAO="EXCLUIR TREM", PREVISAO_TREM_EXCLUIDO=PREVISAO_TREM, POSICAO=POSICAO_TREM)


        except Trem.DoesNotExist:
            # Lidar com o caso onde o trem não é encontrado
            pass
     
    @classmethod #Quando o método é responsável por criar uma nova instância do modelo.
    def criar_trem(cls, data, user):

        from .forms import TremForm
        from previsao_trens.packages.CRIAR_TREM.VALIDAR             import VALIDAR_NOVA_PREVISAO
        from previsao_trens.packages.CRIAR_TREM.ATUALIZAR_POSICAO   import AJUSTAR_POSICAO_CHEGADA
        from previsao_trens.packages.descarga.EDITAR_DESCARGA       import NAVEGACAO_DESCARGA

        with transaction.atomic():
            
            form = TremForm(data)
            
            if form.is_valid():
                novo_trem = form.cleaned_data
                criterios_avaliados = VALIDAR_NOVA_PREVISAO(novo_trem)
                
                if not criterios_avaliados["STATUS"]:
                    return {"status": False, "descricao": criterios_avaliados["DESCRICAO"], "errors": None}

                AJUSTAR_POSICAO_CHEGADA(ACAO="INSERIR TREM", TREM=novo_trem)
                trem_objeto = form.save(commit=False)
                trem_objeto.created_by = user
                trem_objeto.save()

                novo_trem["ID"] = trem_objeto.id
                
                try:

                    print("tentando sem dia anterior...")    
                    navegacao = NAVEGACAO_DESCARGA(novo_trem["terminal"], novo_trem["ferrovia"], novo_trem["mercadoria"])
                    navegacao.EDITAR_TREM(novo_trem, "INSERIR")
                
                except IndexError:

                    print("com dia anterior...") 
                    navegacao = NAVEGACAO_DESCARGA(novo_trem["terminal"], novo_trem["ferrovia"], novo_trem["mercadoria"], DIA_ANTERIOR=True)
                    navegacao.EDITAR_TREM(novo_trem, "INSERIR")

                return {"status": True, "descricao": "Trem adicionado com sucesso!", "errors": None}
            else:
                
                return {"status": False, "descricao": None, "errors": form.errors}
 

    def __str__(self):
        return self.prefixo
    
class Restricao(models.Model):

    terminal    = models.CharField(max_length=50)
    mercadoria  = models.CharField(max_length=50)

    comeca_em   = models.DateTimeField()
    termina_em  = models.DateTimeField()

    porcentagem = models.IntegerField()

    motivo      = models.CharField(max_length=50)
    comentario  = models.CharField(max_length=50) 

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @staticmethod
    def json_to_form(json_data):

        form_data = {
        'terminal'  : json_data.get('TERMINAL', ''),
        'mercadoria'    : json_data.get('SEGMENTO', ''),
        'comeca_em'     : json_data.get('INICIO', ''),
        'termina_em'    : json_data.get('FINAL', ''),
        'porcentagem'   : json_data.get('PCT', 0),
        'motivo'        : json_data.get('MOTIVO', ''),
        'comentario'    : json_data.get('COMENTARIO', '')
        }
        return form_data

    def excluir_restricao(self):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA

        with transaction.atomic():
            restricao_antiga = model_to_dict(self)
            self.delete()

        try: #CASO ESTEJA FORA DA DATA
            try:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"])
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
            
            except KeyError:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"], DIA_ANTERIOR=True)
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
        
        except IndexError:
            pass

    @classmethod
    def criar_restricao(cls, data, user):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA   import NAVEGACAO_DESCARGA
        from previsao_trens.packages.RESTRICAO.VALIDAR          import VALIDAR_RESTRICAO
        from .forms                                             import RestricaoForm

        with transaction.atomic():
            
            restricao_form = RestricaoForm(data)
            
            if restricao_form.is_valid():

                restricao = restricao_form.cleaned_data
                é_valida = VALIDAR_RESTRICAO(restricao)

                if not é_valida["STATUS"]:
                    return {"status": False, "descricao": é_valida["DESCRICAO"], "errors": None, "form": restricao_form}
            
                try: #CASO ESTEJA FORA DA DATA
                    
                    try:
                        
                        navegacao = NAVEGACAO_DESCARGA(restricao["terminal"], None, restricao["mercadoria"])
                        navegacao.EDITAR_RESTRICAO(restricao, "INSERIR")
                    
                    except KeyError:
                        
                        navegacao = NAVEGACAO_DESCARGA(restricao["terminal"], None, restricao["mercadoria"], DIA_ANTERIOR=True)
                        navegacao.EDITAR_RESTRICAO(restricao, "INSERIR")
                    
                    restricao_objeto = restricao_form.save(commit=False)
                    restricao_objeto.created_by = user
                    restricao_objeto.save()
                
                except IndexError:
                    pass

                return {"status": True, "descricao": "Restrição criada com sucesso!", "errors": None, "form": restricao_form}
            else:

                return {"status": False, "descricao": None, "errors": restricao_form.errors, "form": restricao_form}

    def __str__(self):

        return (f"{ self.terminal } - { self.motivo }")

class TremVazio(models.Model):

    prefixo      = models.CharField(max_length=100)
    ferrovia     = models.CharField(max_length=50, choices=[('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')])
    loco_1       = models.CharField(max_length=100)
    loco_2       = models.CharField(max_length=100, blank=True, null=True)
    loco_3       = models.CharField(max_length=100, blank=True, null=True)
    loco_4       = models.CharField(max_length=100, blank=True, null=True)
    loco_5       = models.CharField(max_length=100, blank=True, null=True)
    previsao     = models.DateTimeField(blank=True, null=True)
    eot          = models.CharField(max_length=100)
    
    qt_graos     = models.IntegerField(blank=True, null=True)
    qt_ferti     = models.IntegerField(blank=True, null=True)
    qt_celul     = models.IntegerField(blank=True, null=True)
    qt_acuca     = models.IntegerField(blank=True, null=True)
    qt_contei    = models.IntegerField(blank=True, null=True)

    margem       = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.prefixo
