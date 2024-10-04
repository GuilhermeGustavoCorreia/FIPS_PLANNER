


from django                     import forms
from django.forms.widgets       import DateTimeInput, TextInput, NumberInput, Select, Textarea, RadioSelect
from django.contrib.auth.forms  import AuthenticationForm
from django.core.exceptions     import ValidationError

from .models    import Trem, Restricao, TremVazio, Terminal, Mercadoria
from datetime   import datetime, timedelta, time

import  os
import  json
import  pandas as pd


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

    class Meta:
        model = Trem
        fields = '__all__'
        
        widgets = {
            'prefixo':      forms.TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Prefixo'}),
            'os':           forms.NumberInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'OS'}),
            'origem':       forms.TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Origem'}),
            'local':        forms.TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Local'}),
            'destino':      forms.TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Destino'}),
            'mercadoria':   forms.Select(attrs={'class': 'INPUT INPUT_G', 'id': 'id_mercadoria', 'onchange': 'updateTerminals()'}),
            'terminal':     forms.Select(attrs={'class': 'INPUT INPUT_M', 'id': 'id_terminal'}),
            'vagoes':       forms.NumberInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Vagões'}),
            'previsao':     forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', 'placeholder': 'Previsão'}),
            'comentario':   forms.Textarea(attrs={'class': 'INPUT INPUT_G', 'placeholder': 'Comentário', 'rows': 2}),
            'ferrovia':     forms.RadioSelect(attrs={'class': 'INPUT INPUT_RADIO'})
        }

    def __init__(self, *args, **kwargs):
        
        super(TremForm, self).__init__(*args, **kwargs)
        
        self.fields['ferrovia'].choices = [('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')]
        self.fields['ferrovia'].initial = 'RUMO'

        self.fields['comentario'].required          = False
        self.fields['posicao_previsao'].required    = False 
        self.fields['created_by'].required          = False 
        self.fields['encoste'].required             = False
        self.fields['translogic'].required          = False

    def clean(self):

        cleaned_data    = super().clean()
        previsao        = cleaned_data.get('previsao')
        mercadoria      = cleaned_data.get('mercadoria')
        terminal        = cleaned_data.get('terminal')
        prefixo         = cleaned_data.get('prefixo')
        ferrovia        = cleaned_data.get('ferrovia')
        destino         = cleaned_data.get('destino')

        #region Verificação de conflito
        trens_existentes = Trem.objects.filter(previsao=previsao, mercadoria=mercadoria, terminal=terminal)

        if self.instance.pk:  # Editando um trem existente
            trens_existentes = trens_existentes.exclude(pk=self.instance.pk)

        if trens_existentes.exists() and not all(trem.prefixo == prefixo for trem in trens_existentes):
            raise ValidationError("Erro: Não é permitido ter o mesmo terminal, previsão e mercadoria com prefixos diferentes.")
        #endregion

        #region Verificação de previsao
        periodo_vigente = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        data_arqs       = periodo_vigente["DATA_ARQ"].tolist()

        limite_minimo = datetime.combine(datetime.strptime(data_arqs[0], '%Y-%m-%d').date(), time(1, 0))
        limite_maximo = datetime.combine(datetime.strptime(data_arqs[5], '%Y-%m-%d').date(), time(0, 0)) + timedelta(days=1)

        if previsao and (previsao < limite_minimo or previsao > limite_maximo): 
            raise ValidationError("Erro: Não é possível inserir o trem fora do período de D-1 à D+4.")
        #endregion

        #region Verificação de terminais
        if terminal.nome == "SBR" and (ferrovia == "RUMO" or ferrovia == "VLI"):
  
            raise ValidationError("O Sistema esta configurado para receber somente trens MRS no terminal SBR.")
        

        if terminal.nome == "ECOPORTO" and (ferrovia == "RUMO" or ferrovia == "VLI"):
  
            raise ValidationError("O Sistema esta configurado para receber somente trens MRS no terminal ECOPORTO.")
        #endregion
        
        #region validacao de destino
        if terminal.margem == "ESQUERDA" and destino == "PSN":

            raise ValidationError("Este terminal esta localizado na margem esquerda, por favor mude o destino.")

        if terminal.margem == "DIREITA" and destino == "PCZ":

            raise ValidationError("Este terminal esta localizado na margem direita, por favor mude o destino.")


        #endregion

        return cleaned_data

