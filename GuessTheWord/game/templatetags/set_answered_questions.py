from django import template
from game.models import Round
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.simple_tag
def set_answered_questions(round_obj: Round, list_of_answered_questions: list) -> list:
    return round_obj.set_answered_questions(list_of_answered_questions)




@register.filter(name='split_str')
@stringfilter
def split_str(string: str, char_to_split) -> list:
    return string.split(char_to_split)