from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario



class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'email', 'foto')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff')

admin.site.register(Usuario, UsuarioAdmin)

