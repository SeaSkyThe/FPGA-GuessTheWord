from django.db import models
from django.contrib import admin
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

# Question - modelo das questoes 
class Question(models.Model):
    number = models.IntegerField('Question Number')
    difficulty = models.CharField(
        max_length=99, choices=difficulty_choices, verbose_name='Dificuldade', default='Easy')
    tip = models.TextField(verbose_name='Dica/Enunciado')
    subject = models.CharField(
        max_length=99, choices=subject_choices, verbose_name='Disciplina')
    answer = models.CharField(max_length=50, verbose_name='Resposta')

    def __str__(self) -> str:
        return f"ID: {self.id} - Numero: {self.number} - Disciplina: {self.subject} - Enunciado: {self.tip}"

    @classmethod
    def get_total_number_of_questions(cls, subject):
        return cls.objects.filter(subject=subject).count()
    
class Player(models.Model):
    nickname = models.CharField(max_length=40, verbose_name='Nickname', unique=True)

    def __str__(self) -> str:
        return f"{self.nickname}"


# Round - É a sessão do player, uma partida, um round.
class Round(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    subject = models.CharField(max_length=99, choices=subject_choices)
    score = models.DecimalField(decimal_places=0, max_digits=20, default=256)
    current_question = models.DecimalField(decimal_places=0, max_digits=4, default=1)

    def __str__(self) -> str:
        return f"Round: {self.id} - From: {self.player}"

    
# Model que guarda as respostas dos jogadores
class PlayerAnswer(models.Model): 
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    question_id = models.DecimalField(verbose_name='Question ID', decimal_places=0, max_digits=99)
    player_answer = models.CharField(max_length=99)
    position_in_game = models.DecimalField(verbose_name='Position', decimal_places=0, max_digits=5, default=0)
    
    class Meta:
        verbose_name_plural = "Players Answers"

    def __str__(self) -> str:
        return f"Answer \n  Round: {self.round.id} - From: {self.round.player}\n  Question ID: {self.question_id}\n  Player Answer: {self.player_answer}"
    
    @classmethod
    def get_all_answers_from_user(cls, nickname=None, subject=None, round=None):
        try:
            if(round == None):
                player = Player.objects.get(nickname=nickname)
                round = Round.objects.get(player=player, subject=subject)
            answers = cls.objects.filter(round=round)
            #print(f"\n\n{answers}\n\n")
            return answers
        except Exception as e:
            print(f"\nErro ao pegar respostas do user: {nickname}.\n")
            return None
        
    def is_correct(self):
        try:
            question = Question.objects.get(id=self.question_id, subject=self.round.subject)
            if(question.answer.lower() == self.player_answer.lower()):
                return True
            return False
        except:
            return False