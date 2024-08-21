from    django.db                   import models, transaction
from    django.contrib.auth.models  import AbstractUser
from    django.conf                 import settings
from    django.forms.models         import model_to_dict
from    django.db.models            import F

from    datetime                    import timedelta


        

class Segmento(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Mercadoria(models.Model):

    nome     = models.CharField(max_length=100)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE, related_name='mercadorias')

    def __str__(self):
        return self.nome
    
class Terminal(models.Model):

    nome            = models.CharField(max_length=100)
    ordem           = models.IntegerField()
    margem          = models.CharField(max_length=100) 
    patio           = models.CharField(max_length=100) 
    tempo_encoste   = models.IntegerField()
    segmento        = models.ForeignKey(Segmento, on_delete=models.CASCADE, related_name='terminais')

    def __str__(self):
        return self.nome
    
class Trem(models.Model):

    prefixo     = models.CharField(max_length=100)
    os          = models.IntegerField()
    origem      = models.CharField(max_length=50)
    local       = models.CharField(max_length=50)
    destino     = models.CharField(max_length=50)
    terminal    = models.ForeignKey(Terminal, on_delete=models.CASCADE) 
    mercadoria  = models.ForeignKey(Mercadoria, on_delete=models.CASCADE)
    vagoes      = models.IntegerField()
    previsao    = models.DateTimeField(null=True, blank=True)
    encoste     = models.DateTimeField(null=True, blank=True)
    ferrovia    = models.CharField(max_length=50, choices=[('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')])
    comentario  = models.CharField(max_length=100)
    
    posicao_previsao = models.IntegerField(default=0)
    translogic       = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def update_position(self, new_position):

        old_position = self.posicao_previsao

        if old_position > new_position: direction = "para cima"
        if old_position < new_position: direction = "para baixo"

        if direction == "para cima":
            
            Trem.objects.filter(
                
                posicao_previsao__gt = new_position - 1,
                posicao_previsao__lt = self.posicao_previsao,
                previsao__date       = self.previsao
                
            ).update(posicao_previsao=F('posicao_previsao') + 1)

        if direction == "para baixo":

            Trem.objects.filter(
                
                posicao_previsao__gt = self.posicao_previsao,
                posicao_previsao__lt = new_position + 1,
                previsao__date       = self.previsao
            
            ).update(posicao_previsao=F('posicao_previsao') - 1)

        self.posicao_previsao = new_position
        super().save()

    def save(self, *args, **kwargs):
        
        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as Navegacao
        
        #region em caso de edicao
        if not self._state.adding:

            trem_atual      = Trem.objects.get(pk=self.pk)
            previsao_antiga = trem_atual.previsao.date() if trem_atual.previsao else None
            nova_previsao   = self.previsao.date() if self.previsao else None
            
            self.posicao_previsao = trem_atual.posicao_previsao
            if nova_previsao:
                
                if previsao_antiga != nova_previsao:

                    self.posicao_previsao = 0

                    Trem.objects.filter(
                        
                        posicao_previsao__gt    = trem_atual.posicao_previsao, 
                        previsao__year          = previsao_antiga.year, 
                        previsao__month         = previsao_antiga.month, 
                        previsao__day           = previsao_antiga.day
                        
                    ).update(posicao_previsao=F('posicao_previsao') - 1) 

                    Trem.objects.filter(
                        
                        previsao__year  = nova_previsao.year, 
                        previsao__month = nova_previsao.month, 
                        previsao__day   = nova_previsao.day
                    
                    ).update(posicao_previsao=F('posicao_previsao') + 1)


            super().delete(*args, **kwargs)
            
            if trem_atual.previsao: 
                
                self.encoste = (trem_atual.previsao + timedelta(hours=trem_atual.terminal.tempo_encoste))
                CalculoNavegacaoAntigo = Navegacao(trem_atual.terminal.nome, trem_atual.ferrovia, trem_atual.mercadoria.nome)
                CalculoNavegacaoAntigo.atualizar(trem_atual)

        #endregion

        self.prefixo = self.prefixo.upper()

        #ajustando previsão (colocando este trem como o primeiro da lista)
        if self._state.adding:
            
            Trem.objects.filter(
                
                previsao__year  = self.previsao.year, 
                previsao__month = self.previsao.month, 
                previsao__day   = self.previsao.day
                
            ).update(posicao_previsao=F('posicao_previsao') + 1)

        #inserindo tempo de encoste
        if self.previsao: 
            
            self.encoste = (self.previsao + timedelta(hours=self.terminal.tempo_encoste))
 
            super().save(*args, **kwargs)
            CalculoNavegacao = Navegacao(self.terminal.nome, self.ferrovia, self.mercadoria.nome)
            CalculoNavegacao.atualizar(self)

        else:

            super().save(*args, **kwargs)    

    def delete(self, *args, **kwargs):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as Navegacao
       
        with transaction.atomic():  # Garante que as mudanças sejam atômicas
            
            if self.previsao:    
                #ajustando previsão 
                Trem.objects.filter(
                    
                    posicao_previsao__gt    = self.posicao_previsao, 
                    previsao__year          = self.previsao.year, 
                    previsao__month         = self.previsao.month, 
                    previsao__day           = self.previsao.day
                
                ).update(posicao_previsao=F('posicao_previsao') - 1)

                super().delete(*args, **kwargs)
                
                CalculoNavegacao = Navegacao(self.terminal.nome, self.ferrovia, self.mercadoria.nome)
                CalculoNavegacao.atualizar(self)

            else:

                super().delete(*args, **kwargs)

    def to_slice(self, slice_01, slice_02):
  
        with transaction.atomic():

            if self.previsao.date() == slice_01["previsao"].date() == slice_02["previsao"].date():
                with transaction.atomic():  
                    Trem.objects.filter(
                        
                        posicao_previsao__gt = self.posicao_previsao,
                        previsao__date       = self.previsao

                    ).update(
                        posicao_previsao=F('posicao_previsao') + 1
                    )
                    slice_01["posicao_previsao"] = (self.posicao_previsao + 1)
          
        Trem.objects.create(**slice_01, created_by=self.created_by)
        Trem.objects.create(**slice_02, created_by=self.created_by)

        self.delete()

    def __str__(self):
        return f"{self.prefixo} -  {self.terminal} - {self.mercadoria} - {self.previsao}"
    
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
    eot          = models.CharField(max_length=3,  choices=[('Sim', 'Sim'), ('Nao', 'Nao')])
    margem       = models.CharField(max_length=8,  choices=[('Direita', 'Direita'), ('Esquerda', 'Esquerda')], blank=True)

    loco_1       = models.CharField(max_length=100)
    loco_2       = models.CharField(max_length=100, blank=True, null=True)
    loco_3       = models.CharField(max_length=100, blank=True, null=True)
    loco_4       = models.CharField(max_length=100, blank=True, null=True)
    loco_5       = models.CharField(max_length=100, blank=True, null=True)
    
    previsao     = models.DateTimeField(blank=True, null=True)
    partida_real = models.DateTimeField(blank=True, null=True)

    qt_graos     = models.IntegerField(blank=True, null=True)
    qt_ferti     = models.IntegerField(blank=True, null=True)
    qt_celul     = models.IntegerField(blank=True, null=True)
    qt_acuca     = models.IntegerField(blank=True, null=True)
    qt_contei    = models.IntegerField(blank=True, null=True)

    comentario   = models.CharField(max_length=100, blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        
        from  previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2 import Condensados

        super().save(*args, **kwargs)

        dict_trem = model_to_dict(self)
    
        Condensados().atualizar_previsao(dict_trem)

    def delete(self, *args, **kwargs):

        from previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2     import Condensados
        from django.forms.models import model_to_dict

        super().delete(*args, **kwargs)

        try:
            
            dict_trem = model_to_dict(self)
            Condensados().atualizar_previsao(dict_trem)

        except IndexError:
            pass

        

    def __str__(self):
        return self.prefixo

class Usuario(AbstractUser):

    foto        = models.ImageField(upload_to="fotos_de_perfil", blank=True, default='anonimo.jpg' )
    USERNAME_FIELD = 'username'  # Define o campo usado para fazer login
    
    # REQUIRED_FIELDS deve conter todos os campos adicionais necessários além de username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Adicione 'nome' aos campos necessários
    
    def __str__(self):

        return  self.username
    
