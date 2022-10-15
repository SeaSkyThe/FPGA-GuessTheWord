from django.contrib import admin
from .models import Question, Round, Player
# Register your models here.
admin.site.register(Question)
admin.site.register(Round)
admin.site.register(Player)