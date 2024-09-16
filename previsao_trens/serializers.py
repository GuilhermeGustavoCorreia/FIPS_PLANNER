from rest_framework import serializers 
from .models        import Trem, Mercadoria, Terminal


class TremSerializer(serializers.ModelSerializer):
    mercadoria = serializers.SlugRelatedField(
        queryset=Mercadoria.objects.all(),
        slug_field='nome'  # Campo na tabela Mercadoria que será usado como identificador
    )

    class Meta:
        model = Trem
        fields = '__all__'


class TremSerializerToSend(serializers.ModelSerializer):
    
    mercadoria = serializers.SlugRelatedField(
        queryset=Mercadoria.objects.all(),
        slug_field='nome'  # Campo que será exibido no lugar do ID (ajuste para o campo correto)
    )
    terminal = serializers.SlugRelatedField(
        queryset=Terminal.objects.all(),
        slug_field='nome'  # Campo que será exibido no lugar do ID (ajuste para o campo correto)
    )
    
    class Meta:
        model = Trem
        # Excluindo os campos que não queremos retornar na resposta
        exclude = ['id', 'posicao_previsao', 'translogic', 'created_at', 'created_by']