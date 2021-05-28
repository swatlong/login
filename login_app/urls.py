from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall', views.wall),
    path('post', views.create_post),
    path('post-comment/<int:post_id>', views.post_comment),
    path('delete/<int:id>', views.delete_comment),
    path('remove-post/<int:id>', views.delete_post),
    path('like/<int:id>', views.add_like),
    path('like-comment/<int:id>', views.like),
]