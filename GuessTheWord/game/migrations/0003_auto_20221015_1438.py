# Generated by Django 3.2.16 on 2022-10-15 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_player_round'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='discipline',
            new_name='subject',
        ),
        migrations.RenameField(
            model_name='round',
            old_name='discipline',
            new_name='subject',
        ),
    ]
