from rest_framework import serializers 
from .models        import Trem, Mercadoria


class TremSerializer(serializers.ModelSerializer):
    mercadoria = serializers.SlugRelatedField(
        queryset=Mercadoria.objects.all(),
        slug_field='nome'  # Campo na tabela Mercadoria que será usado como identificador
    )

    class Meta:
        model = Trem
        fields = '__all__'