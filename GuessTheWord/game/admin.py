from django.contrib import admin
from .models import Question, Round, Player, PlayerAnswer
# Register your models here.


class QuestionFilter(admin.ModelAdmin):
    list_display = ["id", "difficulty", "subject", "tip", "answer"]
    list_filter = ["difficulty", "subject"]


admin.site.register(Question, QuestionFilter)
admin.site.register(Round)
admin.site.register(Player)
admin.site.register(PlayerAnswer)
