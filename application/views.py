from django.shortcuts import render

from .forms import TeamCreateForm
from .models import Application, Team

# Create your views here.

def create_team_view(request):
    pass
#     context = {}
    # if request.user.is_authenticated:
    #     try:
    #         team = request.user.team
    #         application = request.user.application_team
    #     except Team.DoesNotExist:
    #         team = Team(user = request.user)
    #     except Application.DoesNotExist:
    #         application = Application(user = request.user)
    # if request.POST:
    #     form = TeamCreateForm(request.POST)
    #     if form.is_valid():
    #         team = form.save(commit=False)
    #         team.admin = request.user
    #         # request.user.team.add(team)
    #         # team.strength = 1
    #         # team.application_status = 'Not Submitted'
    #         team.save()
    #         # team = form.save()
    #         # request.user.team.add(team)
    #         # user_obj = form.save()
    #         # user_obj.team.add(team) 
    #         context['success'] = 'Team Created Successfully'
    #         return render(request, 'home.html', context )
    #     else:
    #         context['team_form'] = form
    # else:
    #     form = TeamCreateForm(
    #         initial={
    #             'name': team.name,
    #         }
    #     )
    #     context['team_form'] = form
    # return render(request, 'home.html', context )
        