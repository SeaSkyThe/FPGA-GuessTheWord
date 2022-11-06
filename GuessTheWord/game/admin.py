from django.contrib import admin
from .models import Question, Round, Player
# Register your models here.


class QuestionFilter(admin.ModelAdmin):
    list_display = ["difficulty", "subject", "tip", "answer"]
    list_filter = ["difficulty", "subject"]


admin.site.register(Question, QuestionFilter)
admin.site.register(Round)
admin.site.register(Player)
