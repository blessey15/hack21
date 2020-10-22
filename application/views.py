from django.shortcuts import render

from .forms import TeamCreateForm

# Create your views here.

def create_team_view(request):
    context = {}
    if request.POST:
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.admin = request.user
            team.strength = 1
            team.application_status = 'Not Submitted'
            team.save()
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
        