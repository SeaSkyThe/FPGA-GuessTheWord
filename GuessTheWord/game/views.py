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
        #player_answers = PlayerAnswer.get_all_answers_from_user_json(nickname=nickname, subject=subject)

        context['round'] = round
        #context['player_answers'] = player_answers
        request.session['round'] = round.id
        return redirect(play, question_number=round.current_question)
    
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
                # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 64*numero_de_questoes)
                round = Round.objects.create(player=player, subject=subject)
                round.score = (round.score)*Question.get_total_number_of_questions(subject)
                round.save()
                context['round'] = round
                request.session['round'] = round.id                
                
                return redirect(play, question_number=round.current_question)
        # Se não existir o player, cria ele e o round
        else:
            context['player_exists'] = False
            player = Player.objects.create(nickname=nickname)
            # Cria um round, passando o player e a disciplina. (A pontuação automaticamente inicia com 64*numero_de_questoes)
            round = Round.objects.create(player=player, subject=subject)
            round.score = (round.score)*Question.get_total_number_of_questions(subject)
            round.save()
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
            
            q_number = context['question'][0].number
            context['player_answers'] = (PlayerAnswer.get_all_answers_from_user_json(round = context['round'], question_number=q_number))

            context['number_of_questions'] = Question.get_total_number_of_questions(context['round'].subject)

            context['current_question'] = question_number
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
        # Load request body
        body = json.loads(request.body)
        round = Round.objects.get(id=body['round_id'])
        
        number_of_questions = Question.get_total_number_of_questions(round.subject)

        current_question = round.get_next_question_number()

        # Atualiza a questão atual do usuário
        
        round.current_question = question_number
        round.score = int(body['score'])
        round.save()

        # Registra as tentativas de respostas do usuario
        for answer_index in body['player_answers']:
            is_final = False
            if(int(answer_index) == int(len(body['player_answers']) - 1)):
                is_final = True
            # TODO REQUEST BEING RECEIVED 2 TIMES, AND DUPLICATING PLAYERANSWERS
            # TODO SAVE SCORE
            # TODO mark as final answers
            PlayerAnswer.objects.create(round=round, 
                                        question_number=question_number, 
                                        player_answer=body['player_answers'][answer_index], 
                                        position_in_game=answer_index, 
                                        is_final_answer=is_final)
        #print(PlayerAnswer.get_all_answers_from_user_json(nickname='Groot'.title(), subject='circuitos_digitais'))
        return redirect(play, question_number=current_question)



