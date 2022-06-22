# import des fonctions login et authenticate
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from . import forms
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required,permission_required

@login_required
def logout_user(request):

    logout(request)
    return redirect('login')



def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user.role == "SECRETARIAT" is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('/statistique/')
            if user.role == "ADMINISTRATION" is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('/statistique/personnel')
            if user.role == "PERSONNEL" is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('/add/personne')
            if user is not None:
                login(request, user)
                # message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('index/')
            else:
                messages.error(request, 'Identifiants invalides.')
    return render(
        request, 'login.html', context={'form': form, 'message': message})



def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            # login(request, user)
            return redirect(settings.LOGIN_URL)
    return render(request, 'register.html', context={'form': form})
