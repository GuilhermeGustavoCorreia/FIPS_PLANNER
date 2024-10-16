from    django.db                   import models, transaction
from    django.contrib.auth.models  import AbstractUser
from    django.conf                 import settings
from    django.forms.models         import model_to_dict
from    django.db.models            import F
from    datetime                    import timedelta
#import  requests
import  pandas as pd

class Segmento(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome
    
class Mercadoria(models.Model):

    nome     = models.CharField(max_length=100)
    segmento = models.ForeignKey(Segmento, on_delete=models.CASCADE, related_name='mercadorias')

    def __str__(self):
        return self.nome
    
class Terminal(models.Model):

    nome            = models.CharField(max_length=100)
    ordem           = models.IntegerField()
    margem          = models.CharField(max_length=100) 
    patio           = models.CharField(max_length=100) 
    tempo_encoste   = models.IntegerField()
    segmento        = models.ForeignKey(Segmento, on_delete=models.CASCADE, related_name='terminais')

    def __str__(self):
        return self.nome

class Trem(models.Model):

    prefixo     = models.CharField(max_length=100)
    os          = models.IntegerField()
    origem      = models.CharField(max_length=50)
    local       = models.CharField(max_length=50)
    destino     = models.CharField(max_length=50)
    terminal    = models.ForeignKey(Terminal, on_delete=models.CASCADE, null=True, blank=True) 
    mercadoria  = models.ForeignKey(Mercadoria, on_delete=models.CASCADE)
    vagoes      = models.IntegerField()
    previsao    = models.DateTimeField(null=True, blank=True)
    encoste     = models.DateTimeField(null=True, blank=True)
    ferrovia    = models.CharField(max_length=50, choices=[('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')])
    comentario  = models.CharField(max_length=100, null=True, blank=True)
    
    posicao_previsao = models.IntegerField(default=0)
    translogic       = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def update_position(self, new_position):

        old_position = self.posicao_previsao

        if old_position > new_position: direction = "para cima"
        if old_position < new_position: direction = "para baixo"

        if direction == "para cima":
            
            Trem.objects.filter(
                
                posicao_previsao__gt = new_position - 1,
                posicao_previsao__lt = self.posicao_previsao,
                previsao__date       = self.previsao
                
            ).update(posicao_previsao=F('posicao_previsao') + 1)

        if direction == "para baixo":

            Trem.objects.filter(
                
                posicao_previsao__gt = self.posicao_previsao,
                posicao_previsao__lt = new_position + 1,
                previsao__date       = self.previsao
            
            ).update(posicao_previsao=F('posicao_previsao') - 1)

        self.posicao_previsao = new_position
        super().save()

    def save(self, *args, **kwargs):
        
        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as Navegacao
        with transaction.atomic(): 

            #region em caso de edicao
            if not self._state.adding:

                trem_atual      = Trem.objects.get(pk=self.pk)
                previsao_antiga = trem_atual.previsao.date()    if trem_atual.previsao  else None
                nova_previsao   = self.previsao.date()          if self.previsao        else None
                
                self.posicao_previsao = trem_atual.posicao_previsao
                if nova_previsao:
                    
                    if previsao_antiga != nova_previsao:

                        self.posicao_previsao = 0

                        Trem.objects.filter(
                            
                            posicao_previsao__gt    = trem_atual.posicao_previsao, 
                            previsao__year          = previsao_antiga.year, 
                            previsao__month         = previsao_antiga.month, 
                            previsao__day           = previsao_antiga.day
                            
                        ).update(posicao_previsao=F('posicao_previsao') - 1) 

                        Trem.objects.filter(
                            
                            previsao__year  = nova_previsao.year, 
                            previsao__month = nova_previsao.month, 
                            previsao__day   = nova_previsao.day
                        
                        ).update(posicao_previsao=F('posicao_previsao') + 1)


                super().delete(*args, **kwargs)
                
                if trem_atual.previsao: 
                    
                    self.encoste = (trem_atual.previsao + timedelta(hours=trem_atual.terminal.tempo_encoste))
                    CalculoNavegacaoAntigo = Navegacao(trem_atual.terminal.nome, trem_atual.ferrovia, trem_atual.mercadoria.nome)
                    CalculoNavegacaoAntigo.atualizar(trem_atual)

            #endregion

            self.prefixo = self.prefixo.upper()

            #ajustando previsão (colocando este trem como o primeiro da lista)
            if self._state.adding and self.previsao:

                Trem.objects.filter(
                    
                    previsao__year  = self.previsao.year, 
                    previsao__month = self.previsao.month, 
                    previsao__day   = self.previsao.day
                    
                ).update(posicao_previsao=F('posicao_previsao') + 1)

            #inserindo tempo de encoste
            if self.previsao: 
                
                self.encoste = (self.previsao + timedelta(hours=self.terminal.tempo_encoste))
    
                super().save(*args, **kwargs)
                CalculoNavegacao = Navegacao(self.terminal.nome, self.ferrovia, self.mercadoria.nome)
                CalculoNavegacao.atualizar(self)

            else:

                super().save(*args, **kwargs)    

    def delete(self, *args, **kwargs):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA as Navegacao
       
        with transaction.atomic():  # Garante que as mudanças sejam atômicas
            
            if self.previsao:    
                #ajustando previsão 
                Trem.objects.filter(
                    
                    posicao_previsao__gt    = self.posicao_previsao, 
                    previsao__year          = self.previsao.year, 
                    previsao__month         = self.previsao.month, 
                    previsao__day           = self.previsao.day
                
                ).update(posicao_previsao=F('posicao_previsao') - 1)

                super().delete(*args, **kwargs)
                
                CalculoNavegacao = Navegacao(self.terminal.nome, self.ferrovia, self.mercadoria.nome)
                CalculoNavegacao.atualizar(self)

            else:

                super().delete(*args, **kwargs)

    def to_slice(self, slice_01, slice_02):
  
        with transaction.atomic():
            
            self.delete() 
            Trem.objects.create(**slice_01, created_by=self.created_by)
            Trem.objects.create(**slice_02, created_by=self.created_by)

    @staticmethod
    def update_nitro():

        def get_access_token():

            url = "https://sso.ops.ti.rumolog.com/auth/realms/tlg/protocol/openid-connect/token"
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            payload = {
                'client_id'     : 'previsao-chegada',
                'grant_type'    : 'client_credentials',
                'client_secret' : 'b74f24e3-4c09-4c2a-a3ac-bf088c860111',
                'scope'         : 'openid'
            }

            response = requests.post(url, headers=headers, data=payload)
            
            if response.status_code == 200:
                # Parse the token from response
                token = response.json().get('access_token')
                return token
            
            else:
                # Handle errors
                return "Error: " + response.text
        
        def access_previsao_api(token):

            url = "https://api.rumolog.com/v1/previsao/zpg"
            # headers = {
            #     'Authorization': f'Bearer {token}',
            #     'Content-Type': 'application/json'
            # }

            # response = requests.get(url, headers=headers)

            # if response.status_code == 200:
            #     return response.json()  # Retorna os dados da previsão
            # else:
            #     raise Exception("API request failed with status code " + str(response.status_code) + ": " + response.text)
            

        access_token = get_access_token()

        lista_de_trens = access_previsao_api(access_token)["data"]
        


    def __str__(self):
        return f"{self.prefixo} -  {self.terminal} - {self.mercadoria} - {self.previsao}"
    
class Restricao(models.Model):

    terminal    = models.CharField(max_length=50)
    mercadoria  = models.CharField(max_length=50)

    comeca_em   = models.DateTimeField()
    termina_em  = models.DateTimeField()

    porcentagem = models.IntegerField()

    motivo      = models.CharField(max_length=50)
    comentario  = models.CharField(max_length=50) 

    aplicacao_status = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



    @staticmethod
    def json_to_form(json_data):

        form_data = {
        'terminal'      : json_data.get('TERMINAL', ''),
        'mercadoria'    : json_data.get('SEGMENTO', ''),
        'comeca_em'     : json_data.get('INICIO', ''),
        'termina_em'    : json_data.get('FINAL', ''),
        'porcentagem'   : json_data.get('PCT', 0),
        'motivo'        : json_data.get('MOTIVO', ''),
        'comentario'    : json_data.get('COMENTARIO', '')
        }
        return form_data

    def excluir_restricao(self):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA

        with transaction.atomic():
            
            restricao_antiga = model_to_dict(self)
            self.delete()

        try: #CASO ESTEJA FORA DA DATA
            try:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"])
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
            
            except KeyError:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"], DIA_ANTERIOR=True)
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
        
        except IndexError:
            pass

    @classmethod
    def criar_restricao(cls, data, user):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA   import NAVEGACAO_DESCARGA
        from previsao_trens.packages.RESTRICAO.VALIDAR          import VALIDAR_RESTRICAO
        from .forms                                             import RestricaoForm

        with transaction.atomic():
            
            restricao_form = RestricaoForm(data)
            
            if restricao_form.is_valid():

                restricao = restricao_form.cleaned_data
                é_valida = VALIDAR_RESTRICAO(restricao)

                if not é_valida["STATUS"]:
                    return {"status": False, "descricao": é_valida["DESCRICAO"], "errors": None, "form": restricao_form}
            
                try: #CASO ESTEJA FORA DA DATA
                    
                    try:
                        
                        navegacao = NAVEGACAO_DESCARGA(restricao["terminal"], None, restricao["mercadoria"])
                        status_restricao = navegacao.EDITAR_RESTRICAO(restricao, "INSERIR")
                    
                    except KeyError:
                        
                        navegacao = NAVEGACAO_DESCARGA(restricao["terminal"], None, restricao["mercadoria"], DIA_ANTERIOR=True)
                        status_restricao = navegacao.EDITAR_RESTRICAO(restricao, "INSERIR")
                    
                    
                
                except IndexError:
                    
                    status_restricao = "NAO_INSERIDA"
                    pass

                restricao_objeto = restricao_form.save(commit=False)
                restricao_objeto.aplicacao_status = status_restricao
                restricao_objeto.created_by = user
                restricao_objeto.save()

                return {"status": True, "descricao": "Restrição criada com sucesso!", "errors": None, "form": restricao_form}
            
            else:

                return { "status": False, "descricao": None, "errors": restricao_form.errors, "form": restricao_form }

    def save(self, *args, **kwargs):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA   import NAVEGACAO_DESCARGA

        try: #CASO ESTEJA FORA DA DATA

            dict_restricao = model_to_dict(self)

            try:
                
                navegacao = NAVEGACAO_DESCARGA(self.terminal, None, self.mercadoria)
                status_restricao = navegacao.EDITAR_RESTRICAO(dict_restricao, "INSERIR")
            
            except KeyError:
                
                navegacao = NAVEGACAO_DESCARGA(self.terminal, None, self.mercadoria, DIA_ANTERIOR=True)
                status_restricao = navegacao.EDITAR_RESTRICAO(dict_restricao, "INSERIR")
                 
        except IndexError:
            
            status_restricao = "NAO_INSERIDA"
            pass

        self.aplicacao_status = status_restricao

        super().save(*args, **kwargs)           

    def delete(self, *args, **kwargs):

        from previsao_trens.packages.descarga.EDITAR_DESCARGA import NAVEGACAO_DESCARGA

        with transaction.atomic():
            
            restricao_antiga = model_to_dict(self)
            super().delete(*args, **kwargs)

        try: #CASO ESTEJA FORA DA DATA
            try:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"])
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
            
            except KeyError:
                
                navegacao = NAVEGACAO_DESCARGA(restricao_antiga["terminal"], None, restricao_antiga["mercadoria"], DIA_ANTERIOR=True)
                navegacao.EDITAR_RESTRICAO(restricao_antiga, "REMOVER")
        
        except IndexError:
            pass

    def __str__(self):

        return (f"{ self.terminal } - { self.motivo }")

class TremVazio(models.Model):

    prefixo      = models.CharField(max_length=100)
    ferrovia     = models.CharField(max_length=50, choices=[('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')])
    eot          = models.CharField(max_length=3,  choices=[('Sim', 'Sim'), ('Nao', 'Nao')])
    margem       = models.CharField(max_length=8,  choices=[('Direita', 'Direita'), ('Esquerda', 'Esquerda')], blank=True)

    loco_1       = models.CharField(max_length=100)
    loco_2       = models.CharField(max_length=100, blank=True, null=True)
    loco_3       = models.CharField(max_length=100, blank=True, null=True)
    loco_4       = models.CharField(max_length=100, blank=True, null=True)
    loco_5       = models.CharField(max_length=100, blank=True, null=True)
    
    previsao     = models.DateTimeField(blank=True, null=True)
    partida_real = models.DateTimeField(blank=True, null=True)

    qt_graos     = models.IntegerField(blank=True, null=True)
    qt_ferti     = models.IntegerField(blank=True, null=True)
    qt_celul     = models.IntegerField(blank=True, null=True)
    qt_acuca     = models.IntegerField(blank=True, null=True)
    qt_contei    = models.IntegerField(blank=True, null=True)

    comentario   = models.CharField(max_length=100, blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    created_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        
        from  previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2 import Condensados
        
        super().save(*args, **kwargs)

        dict_trem = model_to_dict(self)
    
        Condensados().atualizar_previsao(dict_trem)

    def delete(self, *args, **kwargs):

        from previsao_trens.packages.PROG_SUBIDA.CALCULAR_SUBIDA_V2 import Condensados
              
        super().delete(*args, **kwargs)

        try:
            
            dict_trem = model_to_dict(self)
            Condensados().atualizar_previsao(dict_trem)

        except IndexError:
            pass

    @staticmethod   
    def read_excel(excel_file, user):
        
        try:

            def process_eot(x):
                x = str(x).lower()
                return x.startswith('s') if x != '0' else False

            excel_data = pd.read_excel(excel_file, sheet_name="SUBIDA", usecols="AD:AM") 
            
            df_previsao_subida_dir = excel_data.iloc[14:35]
            df_previsao_subida_esq = excel_data.iloc[37:51]
            
            renamed_columns = {

                'Unnamed: 29': 'prefixo',
                'Unnamed: 30': 'ferrovia',
                'Unnamed: 31': 'loco_1', 
                'Unnamed: 32': 'loco_2', 
                'Unnamed: 33': 'loco_3',
                'Unnamed: 34': 'loco_4',
                'Unnamed: 35': 'loco_5',
                'Unnamed: 36': 'previsao',
                'Unnamed: 37': 'eot',
                'Unnamed: 38': 'vagoes'

            }
            
            df_previsao_subida_dir = df_previsao_subida_dir.rename(columns=renamed_columns)
            df_previsao_subida_esq = df_previsao_subida_esq.rename(columns=renamed_columns)
            
            df_previsao_subida_dir = df_previsao_subida_dir.dropna(subset=['prefixo'])
            df_previsao_subida_esq = df_previsao_subida_esq.dropna(subset=['prefixo'])


            loco_columns = ['loco_1', 'loco_2', 'loco_3', 'loco_4', 'loco_5']
            
            df_previsao_subida_dir = df_previsao_subida_dir.fillna(0)
            df_previsao_subida_esq = df_previsao_subida_esq.fillna(0)
            
            df_previsao_subida_dir[loco_columns] = df_previsao_subida_dir[loco_columns].astype(int)
            df_previsao_subida_esq[loco_columns] = df_previsao_subida_esq[loco_columns].astype(int)

            locos = ['loco_2', 'loco_3', 'loco_4', 'loco_5']
            
            for loco in locos:
                df_previsao_subida_dir[loco] = df_previsao_subida_dir[loco].astype(str).str.zfill(4)
                df_previsao_subida_esq[loco] = df_previsao_subida_esq[loco].astype(str).str.zfill(4)
        
            df_previsao_subida_dir[locos] = df_previsao_subida_dir[locos].replace('0000', '')
            df_previsao_subida_esq[locos] = df_previsao_subida_esq[locos].replace('0000', '')

            df_previsao_subida_dir['prefixo'] = df_previsao_subida_dir['prefixo'].apply(lambda x: x.split('/')[0])
            df_previsao_subida_dir['prefixo'] = df_previsao_subida_dir['prefixo'].apply(lambda x: x.split('-')[0])

            df_previsao_subida_esq['prefixo'] = df_previsao_subida_esq['prefixo'].apply(lambda x: x.split('/')[0])
            df_previsao_subida_esq['prefixo'] = df_previsao_subida_esq['prefixo'].apply(lambda x: x.split('-')[0])

            df_previsao_subida_dir['prefixo'] = df_previsao_subida_dir['prefixo'].str.replace(' ', '', regex=True)
            df_previsao_subida_esq['prefixo'] = df_previsao_subida_esq['prefixo'].str.replace(' ', '', regex=True)

            df_previsao_subida_dir['eot'] = df_previsao_subida_dir['eot'].apply(process_eot)
            df_previsao_subida_esq['eot'] = df_previsao_subida_esq['eot'].apply(process_eot)

            df_previsao_subida_dir['previsao'] = pd.to_datetime(df_previsao_subida_dir['previsao'])
            df_previsao_subida_esq['previsao'] = pd.to_datetime(df_previsao_subida_esq['previsao'])

            df_previsao_subida_dir['margem'] = 'Direita'
            df_previsao_subida_esq['margem'] = 'Esquerda'

            df_previsao_subida = pd.concat([df_previsao_subida_esq, df_previsao_subida_dir], ignore_index=True).sort_values(by='previsao').reset_index(drop=True)

            df_previsao_subida['qt_graos'] = 0
            df_previsao_subida['qt_ferti'] = 0
            df_previsao_subida['qt_celul'] = 0
            df_previsao_subida['qt_acuca'] = 0
            df_previsao_subida['qt_contei'] = 0

            df_previsao_subida.loc[
                    (df_previsao_subida['prefixo'].str.len() == 3) & 
                    (~df_previsao_subida['prefixo'].str.startswith('U')) & 
                    (df_previsao_subida['prefixo'].str.startswith('R')), 
                'qt_acuca'] = 82

            df_previsao_subida.loc[
                    (df_previsao_subida['prefixo'].str.len() == 3) & 
                    (~df_previsao_subida['prefixo'].str.startswith('U')) & 
                    (df_previsao_subida['prefixo'].str.startswith('L')), 
                'qt_celul'] = 64
                     
            df_previsao_subida.loc[
                (df_previsao_subida['prefixo'].str.len() == 3) & 
                (~df_previsao_subida['prefixo'].str.startswith('U')) & 
                (df_previsao_subida['prefixo'].str.startswith(('I', 'Y'))) & 
                (pd.to_numeric(df_previsao_subida['prefixo'].str[1:], errors='coerce').notna()) &  # Verifica se é numérico
                (pd.to_numeric(df_previsao_subida['prefixo'].str[1:], errors='coerce') < 82) & 
                (df_previsao_subida['margem'] == 'Direita'), 
                'qt_graos'
            ] = 83

            df_previsao_subida.loc[
                (df_previsao_subida['prefixo'].str.len() == 3) & 
                (~df_previsao_subida['prefixo'].str.startswith('U')) & 
                (df_previsao_subida['prefixo'].str.startswith(('I', 'Y'))) & 
                (pd.to_numeric(df_previsao_subida['prefixo'].str[1:], errors='coerce').notna()) &  # Verifica se é numérico
                (pd.to_numeric(df_previsao_subida['prefixo'].str[1:], errors='coerce') < 82) & 
                (df_previsao_subida['margem'] == 'Esquerda'), 
                'qt_graos'
            ] = 78

            mask = (df_previsao_subida['prefixo'].str.len() == 3) & df_previsao_subida['prefixo'].str.startswith('N')  # Máscara para prefixos que começam com 'N'
            df_previsao_subida.loc[mask, 'qt_ferti'] = df_previsao_subida.loc[mask, 'vagoes'].apply(lambda x: x if isinstance(x, (int, float)) else 0)

            print(f"previao subida: {df_previsao_subida}")

            for _, row in df_previsao_subida.iterrows():
                # Convertendo a linha para dicionário
                dicionario = row.to_dict()

                trem_vazio = TremVazio(
                    prefixo     = dicionario['prefixo'],
                    ferrovia    = dicionario['ferrovia'],
                    eot='Sim' if dicionario['eot'] else 'Nao',  # Converter booleano para string
                    margem      = dicionario['margem'],
                    loco_1      = dicionario['loco_1'],
                    loco_2      = dicionario['loco_2']  or None,  # Usar None se a string for vazia
                    loco_3      = dicionario['loco_3']  or None,
                    loco_4      = dicionario['loco_4']  or None,
                    loco_5      =  dicionario['loco_5'] or None,
                    previsao    = dicionario['previsao'],
                    qt_graos    = dicionario['qt_graos'],
                    qt_ferti    = dicionario['qt_ferti'],
                    qt_celul    = dicionario['qt_celul'],
                    qt_acuca    = dicionario['qt_acuca'],
                    qt_contei   = dicionario['qt_contei'],
                    created_by  =  user
                )
                print(f"inserindo trem vazio: {trem_vazio}")
                trem_vazio.save()
        except:
            pass
    
    def __str__(self):
        return self.prefixo

class Usuario(AbstractUser):

    foto        = models.ImageField(upload_to="fotos_de_perfil", blank=True, default='anonimo.jpg' )
    USERNAME_FIELD = 'username'  # Define o campo usado para fazer login
    
    # REQUIRED_FIELDS deve conter todos os campos adicionais necessários além de username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Adicione 'nome' aos campos necessários
    
    def __str__(self):

        return  self.username
    
