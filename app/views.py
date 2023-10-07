from django.shortcuts import render

def index(request):
    zalupa = 'MEGA ZALUPA'
    return render(request, 'index.html', context={'zalupa': zalupa})