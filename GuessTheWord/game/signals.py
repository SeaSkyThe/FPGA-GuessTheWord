from django.db.models.signals import pre_delete, post_delete, pre_save, post_save 
from django.dispatch import receiver
from .models import Round, Question, PlayerAnswer
from .admin import adjust_indexes

@receiver(post_delete, sender=Question)
def reorder_questions(sender, instance, **kwargs):
    query = Question.objects.filter(subject=instance.subject)
    adjust_indexes(query)

@receiver(pre_delete, sender=Question)
def delete_player_answer(sender, instance, **kwargs):
    question_number = instance.number
    question_subject = instance.subject
    player_answers = PlayerAnswer.objects.filter(question_number=question_number, round__subject=question_subject)
    player_answers.delete()
    
@receiver(pre_save, sender=Question)
def update_player_answers(sender, instance, **kwargs):
    try:
        old_question = sender.objects.get(id=instance.id)
    except Question.DoesNotExist:  
        return None  

    question_number = old_question.number
    question_subject = old_question.subject
    player_answers = PlayerAnswer.objects.filter(question_number=question_number, round__subject=question_subject)
    
    for answer in player_answers:
        answer.question_number = instance.number
        answer.save()