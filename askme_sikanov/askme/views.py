from . import models
from django.core.paginator import Paginator
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# from askme.forms import LoginForm


def paginator(request, model, count):
    pag = Paginator(model, count)
    page_number = request.GET.get('page')
    return pag.get_page(page_number)


@login_required
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
    context = {
        'page_obj': paginator(request, objects, 10),
        'answers': objects,
        'question': question,
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


def ask(request):
    return render(request, 'ask.html')


# def login_view(request):
#     if request.method == 'POST':
#         login_form = LoginForm(request.POST)
#         if login_form.is_valid():
#             user = authenticate(request, **login_form.cleaned_data)
#             if user is not None:
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 login_form.add_error(None, 'Invalid login or password.')
#     else:
#         login_form = LoginForm()
    
#     return render(request, 'login.html', {'form': login_form})



def settings(request):
    return render(request, 'settings.html')


def signup(request):
    return render(request, 'signup.html')
