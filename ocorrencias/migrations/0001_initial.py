# Generated by Django 5.2.1 on 2025-07-07 00:36

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('quartos', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocorrencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField()),
                ('data_registro', models.DateField(auto_now_add=True)),
                ('resolvido', models.BooleanField(default=False)),
                ('data_resolvido', models.DateTimeField(blank=True, null=True)),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('quarto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='quartos.quarto')),
            ],
        ),
    ]
