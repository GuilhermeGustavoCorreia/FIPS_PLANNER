from django import forms
from .models import Trem, Restricao, TremVazio
from django.forms.widgets import DateTimeInput, TextInput, NumberInput, Select, Textarea, RadioSelect

import os
import json

def DICIONARIO_MERCADORIAS():

    
    LOCAL = os.getcwd()
    CAMINHO = "previsao_trens/src/DICIONARIOS/PRODUTOS_E_TERMINAIS.json"

    with open(f"{ LOCAL }/{ CAMINHO }", 'r') as arquivo:
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
            'ferrovia':     RadioSelect(attrs={'name': 'ferrovia'})
        }

    def __init__(self, *args, **kwargs):
        super(TremForm, self).__init__(*args, **kwargs)
        self.fields['ferrovia'].choices = [('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')]

        self.fields['posicao_previsao'].required = False 


class RestricaoForm(forms.ModelForm):

    MERCADORIAS = DICIONARIO_MERCADORIAS()

    class Meta:
        
        model   = Restricao
        fields  = '__all__'
        widgets = {

            'mercadoria':   Select(choices=[(k, k) for k in MERCADORIAS.keys()],    attrs={'class': 'INPUT INPUT_M', 'onchange': 'updateTerminals()'}),
            'terminal':     Select(choices=[(k, k) for k in MERCADORIAS["ACUCAR"]], attrs={'class': 'INPUT INPUT_M'}),
            
            'comeca_em':     DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', }),
            'termina_em':    DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', }),

            'porcentagem':   NumberInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': '%'}),

            'motivo':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Motivo'}),
            'comentario':  Textarea(attrs={'class': 'INPUT INPUT_G', 'placeholder': 'Comentário', 'rows': 2}),

        }

class UploadFileForm(forms.Form):
    file = forms.FileField()

class TremVazioForm(forms.ModelForm):

    class Meta:

        model   = TremVazio
        fields  = '__all__'
        widgets = {

            'prefixo':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Prefixo'}),
            
            'eot':          TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'EOT'}),
            
            'ferrovia':     RadioSelect(attrs={'name': 'ferrovia', 'onclick': 'ATUALIZAR_VAGOES()'}),

            'loco_1':      TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 01'}),
            'loco_2':      TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 02'}),
            'loco_3':      TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 03'}),
            'loco_4':      TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 04'}),
            'loco_5':      TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 05'}),

            'qt_graos':       NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'GRAO',            'placeholder': 'Grãos', 'onchange': 'VALIDAR_QUANTIDADE(this)'}),
            'qt_ferti':       NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'FERTILIZANTE',    'placeholder': 'Ferti', 'onchange': 'VALIDAR_QUANTIDADE(this)'}),
            'qt_celul':       NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'CELULOSE',        'placeholder': 'Celulose', 'onchange': 'VALIDAR_QUANTIDADE(this)'}),
            'qt_acuca':       NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'ACUCAR',          'placeholder': 'Açúcar', 'onchange': 'VALIDAR_QUANTIDADE(this)'}),
            'qt_contei':      NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'CONTEINER',       'placeholder': 'Conteiner', 'onchange': 'VALIDAR_QUANTIDADE(this)'}),

            'previsao':     DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', 'placeholder': 'Previsão'}, format='%Y-%m-%dT%H:%M'),
            'margem':       RadioSelect(attrs={'name': 'margem'})
        }


    def __init__(self, *args, **kwargs):
        
        super(TremVazioForm, self).__init__(*args, **kwargs)
        self.fields['ferrovia'].choices = [('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')]
        self.fields['margem'].choices   = [('DIREITA', 'DIREITA'), ('ESQUERDA', 'ESQUERDA')]

        # Definindo o valor inicial para 'ferrovia' como 'RUMO'
        self.initial['ferrovia'] = 'RUMO'

        # Tornando os campos específicos não obrigatórios
        self.fields['loco_2'].required      = False
        self.fields['loco_3'].required      = False
        self.fields['loco_4'].required      = False
        self.fields['loco_5'].required      = False
        self.fields['qt_graos'].required    = False
        self.fields['qt_ferti'].required    = False
        self.fields['qt_celul'].required    = False
        self.fields['qt_acuca'].required    = False
        self.fields['qt_contei'].required   = False

        self.fields['previsao'].required    = False
        self.fields['margem'].required      = False

