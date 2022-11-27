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

# Question - o nome é descritivo
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


# Round - É a sessão do player, uma partida, um round.
class Round(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    subject = models.CharField(max_length=99, choices=subject_choices)
    score = models.DecimalField(decimal_places=0, max_digits=20, default=256)
    current_question = models.DecimalField(decimal_places=0, max_digits=4, default=0)

    def __str__(self) -> str:
        return f"Round: {self.id} - From: {self.player}"

    
# Model que guarda as respostas dos jogadores
class PlayerAnswer(models.Model): 
    round = models.ForeignKey(Round, on_delete=models.CASCADE)
    question_id = models.DecimalField(verbose_name='Question ID', decimal_places=0, max_digits=99)
    player_answer = models.CharField(max_length=99)
    
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