class DividirTremForm(forms.ModelForm):
    # Campos adicionais para dividir o trem
    
    destino1    = forms.CharField(label='Destino 1', max_length=50)
    mercadoria1 = forms.ModelChoiceField(label='Mercadoria 1',  queryset=Mercadoria.objects.all())
    terminal1   = forms.ModelChoiceField(label='Terminal 1',    queryset=Terminal.objects.all())
    vagoes1     = forms.IntegerField(label='Vagões 1')
    previsao1   = forms.DateTimeField(label='Previsão 1', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    destino2    = forms.CharField(label='Destino 2', max_length=50)
    mercadoria2 = forms.ModelChoiceField(label='Mercadoria 2',  queryset=Mercadoria.objects.all())
    terminal2   = forms.ModelChoiceField(label='Terminal 2',    queryset=Terminal.objects.all())
    vagoes2     = forms.IntegerField(label='Vagões 2')
    previsao2   = forms.DateTimeField(label='Previsão 2', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    class Meta:
        
        model   = Trem
        fields  = ['prefixo', 'os', 'origem', 'local', 'ferrovia']  # apenas os campos diretamente no modelo Trem

    def __init__(self, *args, **kwargs):
        
        super(DividirTremForm, self).__init__(*args, **kwargs)

        self.fields['prefixo'].required     = False
        self.fields['os'].required          = False 
        self.fields['origem'].required      = False 
        self.fields['local'].required       = False
        self.fields['ferrovia'].required    = False

        self.fields['prefixo'].widget.attrs.update( {'class': 'form-control', 'placeholder': 'Prefixo',  'disabled': True})
        self.fields['os'].widget.attrs.update(      {'class': 'form-control', 'placeholder': 'OS',       'disabled': True})
        self.fields['origem'].widget.attrs.update(  {'class': 'form-control', 'placeholder': 'Origem',   'disabled': True})
        self.fields['local'].widget.attrs.update(   {'class': 'form-control', 'placeholder': 'Local',    'disabled': True})
        self.fields['ferrovia'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ferrovia', 'disabled': True})
        
        self.fields['mercadoria1'].widget.attrs.update({'onchange': 'updateTerminals1()'})
        self.fields['mercadoria2'].widget.attrs.update({'onchange': 'updateTerminals2()'})

        self.fields['destino1'].widget.attrs.update({'placeholder': 'destino'})
        self.fields['destino2'].widget.attrs.update({'placeholder': 'destino'})

        self.fields['vagoes1'].widget.attrs.update({'placeholder': 'vagões'})
        self.fields['vagoes2'].widget.attrs.update({'placeholder': 'vagões'})

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

            'motivo':      TextInput(attrs={'class': 'INPUT INPUT_P', 'placeholder': 'Motivo', 'maxlength': '2'}),
            'comentario':  Textarea(attrs={'class': 'INPUT INPUT_G', 'placeholder': 'Comentário', 'rows': 2}),

        }
    def __init__(self, *args, **kwargs):

        super(RestricaoForm, self).__init__(*args, **kwargs)
        self.fields['created_by'].required          = False 

class UploadFileForm(forms.Form):
    file = forms.FileField()

class TremVazioForm(forms.ModelForm):

    class Meta:
    
        model   = TremVazio
        fields  = '__all__'
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
            'previsao':     DateTimeInput(attrs={'type': 'datetime-local', 'class': 'INPUT INPUT_M', 'placeholder': 'Previsão', 'onchange': 'atualizarHorario()'}),
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

    def clean(self):
        
        cleaned_data    = super().clean()
        previsao        = cleaned_data.get('previsao')
        margem          = cleaned_data.get('margem')
        

        trens_existentes = TremVazio.objects.filter(previsao=previsao, margem=margem)
        if self.instance.pk:  # Editando um trem existente
            trens_existentes = trens_existentes.exclude(pk=self.instance.pk)

        if trens_existentes.exists():
            raise ValidationError('Já existe um trem com esta previsão.')
        
        # Verificação de data
        periodo_vigente = pd.read_csv(f"previsao_trens/src/PARAMETROS/PERIODO_VIGENTE.csv", sep=";", index_col=0)
        data_arqs       = periodo_vigente["DATA_ARQ"].tolist()

        limite_minimo = datetime.combine(datetime.strptime(data_arqs[1], '%Y-%m-%d').date(), time(1, 0))
        limite_maximo = datetime.combine(datetime.strptime(data_arqs[2], '%Y-%m-%d').date(), time(0, 0)) + timedelta(days=1)

        if previsao and (previsao < limite_minimo or previsao > limite_maximo): 
            raise ValidationError("Erro: Não é possível inserir o trem fora do período de D à D+1.")

        return cleaned_data

class TerminalForm(forms.ModelForm):
    
    class Meta:

        model = Terminal
        fields = ['nome', 'margem', 'patio', 'tempo_encoste']
        
        labels = {
            'nome'          : 'Nome',
            'margem'        : 'Margem',
            'patio'         : 'Pátio',
            'tempo_encoste' : 'Tempo de Encoste'
        }

        widgets = {
            'nome'          : forms.TextInput(attrs={'class': 'form-control'}),
            'margem'        : forms.TextInput(attrs={'class': 'form-control'}),
            'patio'         : forms.TextInput(attrs={'class': 'form-control'}),
            'tempo_encoste' : forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):

        cleaned_data    = super().clean()
        margem          = cleaned_data.get('margem')
        patio           = cleaned_data.get('patio')

        if margem == 'esquerda' and patio != 'PCZ':
            raise ValidationError({'patio': "O pátio deve ser 'PCZ' quando a margem é esquerda."})
        elif margem == 'direita' and patio not in ['PSN', 'PMC', 'PST']:
            raise ValidationError({'patio': "O pátio deve ser 'PSN', 'PMC' ou 'PST' quando a margem é direita."})

        return cleaned_data

