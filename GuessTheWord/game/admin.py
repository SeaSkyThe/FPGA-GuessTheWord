from django.contrib import admin
from .models import Question, Round, Player, PlayerAnswer
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
# Register your models here.


def adjust_indexes(query):
    new_question_number = 1
    for obj in query.order_by('id'):
        new_obj = obj
        obj.delete()
        new_obj.number = new_question_number
        new_obj.save()
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
    list_display = ["number", "difficulty", "subject", "tip", "answer"]
    list_filter = ["difficulty", "subject"]
    actions=[adjust_question_numbers_circuitos_digitais, 
             adjust_question_numbers_arquitetura_de_computadores, 
             adjust_question_numbers_sistemas_operacionais_1, 
             adjust_question_numbers_sistemas_operacionais_2]

class RoundFilter(admin.ModelAdmin):
    list_display = ["player", "subject", "score", "current_question"]
    list_filter = ["subject"]

admin.site.register(Question, QuestionFilter)
admin.site.register(Round, RoundFilter)
admin.site.register(Player)
admin.site.register(PlayerAnswer)
