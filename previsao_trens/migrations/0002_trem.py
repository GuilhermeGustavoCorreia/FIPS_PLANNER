# Generated by Django 5.0.2 on 2024-04-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('previsao_trens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefixo', models.CharField(max_length=100)),
                ('os', models.IntegerField()),
                ('origem', models.CharField(max_length=50)),
                ('local', models.CharField(max_length=50)),
                ('destino', models.CharField(max_length=50)),
                ('terminal', models.CharField(max_length=50)),
                ('mercadoria', models.CharField(max_length=50)),
                ('vagoes', models.IntegerField()),
                ('previsao', models.DateTimeField()),
                ('comentario', models.CharField(max_length=100)),
            ],
        ),
    ]