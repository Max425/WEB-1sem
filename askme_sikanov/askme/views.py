from . import models
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import transaction
from askme.forms import *


def paginator(request, model, count):
    pag = Paginator(model, count)
    page_number = request.GET.get('page')
    return pag.get_page(page_number)


def index(request):
    objects = models.Question.objects.by_date()
    context = {
        'page_obj': paginator(request, objects, 10),
        'questions': objects,
    }
    return render(request, 'index.html', context)


@require_http_methods(['GET', 'POST'])
def question(request, question_id):
    try:
        question = models.Question.objects.get(id=question_id)
    except IndexError:
        raise Http404("does not exist")
    
    objects = models.Answer.objects.get_for_question(question_id)
    context = {
        'page_obj': paginator(request, objects, 10),
        'answers': objects,
        'question': question,
        'form': AnswerForm()
    }
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            context['form'] = form
            answer_text = form.cleaned_data['text']
            answer = models.Answer.objects.create(
                text=answer_text, question=question, correct=False, profile=request.user.profile)
            context['flag'] = True
            return render(request, 'question.html', context)
    else:
        form = AnswerForm()

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


@login_required(login_url="login", redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(request)
            return redirect('question', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'ask.html', {'form': form})


@require_http_methods(['GET', 'POST'])
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
    next_url = request.META.get('HTTP_REFERER')
    logout(request)
    return redirect(next_url if next_url else reverse('index'))


@login_required(login_url="login", redirect_field_name='continue')
@require_http_methods(['GET', 'POST'])
def settings(request):
    user = request.user
    if request.method == 'POST':
        form = SettingsForm(request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect(reverse('index'))
    else:
        form = SettingsForm(instance=user)
    return render(request, 'settings.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST, files=request.FILES)
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


@login_required()
@require_POST
def vote_up(request):
    object_id = request.POST.get('object_id')
    type = request.POST.get('type')
    type_obj = models.Question if type == 'question' else models.Answer
    try:
        obj = type_obj.objects.get(id=object_id)
    except type_obj.DoesNotExist:
        raise Http404("Does not exist")

    profile = request.user.profile

    with transaction.atomic():
        try:
            like = models.Like.objects.get(content_type=ContentType.objects.get_for_model(obj),
                                          object_id=object_id,
                                          profile=profile)
            like.delete()
            obj.like -= 1
        except models.Like.DoesNotExist:
            like = models.Like.objects.create(content_type=ContentType.objects.get_for_model(obj),
                                              object_id=object_id,
                                              profile=profile)
            obj.like += 1

        obj.save()

    return JsonResponse({
        'new_like': obj.like
    })


@login_required()
@require_POST
def is_correct(request):
    answer_id = request.POST.get('answer_id')
    try:
        answer = models.Answer.objects.get(id=answer_id)
    except models.Answer.DoesNotExist:
        raise Http404("Answer does not exist")

    profile = request.user.profile

    if answer.profile == profile:
        answer.correct = not answer.correct
        answer.save()

    return JsonResponse({
        'is_correct': answer.correct
    }) 
