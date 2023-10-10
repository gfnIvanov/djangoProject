from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('post/<int:pk>', views.get_post, name='get-post'),
    path('admin/', views.admin, name='admin'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('create-post/', views.create_post, name='create-post'),
    path('post/<int:pk>/edit', views.edit_post, name='edit-post'),
    path('post/<int:pk>/delete', views.delete_post, name='delete-post')
]
