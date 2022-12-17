from django.urls import path

from . import views

urlpatterns = [
    path('', views.register, name='register'),
    path('play/<int:question_number>/', views.play, name='play'),
]