from rest_framework.permissions import BasePermission

class IsInAllowedGroup(BasePermission):
    
    """
    Permissão personalizada para permitir o acesso apenas aos usuários de um grupo específico.
    """

    def has_permission(self, request, view):
        
        # Verifica se o usuário está autenticado e faz parte do grupo 'allowed_group'
        return request.user and request.user.groups.filter(name='api_user').exists()
