from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from application.models import Team
from application.forms import TeamCreateForm

def home(request):
    context = {}
    if request.user.is_authenticated:
        try:
            team = request.user.team
        except Team.DoesNotExist:
            team = Team(user = request.user)
    if request.POST:
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.admin = request.user
            # request.user.team.add(team)
            # team.strength = 1
            # team.application_status = 'Not Submitted'
            team.save()
            # team = form.save()
            # request.user.team.add(team)
            # user_obj = form.save()
            # user_obj.team.add(team) 
            context['success'] = 'Team Created Successfully'
            return render(request, 'home.html', context )
        else:
            context['team_form'] = form
    else:
        form = TeamCreateForm(
            initial={
                'name': team.name,
            }
        )
        context['team_form'] = form
    return render(request, 'home.html', context )
    # return render(request, 'home.html')


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('profile')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'login.html', context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = AccountUpdateForm(
            initial = {
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, 'account.html', context)

