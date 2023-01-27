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
        max_length=99, choices=difficulty_choices, verbose_name='Dificuldade', default='Easy') # Campo dificuldade
    tip = models.TextField(verbose_name='Dica/Enunciado') # Campo enunciado
    subject = models.CharField(
        max_length=99, choices=subject_choices, verbose_name='Disciplina') # Campo disciplina
    answer = models.CharField(max_length=50, verbose_name='Resposta') # Campo resposta

    def __str__(self) -> str:
        return f"ID: {self.id} - Numero: {self.number} - Disciplina: {self.subject} - Enunciado: {self.tip}"

    class Meta:
        unique_together = ('number', 'subject',)
        
    @classmethod
    def get_total_number_of_questions(cls, subject):
        return cls.objects.filter(subject=subject).count()

# Modelo do jogador
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
    
    def get_next_question(self):
        questions = Question.objects.order_by('number').filter(subject=self.subject)
        
        if(self.current_question == questions.last().number):
            return self.current_question
        
        next_question_number = self.current_question + 1
        next_question = None
        
        while(True):
            try:
                next_question = questions.get(number=next_question_number)
                return next_question
            except Question.DoesNotExist:
                next_question_number = next_question_number + 1
        
        
    def get_next_question_number(self):
        question = self.get_next_question()
        return question
    
    # Faz uma consulta no banco para pegar todas as respostas dos jogadores
    def get_all_player_answers(self):
        answers = PlayerAnswer.objects.filter(round=self)
        return answers 
    
    # Consulta o numero total de questões:
    def get_total_number_of_questions(self):
        return Question.get_total_number_of_questions(subject=self.subject)
        
    # Verifica, quantas questões ja foram respondidas
    def get_number_of_questions_answered(self):
        answers = self.get_all_player_answers()
        questions_answered = []
        for answer in answers:
            if(not answer.question_number in questions_answered):
                questions_answered.append(answer.question_number)
        
        return len(questions_answered)
    
    # Verifica quantas questões foram respondidas corretamente
    def get_number_of_questions_answered_correctly(self):
        answers = self.get_all_player_answers()
        questions_answered_correctly = []
        for answer in answers:
            try:
                question = Question.objects.filter(number=answer.question_number, subject=self.subject).first()
                if(question.answer.lower() == answer.player_answer.lower()): # Se a resposta da questao, for igual a dada pelo player, salvamos
                    if(not answer.question_number in questions_answered_correctly):  # Evitar duplicadas
                        questions_answered_correctly.append(answer.question_number)
            except:
                pass
        
        return len(questions_answered_correctly)

    # Verifica o numero total de tentativas
    def get_number_of_tries(self):
        answers = self.get_all_player_answers()
        return len(answers)
    
    # Verifica o numero total de tentativas certas
    def get_number_of_correct_tries(self):
        answers = self.get_all_player_answers()
        correct_answers = []
        for answer in answers:
            try:
                question = Question.objects.filter(number=answer.question_number, subject=self.subject).first()
                if(question.answer.lower() == answer.player_answer.lower() and answer.is_final_answer):
                    if(not answer in correct_answers):
                        correct_answers.append(answer)
            except:
                pass
        
        return len(correct_answers)
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