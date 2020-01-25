from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.contrib.auth.decorators import login_required
from .forms import SignInForm, SignUpForm
# Create your views here.


def signIn(request):
    next = request.GET.get('next')
    form = SignInForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        remember = form.cleaned_data.get('remember_me')

        if not remember:
            request.session.set_expiry(0)

        user = authenticate(username=username, password=password)
        login(request, user)
        if next:
            return redirect(next)
        return redirect('/')

    return render(request, 'signin.html', {'form': form})


def signUp(request):
    form = SignUpForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()

        form.clean()
        messages.success(request, 'You have registered in successfully.')

    return render(request, 'signup.html', {'form': form})


def recoverPass(request):
    pass


@login_required(login_url='u_signin')
def signOut(request):
    logout(request)
    return redirect('/')


@login_required(login_url='u_signin')
def profile(request):
    pass


@login_required(login_url='u_signin')
def updateProfile(request):
    pass


@login_required(login_url='u_signin')
def changePassword(request):
    pass
