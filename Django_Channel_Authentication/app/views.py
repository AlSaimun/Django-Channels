from django.shortcuts import render, redirect

from .models import Group, Chat 
# Create your views here.


def group_chat(request):
    group_name = request.GET.get('group_name', 'general')
    group = Group.objects.filter(name = group_name).first()
    print(group_name)
    chats = []
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        group = Group.objects.create(name = group_name)
    return render(request, 'app/index.html', {'group_name':group_name, 'chats':chats})

def home(request):
    return render(request, 'app/group_form.html')