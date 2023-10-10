from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import RegisterForm, PostForm, CommentForm
from .models import Post, Comment


def index(request):
    is_auth = request.session.get('is_auth', False)
    context = {'is_auth': is_auth}
    return render(request, 'index.html', context)


def home(request):
    # Это для вкладки "Главная". Чтобы все посты выводились
    if request.user.is_authenticated():
        posts = Post.objects.all()
        return render(request, 'index.html', {"posts": posts})
    else:
        redirect('app')


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
                post.tags = form.cleaned_data['tags']
                post.author = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
    else:
        form = PostForm()
        context['form_data'] = form.cleaned_data
        context['errors'] = form.errors.get_json_data()
    return render(request, 'index.html', context)


def edit_post(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('index.html', post_id=post.id)
    context = {'post': post, 'index': index, 'form': form}
    return render(request, 'components/edit_post.html', context)


def delete_post(request, pk):
    post_to_delete = Post.objects.get(pk=pk)
    if post_to_delete is not None:
        post_to_delete.delete()
    return HttpResponseRedirect(reverse('index'))


def get_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'index.html', {'post': post})


def create_comment(request):
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
        return HttpResponseRedirect(reverse('index'))

    else:
        return HttpResponseRedirect(reverse('index'))


def logout_view(request):
    # TODO Нужно подправить файл headers.html, чтобы отправлять через кнопку POST-запрос
    # if request.method == "POST":
    logout(request)
    context = {'is_auth': False}
    return render(request, "index.html", context)
# return render(request, 'index.html')
