# Generated by Django 5.0.2 on 2024-07-18 18:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('previsao_trens', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TremVazio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefixo', models.CharField(max_length=100)),
                ('ferrovia', models.CharField(choices=[('MRS', 'MRS'), ('RUMO', 'RUMO'), ('VLI', 'VLI')], max_length=50)),
                ('loco_1', models.CharField(max_length=100)),
                ('loco_2', models.CharField(blank=True, max_length=100, null=True)),
                ('loco_3', models.CharField(blank=True, max_length=100, null=True)),
                ('loco_4', models.CharField(blank=True, max_length=100, null=True)),
                ('loco_5', models.CharField(blank=True, max_length=100, null=True)),
                ('previsao', models.DateTimeField(blank=True, null=True)),
                ('eot', models.CharField(max_length=100)),
                ('qt_graos', models.IntegerField(blank=True, null=True)),
                ('qt_ferti', models.IntegerField(blank=True, null=True)),
                ('qt_celul', models.IntegerField(blank=True, null=True)),
                ('qt_acuca', models.IntegerField(blank=True, null=True)),
                ('qt_contei', models.IntegerField(blank=True, null=True)),
                ('margem', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='cargo',
        ),
        migrations.CreateModel(
            name='Restricao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('terminal', models.CharField(max_length=50)),
                ('mercadoria', models.CharField(max_length=50)),
                ('comeca_em', models.DateTimeField()),
                ('termina_em', models.DateTimeField()),
                ('porcentagem', models.IntegerField()),
                ('motivo', models.CharField(max_length=50)),
                ('comentario', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
                ('ferrovia', models.CharField(choices=[('RUMO', 'RUMO'), ('MRS', 'MRS'), ('VLI', 'VLI')], max_length=50)),
                ('comentario', models.CharField(max_length=100)),
                ('posicao_previsao', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]