# Generated by Django 3.2.16 on 2022-12-12 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_alter_round_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='playeranswer',
            name='position_in_game',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5, verbose_name='Position'),
        ),
    ]
