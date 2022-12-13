from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import subject_choices, Question, Round, Player, PlayerAnswer
from django.views.decorators.csrf import csrf_exempt

import json
# Create your views here.

# View for the REGISTER page
@csrf_exempt
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
            # Tem tambem que existir um Round (jogo em andamento) do player para aquela disciplina
            player = Player.objects.get(nickname=nickname)
            if(Round.objects.filter(player=player, subject=subject).exists()):
                context['player_exists'] = True
                context['nickname'] = nickname
                context['subject'] = subject
                return render(request, 'register.html', context=context)
            # Se não existir o round, cria o round e boa
            else:
                context['player_exists'] = True
                # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 256)
                round = Round.objects.create(player=player, subject=subject)
                context['round'] = round
                request.session['round'] = round.id                
                
                return redirect('play/'+str(round.current_question)+'/')
        # Se não existir o player, cria ele e o round
        else:
            context['player_exists'] = False
            player = Player.objects.create(nickname=nickname)
            # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 256)
            round = Round.objects.create(player=player, subject=subject)

            context['round'] = round
            request.session['round'] = round.id
            return redirect('play/'+str(round.current_question)+'/')

# View for the GAME page
@csrf_exempt
def play(request, question_number):
    context = {}
    if (request.method == 'GET'): # Se estivermos pedindo a página do jogo
        if ('round' in request.session): # Se ja existir uma rodada nas variaveis de sessão, usaremos ela, para evitar reiniciar o jogo caso o usuario dê refresh na pagina
            # Pegamos o round em questao
            try:
                context['round'] = Round.objects.get(
                    id=request.session['round'])
            except (KeyError, Round.DoesNotExist):
                context['round'] = None

            # Pegamos a questão que vai ser enviada para o template, através do argumento da URL (play/<int:numero>)
            try:
                context['question'] = [Question.objects.get(number=question_number,
                    subject=context['round'].subject)]
            except: # Caso não seja encontrao uma questão com esse numero, enviamos a primeira questão
                context['question'] = [Question.objects.order_by('number').first()]
                
            context['player_answers'] = PlayerAnswer.get_all_answers_from_user(round = context['round'])

            context['number_of_questions'] = Question.get_total_number_of_questions(context['round'].subject)

            context['current_question'] = question_number
            
            print(f"\n\n Questao enviada para o template {context['question'][0]} \n\n")
            return render(request, 'game.html', context=context)
            #del request.session['round']
        else:
            context['round'] = None
            context['question'] = []
            context['player_answers'] = []
            context['number_of_questions'] = 0
            return render(request, 'game.html', context=context)

    #controls when the player ANSWER a question (when the player uses all the chances (WRONG) or by getting it right (RIGHT))
    elif(request.is_ajax()):
        print(f"\n\n AJAX {request.body} Question ID: {question_number}\n\n")
        body = json.loads(request.body)
        round = Round.objects.get(id=body['round_id'])
        round.current_question = question_number
        round.save()
    
        number_of_questions = Question.get_total_number_of_questions()
        if(number_of_questions >= question_number+1):
            current_question = question_number+1
        else:
            current_question = question_number
        
        print(f"\n\n{round.player} \nQuestion ID: {question_number}\n\n")
        return redirect(play, question_number=current_question)



# LAST CHANGE WAS TRYING TO STOP USING QUESTION.ID AND USE QUESTION.NUMBER