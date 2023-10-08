from django.shortcuts import render

def index(request):
    is_auth = request.session.get('is_auth', False)
    context = {'is_auth': is_auth}
    return render(request, 'index.html', context)

def register(request):
    context = {'is_auth': True}
    return render(request, 'index.html', context)
