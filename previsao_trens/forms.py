from django import forms
from .models import Trem
from django.forms.widgets import DateTimeInput, TextInput, NumberInput, Select, Textarea, RadioSelect

import os
import json

def DICIONARIO_MERCADORIAS():

    
    LOCAL = os.getcwd()
    CAMINHO = "previsao_trens\src\DICIONARIOS\PRODUTOS_E_TERMINAIS.json"

    with open(f"{ LOCAL }\{ CAMINHO }", 'r') as arquivo:
        dados_lidos = json.load(arquivo)
    
    return dados_lidos

MERCADORIAS = DICIONARIO_MERCADORIAS()

class TremForm(forms.ModelForm):

    MERCADORIAS = DICIONARIO_MERCADORIAS()

    class Meta:
        model = Trem
        fields = '__all__'
        widgets = {

            'prefixo':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Prefixo'}),
            'os':           NumberInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'OS'}),
            'origem':       TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Origem'}),
            'local':        TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Local'}),
            'destino':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Destino'}),

            'mercadoria':   Select(choices=[(k, k) for k in MERCADORIAS.keys()], attrs={'class': 'INPUT INPUT_G', 'onchange': 'updateTerminals()'}),
            'terminal':     Select(choices=[(k, k) for k in MERCADORIAS["ACUCAR"]], attrs={'class': 'INPUT INPUT_M'}),

            'vagoes':       NumberInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Vagões'}),
            'previsao':     DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', 'placeholder': 'Previsão'}),
            'comentario':   Textarea(attrs={'class': 'INPUT INPUT_G', 'placeholder': 'Comentário', 'rows': 2}),
            'ferrovia':     RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(TremForm, self).__init__(*args, **kwargs)
        # Definir valores padrões
        self.initial['prefixo'] = 'U36'
        self.initial['os'] = 1234567
        self.initial['origem'] = 'ZBL'
        self.initial['local'] = 'ZEM'
        self.initial['destino'] = 'PSN'
        self.initial['mercadoria'] = 'FARELO'
        self.initial['terminal'] = 'T39'
        self.initial['vagoes'] = 60
        self.initial['previsao'] = '2024-04-18T12:00'
        self.initial['comentario'] = 'ESTE É UM TRES DE DESTE'
        self.fields['ferrovia'].choices = [('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')]



