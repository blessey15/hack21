from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from application.models import Team, Application
from application.forms import TeamCreateForm, TeamSearchForm
from  application.views import create_team_view

def home(request):
    # create_team_view(request)
    no_teams_found = False
    context = {}
    if request.user.is_authenticated:
        try:
            team = request.user.team
            user_has_team = True
            context['users_team'] = team
        except Team.DoesNotExist:
            team = Team(admin = request.user)
            # team.save() 
            user_has_team = False

        # try:
        #     application = Application.objects.get(team=team)
        #     print("has team")
        #     print(team.application_team.team.name)
        # except Application.DoesNotExist:
        #     application = Application(team = team)
        #     application.save()
        #     application.members.add(request.user)
        #     # application.save()
        #     print("created Team")

        team_form = TeamCreateForm()
        search_form = TeamSearchForm()
        context['user_has_team'] = user_has_team
        # context['application'] = application
        if request.POST:
            # team_form = TeamCreateForm(request.POST)
            # search_form = TeamSearchForm(request.POST)
            if "create_team" in request.POST:
                team_form = TeamCreateForm(request.POST)
                if team_form.is_valid(): #TODO searching for teams to join
                    if user_has_team:
                        context['message'] = 'You already have a team!!'
                    else:
                        team = team_form.save(commit=False)
                        team.admin = request.user
                        # request.user.team.add(team)
                        # team.strength = 1
                        # team.application_status = 'Not Submitted'
                        team.save()

                        try:
                            application = Application.objects.get(team=team)
                            print("has team")
                            context['application'] = application
                            print(team.application_team.team.name)
                        except Application.DoesNotExist:
                            application = Application(team = team)
                            application.save()
                            application.members.add(request.user)
                            # application.save()
                            print("created Team")
                            context['application'] = application


                        # application = Application(team = team)
                        # # application.save()
                        # application.save()
                        # application.members.add(request.user)
                        # context['application'] = application

                        # team = team_form.save()
                        # request.user.team.add(team)
                        # user_obj = team_form.save()
                        # user_obj.team.add(team) 
                        context['success'] = 'Team Created Successfully'
                        return render(request, 'home.html', context )
                else:
                    context['team_form'] = team_form

            elif "search_team" in request.POST:
                # conext['search_performed'] = True
                search_form = TeamSearchForm(request.POST)
                if search_form.is_valid():
                    team_id = search_form.cleaned_data.get('team_id')
                    try:
                        searched_team = Team.objects.get(id=team_id)
                        context['searched_team'] = searched_team
                    except Team.DoesNotExist:
                        no_teams_found = True
                        context['no_teams_found'] = no_teams_found
                else:
                    context['search_form'] = search_form 
        else:
            team_form = TeamCreateForm(
                initial={
                    # 'name': team.name,
                }
            )
            context['team_form'] = team_form
            search_form = TeamSearchForm(
                initial={

                }
            )
            context['search_form'] = search_form

        try:
            application = Application.objects.get(team=team)
            print("has team")
            context['application'] = application
            print(team.application_team.team.name)
        except Application.DoesNotExist:
            pass
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

