
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('group-chat/', views.group_chat, name='group-chat'),
]
