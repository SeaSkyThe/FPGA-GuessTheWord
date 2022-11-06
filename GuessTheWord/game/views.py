from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import subject_choices, Question, Round, Player
import json
# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register(request):
    context = {}
    if(request.method == 'GET'):
        context['subjects'] = subject_choices
        return render(request, 'register.html', context=context)
    elif(request.method == 'POST'):
        # Pega do form o nick e a disciplina
        nickname = request.POST.get('nickname_field')
        nickname = nickname.title()
        subject = request.POST.get('subject_select')
        
        # Cria um player com aquele nick, ou pega um que ja existe
        player = Player.objects.get_or_create(nickname=nickname)[0]
        # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 256)
        round = Round.objects.create(player=player, subject=subject)
        
        context['round'] =  round
        request.session['round'] = round.id
        return redirect('play')

def play(request):
    context = {}
    if(request.method == 'GET'):
        if('round' in request.session):
            try:
                context['round'] = Round.objects.get(id=request.session['round'])
            except (KeyError, Round.DoesNotExist):
                context['round'] = None
            #del request.session['round']
            return render(request, 'game.html', context=context)
        else:
            context['round'] = None
            return render(request, 'game.html', context=context)
    elif(request.method == 'POST'):
        return render(request, 'game.html') 