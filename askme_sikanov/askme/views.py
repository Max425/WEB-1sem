from . import models
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from askme.forms import *


def paginator(request, model, count):
    pag = Paginator(model, count)
    page_number = request.GET.get('page')
    return pag.get_page(page_number)


def index(request):
    objects = models.Question.objects.all()
    context = {
        'page_obj': paginator(request, objects, 10),
        'questions': objects,
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    try:
        question = models.Question.objects.get(id=question_id)
    except IndexError:
        raise Http404("does not exist")
    
    objects = models.Answer.objects.get_for_question(question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer_text = form.cleaned_data['text']
            answer = models.Answer.objects.create(
                text=answer_text, question=question, correct=False, profile=request.user.profile)
            context = {
                'page_obj': paginator(request, objects, 10),
                'answers': objects,
                'question': question,
                'form': form,
                'flag': True
            }
            return render(request, 'question.html', context)
    else:
        form = AnswerForm()

    context = {
        'page_obj': paginator(request, objects, 10),
        'answers': objects,
        'question': question,
        'form': form,
        'flag': False
    }
    return render(request, 'question.html', context)


def tag(request, tag_name):
    objects = models.Question.objects.get_by_tag(tag_name)
    context = {
        'page_obj': paginator(request, objects, 10),
        'tag': tag_name,
        'questions': objects
    }
    return render(request, 'tag.html', context)


def hot(request):
    objects = models.Question.objects.get_hot()
    context = {
        'page_obj': paginator(request, objects, 10),
        'questions': objects,
    }
    return render(request, 'hot.html', context)


@login_required(redirect_field_name='continue')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request)
            return redirect('question', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue') if request.GET.get('continue') != '' else reverse('index'))
            else:
                login_form.add_error(None, 'Invalid login or password.')
    else:
        login_form = LoginForm()

    return render(request, 'login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@login_required(redirect_field_name='continue')
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SettingsForm(instance=user)
    return render(request, 'settings.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user is not None:
                login(request, user)
                return redirect(reverse('index'))
            else:
                user_form.add_error(None, 'User saving error!')
    else:
        user_form = RegistrationForm()

    return render(request, 'signup.html', {'form': user_form})
