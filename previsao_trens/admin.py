from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Trem, TremVazio



class UsuarioAdmin(UserAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
    (
        None, {'fields': ('cargo', 'foto')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
    (
        None, {'fields': ('cargo', 'foto')}),
    )

admin.site.register(Usuario, UserAdmin)

admin.site.register(Trem)
admin.site.register(TremVazio)