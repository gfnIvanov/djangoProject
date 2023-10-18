from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('post/add', views.add_post, name='add-post'),
    path('post/<int:pk>/watch', views.watch_post, name='watch-post'),
    path('post/<int:pk>/edit', views.edit_post, name='edit-post'),
    path('post/<int:pk>', views.get_post, name='get-post'),
    path('practice/', views.practice, name='practice'),
    path('practice/upload_file', views.upload_file, name="upload_file"),
    path('practice/train_model', views.train_model, name="train_model"),
    path('practice/use_model', views.use_model, name="use_model"),
    path('register/', views.register, name='register'),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('post/<int:pk>/delete', views.delete_post, name='delete-post')
]
