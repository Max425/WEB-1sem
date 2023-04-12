from . import models
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import Http404

def paginator(request, model, count):
    pag = Paginator(model, count)
    page_number = request.GET.get('page')
    return pag.get_page(page_number)

def index(request):
    context = {
        'page_obj': paginator(request, models.Question.objects.all(), 10),
        'questions': models.Question.objects.all(),
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    try:
        question = models.Question.objects.all()[int(question_id)]
    except IndexError:
        return Http404("does not exist")

    context = {
        'page_obj': paginator(request, models.Answer.objects.get_for_question(question_id), 10),
        'answers': models.Answer.objects.get_for_question(question_id),
        'question': question,
    }
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = {
        'page_obj': paginator(request, models.Question.objects.get_by_tag(tag_name), 10),
        'tag': tag_name,
        'questions': models.Question.objects.get_by_tag(tag_name)
    }
    return render(request, 'tag.html', context)


def hot(request):
    context = {
        'page_obj': paginator(request, models.Question.objects.get_new(), 10),
        'questions': models.Question.objects.get_new(),
    }
    return render(request, 'hot.html', context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')
