from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='blog'),
    path('<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/modify/<int:post_id>/', views.post_modify, name='post_modify'),
    path('post/delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('comment/create/<int:post_id>/', views.comment_create, name='comment_create'),
]