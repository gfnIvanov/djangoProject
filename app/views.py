from typing import Optional
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm, PostForm, CommentForm
from .models import Post, Comment

def index(request: HttpRequest):
    context = {'active_page': 'index'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'index.html', context)


def posts(request: HttpRequest):
    context = {'active_page': 'posts'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'posts.html', context)


def register(request: HttpRequest):
    """
    Регистрация нового пользователя
    При успешной регистрации стразу выполняем авторизацию пользователя
    """  
    context = {'show_register': True}
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(username=form.cleaned_data['user_login'])
                context['form_data'] = form.cleaned_data
                context['errors'] = {'user_login': [{'message': 'Указанный логин уже присутствует в базе'}]}
                return render(request, 'index.html', context)
            except User.DoesNotExist:
                user = User.objects.create_user(username=form.cleaned_data['user_login'],
                                                password=form.cleaned_data['user_password'])
                user.first_name = form.cleaned_data['user_firstname']
                user.last_name = form.cleaned_data['user_surname']
                user.save()
                _set_auth_data(request, user)
                return HttpResponseRedirect(reverse('index'))
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def login(request: HttpRequest):
    """
    Авторизация пользователя
    """
    context = {'show_login': True}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['user_login']
            password = form.cleaned_data['user_password']
            user = authenticate(username=username, password=password)
            if user is not None:
                _set_auth_data(request, User.objects.get(username=username))
                return HttpResponseRedirect(reverse('index'))
            else:
                context['errors'] = {'auth_failed': [{'message': 'Не удалось пройти авторизацию'}]}
        context['form_data'] = form.cleaned_data
        if context.get('errors') is not None:
            context['errors'].update(form.errors.get_json_data()) 
        else:
            context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def logout(request):
    """
    Выход из аккаунта
    """
    _set_auth_data(request)
    return HttpResponseRedirect(reverse('index'))


def create_post(request: HttpRequest):
    context = {'show_register': False, 'is_auth': True}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                Post.objects.get(title=form.cleaned_data['title'])
                context['form_data'] = form.cleaned_data
                context['errors'] = {'title': [{'message': 'Указанное название поста уже присутствует в базе'}]}
            except Post.DoesNotExist:
                post = Post.objects.create(title=form.cleaned_data['title'],
                                           body=form.cleaned_data['body'])
                post.tags = form.cleaned_data['tags']
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def get_post(request: HttpRequest, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'index.html', {'post': post})


def create_comment(request: HttpRequest):
    context = {'show_register': False, 'is_auth': True}
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment.objects.create(body=form.cleaned_data['body'])
            comment.author = request.user
            comment.post = ""  # TODO взять Post на который пишется коммент
            comment.save()
            return render(request, 'index.html')
    else:
        form = CommentForm()
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def create_post(request: HttpRequest):
    context = {'show_register': False}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                Post.objects.get(title=form.cleaned_data['title'])
                context['form_data'] = form.cleaned_data
                context['errors'] = {'title': [{'message': 'Указанное название поста уже присутствует в базе'}]}
            except Post.DoesNotExist:
                post = Post.objects.create(title=form.cleaned_data['title'],
                                           body=form.cleaned_data['body'])
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def _set_auth_data(request: HttpRequest, user: Optional[User] = None) -> None:
    if user is None:
        request.session.clear()
        return
    request.session['auth_data'] = dict.fromkeys(['is_auth', 'firstname', 'surname'])
    request.session['auth_data']['is_auth'] = True
    request.session['auth_data']['firstname'] = user.first_name
    request.session['auth_data']['surname'] = user.last_name[0] + '.'
