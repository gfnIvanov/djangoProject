from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout-view'),
    path('login/', views.login_view, name='login-view'),
    path('create-post/', views.create_post, name='create-post')
]
