# Generated by Django 3.2.16 on 2022-11-27 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_alter_playeranswer_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='round',
            name='answered_questions',
        ),
    ]