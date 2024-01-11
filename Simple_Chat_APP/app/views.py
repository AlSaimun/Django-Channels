from django.shortcuts import render, redirect

# Create your views here.
def group_chat(request):
    group_name = request.GET.get('group_name', 'general')
    print(group_name)
    return render(request, 'app/index.html', {'group_name':group_name})

def home(request):
    return render(request, 'app/group_form.html')