from django.contrib import auth
from django.http import HttpResponse


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
       auth.login(request, user)
    else:
        return HttpResponse('invalid login')

def register(request):
     pass

def logout(request):
    auth.logout(request)

