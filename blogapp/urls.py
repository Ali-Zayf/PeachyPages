from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.post_list, name="post_list"),

    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),

    path('create/', views.create_post, name="create_post"),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),

    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),

    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]