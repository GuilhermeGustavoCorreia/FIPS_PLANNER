from django import template

register = template.Library()

@register.filter
def times(number, value):
    return number * value


@register.filter
def formata_milhar(valor):
    # Converte o valor para string se não for
    if not isinstance(valor, str):
        valor = str(valor)
    
    try:
        # Substitui a vírgula pelo ponto temporariamente para conversão
        valor_float = float(valor.replace(',', '.'))
        # Formata o valor com separadores de milhares
        valor_formatado = f"{valor_float:,.0f}"
        # Substitui os separadores para o formato desejado
        return valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
    except ValueError:
        return valor  # Retorna o valor original se a conversão falhar