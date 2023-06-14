from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Events

# Create your views here.

def userregister(request):
    if request.user.is_authenticated:
        return redirect("/eventsList/")
    elif request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            print('user created')
            return redirect("/login/")
    form = NewUserForm()
    return render(request=request, template_name="register.html",
                  context={"register_form": form})

def userlogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # print('reached')
                login(request, user)
                return redirect('/postList/')
            else:
                print("Invalid username or password.")
        else:
            print("Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})

def userlogout(request):
    logout(request)
    print("You have successfully logged out.")
    return redirect("/")

def eventsList(request):
    if request.user.is_authenticated:
        events=Events.get_all_events(user=request.user)
        return render(request=request,template_name='my_events_List.html',context={"events":events,"user":request.user})
    else:
        return redirect("/login/")

