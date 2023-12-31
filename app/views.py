import os
from typing import Optional
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.uploadedfile import UploadedFile
from config.settings import BASE_DIR
from .forms import RegisterForm, LoginForm, PostForm, UploadFileForm
from .models import Post
from .ML import model


def index(request: HttpRequest):
    context = {'active_page': 'index'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'index.html', context)


def posts(request: HttpRequest):
    posts_data = []
    posts = Post.objects.all()
    for post in posts:
        user = User.objects.get(username=post.author)
        author = user.last_name + ' ' + user.first_name[0] + '.'
        posts_data.append({
            'id': post.id,
            'title': post.title,
            'body': post.body,
            'date_create': post.date_create,
            'author': author
        })
    context = {'active_page': 'posts', 'posts': posts_data}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'posts.html', context)


def watch_post(request: HttpRequest, pk: int):
    post = Post.objects.get(pk=pk)
    context = {'post': post}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'watch_post.html', context)


def practice(request: HttpRequest):
    context = {'active_page': 'practice'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    return render(request, 'practice.html', context)


def register(request: HttpRequest):
    """
    Регистрация нового пользователя
    При успешной регистрации сразу выполняем авторизацию пользователя
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


def add_post(request: HttpRequest):
    context = {}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                Post.objects.get(title=form.cleaned_data['title'])
                context['form_data'] = form.cleaned_data
                context['errors'] = {'title': [{'message': 'Указанное название поста уже присутствует в базе'}]}
                return render(request, 'add_post.html', context)
            except Post.DoesNotExist:
                user = User.objects.get(username=request.session.get('auth_data')['login'])
                post = Post.objects.create(title=form.cleaned_data['title'],
                                           body=form.cleaned_data['body'],
                                           author=user)
                post.save()
                return HttpResponseRedirect(reverse('posts'))
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'add_post.html', context)


def edit_post(request: HttpRequest, pk: int):
    context = {}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)

    post = Post.objects.get(pk=pk)
    context['post'] = post

    if request.method == 'POST':
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('posts'))
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'edit_post.html', context)


def delete_post(request: HttpRequest, pk: int):
    post_to_delete = Post.objects.get(pk=pk)
    if post_to_delete is not None:
        post_to_delete.delete()
    return HttpResponseRedirect(reverse('index'))


def get_post(request: HttpRequest, pk: int):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'index.html', {'post': post})


def upload_file(request: HttpRequest):
    context = {'active_page': 'upload_file'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            _upload_file(request.FILES['file'])
            return HttpResponseRedirect(reverse('train_model'))
        context['errors'] = form.errors.get_json_data()
    return render(request, 'practice.html', context)


def train_model(request: HttpRequest):
    context = {'active_page': 'train_model'}
    messages = []
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    model.train()
    with open(os.path.join(BASE_DIR, 'app/ML/log.txt'), 'r') as log_file:
        for str in log_file.readlines():
            messages.append(str)
    context.update({'messages': ','.join(messages)})
    return render(request, 'train_model.html', context)


def use_model(request: HttpRequest):
    context = {'active_page': 'use_model'}
    auth_data = request.session.get('auth_data', {'is_auth': False})
    context.update(auth_data)
    target, test_data, prediction = model.use()
    context.update({'target': target, 'test_data': test_data, 'prediction': prediction})
    return render(request, 'use_model.html', context)


def _set_auth_data(request: HttpRequest, user: Optional[User] = None) -> None:
    if user is None:
        request.session.clear()
        return
    request.session['auth_data'] = dict.fromkeys(['is_auth', 'firstname', 'surname'])
    request.session['auth_data']['is_auth'] = True
    request.session['auth_data']['login'] = user.username
    request.session['auth_data']['firstname'] = user.first_name
    request.session['auth_data']['surname'] = user.last_name[0] + '.'


def _upload_file(file: UploadedFile):
    with open(os.path.join(BASE_DIR, 'temp/data.csv'), 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)
