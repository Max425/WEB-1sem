from . import models
from django.shortcuts import render


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request, question_id):
    context = {'question': models.QUESTIONS[question_id], 'answers' : models.ANSWERS}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')


def tag(request, tag_name):
    context = {'tag': tag_name,'questions': models.QUESTIONS}
    return render(request, 'tag.html', context)


def hot(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'hot.html', context)