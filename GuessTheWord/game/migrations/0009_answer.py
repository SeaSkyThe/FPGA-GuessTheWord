# Generated by Django 3.2.16 on 2022-11-27 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_alter_round_answered_questions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.DecimalField(decimal_places=0, max_digits=99, verbose_name='Question ID')),
                ('player_answer', models.CharField(max_length=99)),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.round')),
            ],
        ),
    ]
