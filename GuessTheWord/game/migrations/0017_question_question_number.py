# Generated by Django 3.2.16 on 2022-12-12 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_remove_question_question_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_number',
            field=models.IntegerField(default=0, verbose_name='Question Number'),
            preserve_default=False,
        ),
    ]
