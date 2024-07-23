from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from rolepermissions.roles import get_user_roles, assign_role, clear_roles, RolesManager
from .models import Usuario, Trem, TremVazio, Restricao
from setup.roles import CurtoPrazo, UsuarioComum, CelulaOperacao  # Certifique-se de que o caminho para roles.py está correto

# Função para obter todos os papéis disponíveis
def get_roles_names():
    roles = RolesManager.get_roles()
    return [(role.role_name, role.role_name) for role in roles]

# Formulário personalizado para o modelo Usuario
class UserChangeForm(forms.ModelForm):
    # Campo adicional para selecionar os papéis do usuário
    roles = forms.MultipleChoiceField(
        choices  = get_roles_names(),  # Opções são todos os nomes de papéis disponíveis
        required = False,  # Campo não é obrigatório
        label    = 'Roles'  # Rótulo do campo no formulário
    )

    class Meta:
        model  = Usuario
        fields = '__all__'  # Incluir todos os campos do modelo Usuario

# Classe personalizada para a administração do modelo Usuario
class CustomUserAdmin(UserAdmin):
    form = UserChangeForm  # Usar o formulário personalizado criado acima

    # Inclua campos adicionais aqui
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('foto', 'roles',)}),
    )

    # Método para salvar o modelo, sobrescrevendo o comportamento padrão
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Chamar o método original para salvar o usuário
        if change:
            clear_roles(obj)  # Limpar os papéis antigos do usuário
            roles = form.cleaned_data.get('roles')  # Obter os novos papéis do formulário
            if roles:
                for role in roles:
                    assign_role(obj, role)  # Atribuir cada papel ao usuário

    # Método para obter o formulário, sobrescrevendo o comportamento padrão
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)  # Chamar o método original para obter o formulário
        if obj:
            roles = [role.role_name for role in get_user_roles(obj)]  # Obter os papéis atuais do usuário
            form.base_fields['roles'].initial = roles  # Definir os papéis atuais como valores iniciais no formulário
        return form

# Registrar o modelo Usuario com o admin do Django usando a classe personalizada CustomUserAdmin
admin.site.register(Usuario, CustomUserAdmin)
# Registrar outros modelos no admin do Django
admin.site.register(Trem)
admin.site.register(TremVazio)
admin.site.register(Restricao)
