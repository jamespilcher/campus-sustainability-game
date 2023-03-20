from django.shortcuts import render
from django.core import serializers
from app.models import Question
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random

questionCounter = 0

def trivia(request):
    return render(request, 'app/trivia.html')

def questions():
    question = serializers.serialize('json', Question.objects.all())
    context = {
        'question': question,
    }
    return context

def get_random_questions(request):
    pks = Question.objects.values_list('pk', flat=True)
    random_pk = random.choice(pks)
    random_question = Question.objects.get(pk=random_pk)
    return random_question

@login_required
def trivia(request):
    context = {}
    if Question.objects.count() == 0:
        messages.error(request, ("Found no questions in database. "
                                 "Please add some questions in the "
                                 "admin panel."))
    if not Question.objects.count() == 0:
        if questionCounter <= 3:
            questionCounter += 1
            questions = get_random_questions()
            context = {
                'question': questions.question,
                'a': questions.a,
                'b': questions.b,
                'c': questions.c,
                'd': questions.d,
            }
        else:
            messages.error(request, ("You have completed the quiz."))

    return render(request, 'app/trivia.html', context)
