from django import forms
from .models import Trem, Restricao, TremVazio
from django.forms.widgets import DateTimeInput, TextInput, NumberInput, Select, Textarea, RadioSelect
from django.contrib.auth.forms import AuthenticationForm
import os
import json
import pandas as pd
def DICIONARIO_MERCADORIAS():

    
    LOCAL = os.getcwd()
    CAMINHO = "previsao_trens/src/DICIONARIOS/PRODUTOS_E_TERMINAIS.json"

    with open(f"{ LOCAL }/{ CAMINHO }", 'r') as arquivo:
        dados_lidos = json.load(arquivo)
    
    return dados_lidos

MERCADORIAS = DICIONARIO_MERCADORIAS()

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        return username.upper()  # Converte o nome de usuário para maiúsculas


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
            'ferrovia':     RadioSelect(attrs={'class': 'INPUT INPUT_RADIO'})
        }

    def __init__(self, *args, **kwargs):
        super(TremForm, self).__init__(*args, **kwargs)
        self.fields['ferrovia'].choices = [('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')]
        self.fields['ferrovia'].initial = 'RUMO'
        self.fields['comentario'].required = False
        self.fields['posicao_previsao'].required = False 
        self.fields['created_by'].required = False

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
    def __init__(self, *args, **kwargs):

        super(RestricaoForm, self).__init__(*args, **kwargs)
        self.fields['created_by'].required          = False 

class UploadFileForm(forms.Form):
    file = forms.FileField()

from django         import forms
from .models        import TremVazio
from django.forms   import TextInput, RadioSelect, NumberInput, DateTimeInput

class TremVazioForm(forms.ModelForm):

    class Meta:
     
        PATH_PERIODO_VIGENTE = "previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv"
        periodo_vigente      = pd.read_csv(PATH_PERIODO_VIGENTE, sep=";", index_col=0)

        data_arq_D           = periodo_vigente[periodo_vigente['NM_DIA'] == "D"].iloc[0]['DATA_ARQ']
        data_arq_D1          = periodo_vigente[periodo_vigente['NM_DIA'] == "D+1"].iloc[0]['DATA_ARQ']

        model = TremVazio
        fields = '__all__'
        widgets = {
            'prefixo':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Prefixo', 'style': 'text-transform: uppercase;'}),
            'eot':          RadioSelect(),
            'ferrovia':     RadioSelect(attrs={'name': 'ferrovia', 'onclick': 'atualizar_tabela()'}),
            'loco_1':       TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 01'}),
            'loco_2':       TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 02'}),
            'loco_3':       TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 03'}),
            'loco_4':       TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 04'}),
            'loco_5':       TextInput(attrs={'class': 'INPUT INPUT_P ', 'placeholder': 'Loco 05'}),
            'qt_graos':     NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'GRAO'}),
            'qt_ferti':     NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'FERTILIZANTE'}),
            'qt_celul':     NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'CELULOSE'}),
            'qt_acuca':     NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'ACUCAR'}),
            'qt_contei':    NumberInput(attrs={'class': 'INPUT INPUT_P ', 'data-segmento': 'CONTEINER'}),
            'previsao':     DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', 'placeholder': 'Previsão', 'min': f'{data_arq_D}T01:00','max': f'{data_arq_D1}T23:59', 'onchange': 'atualizarHorario()'}),
            'margem':       RadioSelect(attrs={'name': 'margem', 'onclick': 'atualizar_tabela()'}),
        }

    def __init__(self, *args, **kwargs):
        
        super(TremVazioForm, self).__init__(*args, **kwargs)

        self.fields['ferrovia'].choices     = [('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')]
        self.fields['margem'].choices       = [('Direita', 'Direita'), ('Esquerda', 'Esquerda')]
        self.fields['eot'].choices          = [('Sim', 'Sim'), ('Nao', 'Não')]
        self.initial['ferrovia']            = 'RUMO'
        self.initial['eot']                 = 'Sim'
        self.initial['margem']              = 'Direita'

        # Definir campos opcionais
        self.fields['loco_2'].required      = False
        self.fields['loco_3'].required      = False
        self.fields['loco_4'].required      = False
        self.fields['loco_5'].required      = False
        self.fields['qt_graos'].required    = False
        self.fields['qt_ferti'].required    = False
        self.fields['qt_celul'].required    = False
        self.fields['qt_acuca'].required    = False
        self.fields['qt_contei'].required   = False
        self.fields['margem'].required      = False

        self.fields['created_by'].required = False


        # Configurar formato do campo `previsao`
        self.fields['previsao'].widget.attrs['format'] = '%Y-%m-%dT%H:%M'


    def clean_previsao(self):

        previsao = self.cleaned_data.get('previsao')
        margem   = self.cleaned_data.get('margem')
        
        if TremVazio.objects.filter(previsao=previsao, margem=margem).exists():
            raise forms.ValidationError('Já existe um trem com esta previsão.')
        
        return previsao
