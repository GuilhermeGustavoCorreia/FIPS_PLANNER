from rolepermissions.roles import AbstractUserRole

class CurtoPrazo(AbstractUserRole):
    role_name = "curto_prazo"
    available_permissions  = {
        "editar_subida":    False,
        "editar_itens":     True, 
        "ver_previsao":     True, 
        "ver_navegacao":    True,
        "ver_relatorios":   True,
        "gerenciar_contas": False
    }

class UsuarioComum(AbstractUserRole):
    role_name = "usuario_comum"
    available_permissions  = {
        "editar_subida":    False,
        "editar_itens":     False, 
        "ver_previsao":     True, 
        "ver_navegacao":    True,
        "ver_relatorios":   True,
        "gerenciar_contas": False
    }

class CelulaOperacao(AbstractUserRole):
    role_name = "celula_operacao"
    available_permissions  = {
        "editar_subida":    True,
        "editar_itens":     False, 
        "ver_previsao":     True, 
        "ver_navegacao":    True,
        "ver_relatorios":   True,
        "gerenciar_contas": False
    }