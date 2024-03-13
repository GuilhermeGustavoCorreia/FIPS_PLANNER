from django.db import models
from django.contrib.auth.models import AbstractUser



class Usuario(AbstractUser):

    cargo       = models.CharField(max_length=200, null=True)
    foto        = models.ImageField(upload_to="fotos_de_perfil", blank=True, default='anonimo.jpg' )

    USERNAME_FIELD = 'username'  # Define o campo usado para fazer login
    
    # REQUIRED_FIELDS deve conter todos os campos adicionais necessários além de username
    REQUIRED_FIELDS = ['first_name ', 'last_name']  # Adicione 'nome' aos campos necessários

    def __str__(self):
        return self.first_name if self.username else self.username  # Retorna o nome do usuário ao chamar str(objeto)
