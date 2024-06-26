from django.db import models
from django.contrib.auth.models import AbstractUser



class Usuario(AbstractUser):

    cargo       = models.CharField(max_length=200, null=True)
    foto        = models.ImageField(upload_to="fotos_de_perfil", blank=True, default='anonimo.jpg' )

    USERNAME_FIELD = 'username'  # Define o campo usado para fazer login
    
    # REQUIRED_FIELDS deve conter todos os campos adicionais necessários além de username
    REQUIRED_FIELDS = ['first_name', 'last_name', 'foto']  # Adicione 'nome' aos campos necessários


    def __str__(self):
        return  self.username if self.first_name else self.first_name  # Retorna o nome do usuário ao chamar str(objeto)
    
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
    ferrovia    = models.CharField(max_length=50, choices=[('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')])
    comentario  = models.CharField(max_length=100)

    posicao_previsao = models.IntegerField(default=0)

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
