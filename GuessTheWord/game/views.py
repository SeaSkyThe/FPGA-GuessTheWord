from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import subject_choices, Question, Round, Player
import json
# Create your views here.

def register(request):
    context = {}
    context['subjects'] = subject_choices

    if(request.is_ajax()): # Se for uma requisição AJAX (requisição onde o usuário disse que ele é o player em questão)
        # Usaremos o Nickname e o nome da Disciplina, para pegar de onde o player parou (pegar o round)
        body = json.loads(request.body)
        nickname = body['nickname']
        nickname = nickname.title()
        subject = body['subject']
        
        player = Player.objects.get(nickname=nickname)
        round = Round.objects.get(player=player, subject=subject)
        
        context['round'] = round
        request.session['round'] = round.id
        return redirect('play')
    
    elif (request.method == 'GET'): # Se for uma GET request, renderiza a pagina de registro
        return render(request, 'register.html', context=context)
    elif (request.method == 'POST'): # Se for uma POST, está enviando o form
        # Pega do form o nick e a disciplina
        nickname = request.POST.get('nickname_field')
        nickname = nickname.title()
        subject = request.POST.get('subject_select')

        # Verifica se um player já existe com esse nick, se existir, avisa o usuario
        if(Player.objects.filter(nickname=nickname).exists()):
            context['player_exists'] = True
            context['nickname'] = nickname
            context['subject'] = subject
            return render(request, 'register.html', context=context)
        
        # Se nao, continua
        context['player_exists'] = False
        player = Player.objects.create(nickname=nickname)
        # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 256)
        round = Round.objects.create(player=player, subject=subject)

        context['round'] = round
        request.session['round'] = round.id
        return redirect('play')


def play(request):
    context = {}
    if (request.method == 'GET'):
        if ('round' in request.session):
            try:
                context['round'] = Round.objects.get(
                    id=request.session['round'])
            except (KeyError, Round.DoesNotExist):
                context['round'] = None

            context['questions'] = Question.objects.filter(
                subject=context['round'].subject)
            return render(request, 'game.html', context=context)
            #del request.session['round']
        else:
            context['round'] = None
            context['questions'] = []
            return render(request, 'game.html', context=context)

    elif (request.method == 'POST'):
        return render(request, 'game.html')


def getQuestionsJSON(subject):
    questions = []
    for question in Question.objects.filter(subject=subject):
        questions.append(
            {
                "tip": question.tip,
                "answer": question.answer,
                "difficulty": question.difficulty,
                "subject": question.subject
            }
        )

    return questions
