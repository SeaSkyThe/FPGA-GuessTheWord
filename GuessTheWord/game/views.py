from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import subject_choices, Question, Round, Player, PlayerAnswer
import json
# Create your views here.

# View for the REGISTER page
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
        player_answers = PlayerAnswer.get_all_answers_from_user(nickname=nickname, subject=subject)

        context['round'] = round
        context['player_answers'] = player_answers
        request.session['round'] = round.id
        return redirect('play/'+str(round.current_question)+'/')
    
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
        return redirect('play/'+str(round.current_question)+'/')

# View for the GAME page
def play(request, question_id):
    context = {}
    if (request.method == 'GET'): # Se estivermos pedindo a página do jogo
        if ('round' in request.session): # Se ja existir uma rodada nas variaveis de sessão, usaremos ela, para evitar reiniciar o jogo caso o usuario dê refresh na pagina
            # Pegamos o round em questao
            try:
                context['round'] = Round.objects.get(
                    id=request.session['round'])
            except (KeyError, Round.DoesNotExist):
                context['round'] = None

            # Pegamos a questão que vai ser enviada para o template, através do argumento da URL (play/<int:id>)
            try:
                context['question'] = [Question.objects.get(id=question_id,
                    subject=context['round'].subject)]
            except: # Caso não seja encontrao uma questão com esse ID, enviamos a primeira questão
                 return 
                
            context['player_answers'] = PlayerAnswer.get_all_answers_from_user(round = context['round'])

            context['number_of_questions'] = Question.get_total_number_of_questions()
            
            return render(request, 'game.html', context=context)
            #del request.session['round']
        else:
            context['round'] = None
            context['question'] = []
            context['player_answers'] = []
            context['number_of_questions'] = 0
            return render(request, 'game.html', context=context)

    elif (request.method == 'POST'):
        return render(request, 'game.html')


# View that controls when the player ANSWER a question (when the player uses all the chances (WRONG) or by getting it right (RIGHT))
def answer(request):
    pass