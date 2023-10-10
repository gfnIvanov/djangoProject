from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import RegisterForm, PostForm
from .models import Post


def index(request):
    is_auth = request.session.get('is_auth', False)
    context = {'is_auth': is_auth}
    return render(request, 'index.html', context)


def create_post(request):
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
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def register(request):
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
                request.session['is_auth'] = True
                return HttpResponseRedirect(reverse('index'))
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        context = {'is_auth': True}
        return render(request, "index.html", context)
    else:
        return redirect("app")


def logout_view(request):
    if request.method == "POST":
        logout(request)
        context = {'is_auth': False}
        return render(request, "index.html", context)
    return render(request, 'index.html')
