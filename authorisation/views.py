from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse
from landing.views import *
from dashboard.views import *
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.


def anonymous_required(function=None,redirect_url=None):
    if not redirect_url:
        redirect_url = 'dashboard'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous(),
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def login(request):
    if request.method == 'POST':
        email = request.POST['email'].replace(' ','').lower()
        password = request.POST['password']

        user = auth.authenticate(username=email,password=password)

        if user:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,'user not exist')


        

    return render(request,'authorisation/login.html',{})


@anonymous_required
def signup(request):

    if request.method == 'POST':
        email = request.POST['email'].replace(' ','').lower()
        password1 = request.POST['password1']
        password2 = request.POST['password2']


        if not password1 == password2:
            messages.error(request,'password not matching')
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request,'email already exists use another one')
            return redirect('signup')

        user = User.objects.create_user(email=email,username=email,password=password2)
        user.save()
        auth.login(request,user)
        return redirect('dashboard')

    return render(request,'authorisation/signup.html')



# logoout function

def logout(request):
    auth.logout(request)
    return redirect('login')