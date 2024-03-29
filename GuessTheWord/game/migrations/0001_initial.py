# Generated by Django 3.2.16 on 2022-10-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tip', models.TextField(verbose_name='Dica/Enunciado')),
                ('discipline', models.CharField(choices=[('circuitos_digitais', 'Circuitos Digitais'), ('arquitetura_de_computadores', 'Arquitetura de Computadores'), ('sistemas_operacionais_1', 'Sistemas Operacionais 1'), ('sistemas_operacionais_2', 'Sistemas Operacionais 2')], max_length=99, verbose_name='Disciplina')),
                ('answer', models.CharField(max_length=50, verbose_name='Resposta')),
            ],
        ),
    ]
