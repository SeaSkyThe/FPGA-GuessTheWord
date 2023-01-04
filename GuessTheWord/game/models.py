from django.db import models
from django.contrib import admin
import json
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

    class Meta:
        unique_together = ('number', 'subject',)
        
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
    score = models.DecimalField(decimal_places=0, max_digits=20, default=64)
    current_question = models.DecimalField(decimal_places=0, max_digits=4, default=1)

    def __str__(self) -> str:
        return f"Round: {self.id} - From: {self.player}"

    
# Model que guarda as respostas(tentativas) dos jogadores
# Nota-se que para cada questão, podemos ter varias respostas(tentativas)
# Cada instancia de PlayerAnswer indica uma linha preenchida no jogo
class PlayerAnswer(models.Model): 
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    question_number = models.DecimalField(verbose_name='Question Number', decimal_places=0, max_digits=99)
    player_answer = models.CharField(verbose_name='Player Answer', max_length=99)
    position_in_game = models.DecimalField(verbose_name='Position', decimal_places=0, max_digits=5, default=0)
    is_final_answer = models.BooleanField(verbose_name="Is Final Answer", default=False) # Final Answer indicates if it is the last answer from the user (either correct answer, or the user used all tries)
    
    class Meta:
        verbose_name_plural = "Players Answers"

    def __str__(self) -> str:
        return f"\n\nAnswer  \n|  Round: {self.round.id}  \n|  From: {self.round.player}\n  \n|  Question Number: {self.question_number}\n  \n|  Player Answer: {self.player_answer}\n\n"
    
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
    
    @classmethod
    def get_all_answers_from_user_json(cls, nickname=None, subject=None, round=None, question_number=None):
        answers = cls.get_all_answers_from_user(nickname=nickname, subject=subject, round=round)
        answers_dict = {}
        if(round):
            c_subject = round.subject
        else:
            c_subject = subject
        number_of_questions = Question.get_total_number_of_questions(subject=c_subject)
        
        for i in range(1, number_of_questions+1):
            answers_dict[i] = {}

        for answer in answers:
            answers_dict[int(answer.question_number)][int(answer.position_in_game)] = answer.player_answer
        
        if(question_number):
            return json.dumps(answers_dict[question_number])

        return json.dumps(answers_dict)

    
    def is_correct(self):
        try:
            question = Question.objects.get(id=self.question_number, subject=self.round.subject)
            if(question.answer.lower() == self.player_answer.lower()):
                return True
            return False
        except:
            return False