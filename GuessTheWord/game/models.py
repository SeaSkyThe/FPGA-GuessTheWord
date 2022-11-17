from django.db import models
# Create your models here.
subject_choices = (
    ('circuitos_digitais', 'Circuitos Digitais'),
    ('arquitetura_de_computadores', 'Arquitetura de Computadores'),
    ('sistemas_operacionais_1', 'Sistemas Operacionais 1'),
    ('sistemas_operacionais_2', 'Sistemas Operacionais 2'),
)
difficulty_choices = (
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
)


class Question(models.Model):
    difficulty = models.CharField(
        max_length=99, choices=difficulty_choices, verbose_name='Dificuldade', default='Easy')
    tip = models.TextField(verbose_name='Dica/Enunciado')
    subject = models.CharField(
        max_length=99, choices=subject_choices, verbose_name='Disciplina')
    answer = models.CharField(max_length=50, verbose_name='Resposta')

    def __str__(self) -> str:
        return f"{self.id} - {self.subject} - {self.tip}"


class Player(models.Model):
    nickname = models.CharField(max_length=40, verbose_name='Nickname', unique=True)

    def __str__(self) -> str:
        return f"{self.nickname}"


class Round(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    subject = models.CharField(max_length=99, choices=subject_choices)
    score = models.DecimalField(decimal_places=0, max_digits=20, default=256)
    current_question = models.DecimalField(decimal_places=0, max_digits=4, default=0)

    def __str__(self) -> str:
        return f"Round: {self.id} - From: {self.player}"
