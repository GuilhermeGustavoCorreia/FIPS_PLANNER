from rolepermissions.roles import AbstractUserRole


class AnalistaCurtoPrazo(AbstractUserRole):

    available_permissions  = {
        "editar_itens":     True, 
        "ver_previsao":     True, 
        "ver_navegacao":    True,
        "ver_relatorios":   True,
        "gerenciar_contas": False
    }

class Supervisao(AbstractUserRole):

    available_permissions  = {
        "editar_itens":     True, 
        "ver_previsao":     True, 
        "ver_navegacao":    True,
        "ver_relatorios":   True,
        "gerenciar_contas": True
    }