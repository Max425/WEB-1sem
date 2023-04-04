from . import models
from django.core.paginator import Paginator
from django.shortcuts import render


def index(request):
    questions_list = models.QUESTIONS
    paginator = Paginator(questions_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'questions': models.QUESTIONS,
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    answer_list = models.QUESTIONS
    paginator = Paginator(answer_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'answers': models.ANSWERS,
        'question': models.QUESTIONS[question_id],
    }
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
    tag_questions_list = models.QUESTIONS
    paginator = Paginator(tag_questions_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'tag': tag_name,
        'questions': models.QUESTIONS
    }
    return render(request, 'tag.html', context)


def hot(request):
    hot_questions_list = models.QUESTIONS
    paginator = Paginator(hot_questions_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'questions': models.QUESTIONS,
    }
    return render(request, 'hot.html', context)
