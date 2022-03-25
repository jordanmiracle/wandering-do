# Create your views here.
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from wanderingapp.models import PostImage
from .forms import RegisterForm, LoginForm


@login_required(login_url="user:login")
def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        newUser = User(username=username)
        newUser.set_password(password)

        newUser.save()
        login(request, newUser)
        messages.info(request, "Successfully registered..")

        return redirect("index")
    context = {
        "form": form
    }
    return render(request, "register.html", context)


def loginUser(request):
    form = LoginForm(request.POST or None)

    context = {
        "form": form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.info(request, "Username or password incorrect")
            return render(request, "login.html", context)

        messages.success(request, "Login Successful")
        login(request, user)
        return redirect("index")
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("index")


@login_required(login_url='login')
def addPhoto(request):
    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        for image in images:
            photo = PostImage.objects.create(
                description=data['description'],
                image=image,
            )

        return redirect('gallery')

    return render(request, 'add.html')
