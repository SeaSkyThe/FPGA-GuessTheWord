from django.contrib import admin
from .models import Question, Round, Player, PlayerAnswer
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
# Register your models here.


def adjust_indexes(query):
    new_question_number = 1
    for question in query.order_by('id'):
        # Atualiza o numero da questao
        question.number = new_question_number

        # Atualiza o numero da questao em todos os objetos de player answer
        player_answers = PlayerAnswer.objects.filter(round__subject=question.subject, question_number=question.number)
        for answer in player_answers:
            answer.question_number = new_question_number
            answer.save()
        
        # Atualiza o current question dos rounds existentes que estão nessa questão:
        player_rounds = Round.objects.filter(subject=question.subject, current_question=question.number)
        for round in player_rounds:
            round.current_question = new_question_number
            round.save()

        question.save()
        new_question_number = new_question_number + 1

@admin.action(description='Ajustar numero das questões de Circuitos')
def adjust_question_numbers_circuitos_digitais(modeladmin, request, queryset):
    query = Question.objects.filter(subject='circuitos_digitais')
    adjust_indexes(query)
        
@admin.action(description='Ajustar numero das questões de Arquitetura')
def adjust_question_numbers_arquitetura_de_computadores(modeladmin, request, queryset):
    new_question_number = 1
    query = Question.objects.filter(subject='arquitetura_de_computadores')
    adjust_indexes(query)

@admin.action(description='Ajustar numero das questões de SO1')
def adjust_question_numbers_sistemas_operacionais_1(modeladmin, request, queryset):
    new_question_number = 1
    query = Question.objects.filter(subject='sistemas_operacionais_1')
    adjust_indexes(query)

@admin.action(description='Ajustar numero das questões de SO2')
def adjust_question_numbers_sistemas_operacionais_2(modeladmin, request, queryset):
    new_question_number = 1
    query = Question.objects.filter(subject='sistemas_operacionais_2')
    adjust_indexes(query)

class QuestionFilter(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ["number", "difficulty", "subject", "tip", "answer"]
    list_filter = ["difficulty", "subject"]
    actions=[adjust_question_numbers_circuitos_digitais, 
             adjust_question_numbers_arquitetura_de_computadores, 
             adjust_question_numbers_sistemas_operacionais_1, 
             adjust_question_numbers_sistemas_operacionais_2]

class RoundFilter(admin.ModelAdmin):
    list_display = ["player", "subject", "score", "current_question"]
    list_filter = ["subject"]

class PlayerAnswerFilter(admin.ModelAdmin):
    list_display = ["round", "question_number", "player_answer", "position_in_game", "is_final_answer"]
    list_filter = ['round__player', 'round__subject', ]

admin.site.register(Question, QuestionFilter)
admin.site.register(Round, RoundFilter)
admin.site.register(Player)
admin.site.register(PlayerAnswer, PlayerAnswerFilter)
