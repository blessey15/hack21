from django.shortcuts import render, get_object_or_404, redirect

from .forms import TeamCreateForm
from .models import Application, Team, JoinRequest
from accounts.views import home

# Create your views here.

def team_detail_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    context['team'] = team
    try:
        application = Application.objects.get(team=team)
        # print("has team")
        context['application'] = application
        context['number_of_members'] = len(application.members.all())
        if (request.user in application.members.all()):
            context['in_team'] = True 
        # try:
        #     join_request = JoinRequest.objects.get(team=team, user=request.user)
        #     context['sent_request'] = True
        # except JoinRequest.DoesNotExist:
        #     context['sent_request'] = False
        # print(team.application_team.team.name)
    except Application.DoesNotExist:
        pass
    return render(request, 'team_detail.html', context)


def join_team_view(request, team_id):
    context={}
    team = get_object_or_404(Team, id=team_id)
    context['team'] = team
    try:
        application = Application.objects.get(team=team)
        context['application'] = application
        context['number_of_members'] = len(application.members.all())
        if (request.user in application.members.all()):
            context['in_team'] = True
        else:
            if application.application_status == "Not Submitted":
                if len(application.members.all())<4:
                    application.members.add(request.user)
                    # return redirect('join_team')
                    # return render(request, 'team_detail.html', context)
                    # return team_detail_view(request, team_id)
                    return redirect('home')
                else:
                    context['message'] = "This team already has 4 members. You cant join this team!"
                    return render(request, 'messages.html', context)
            else:
                context['message'] = "The Application for this team is already submitted. You can no longer Join this team."
                return render(request, 'messages.html', context)
    #     try:
    #         join_request = JoinRequest.objects.get(team=team, user=request.user)
    #         context['sent_request'] = True
    #     except JoinRequest.DoesNotExist:
    #         join_request = JoinRequest(team=team, user=request.user, request_status='Submitted')
    #         join_request.save()
    #         context['sent_request'] = True
    #     # print("has team")
    #     context['application'] = application
    #     # print(team.application_team.team.name)
    except Application.DoesNotExist:
        pass
    return render(request, 'team_detail.html', context)
    # return redirect('home')


# def accept_to_team(request, team_id):
#     context = {}
#     try:
#         team = Team.objects.get(id=team_id)
#     except Team.DoesNotExist:
#         pass
#     try:
#         application = Application.objects.get(team=team)
#         # print("has team")
#         context['application'] = application
#         application.members.add(request.user)
#         application.save()
#         # request.user.request_team.request_status = "Accepted"
#         # request.user.join_request.request_status = "Accepted"
#         print(team.application_team.team.name)
#     except Application.DoesNotExist:
#         pass
#     return render(request, 'messages.html', context)

def leave_team_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    application = team.application_team
    # application = Application.objects.filter(members__id = request.user.id)
    # if not (len(application) == 0):
    #     application = application[0]
    context['application'] = application
    # team = application.team
    if application.application_status == 'Not Submitted':
        if request.user == team.admin:
            application.delete()
            context['application'] = None
            team.delete()
            context['team'] = None
            return redirect('home')
        else:
            application.members.remove(request.user)
            return redirect('home')
    else:
        context['message'] = "The application is already submitted. You cannot leave the team now!!"
        return render(request, 'messages.html', context)
    
    return render(request, 'team_detail.html', context)

def submit_aplication_view(request):
    context = {}
    application = Application.objects.filter(members__id = request.user.id)
    if len(application) > 0:
        application = application[0]
        if request.user == application.team.admin:
            if len(application.members.all()) > 4:
                context['message'] = "You can have a maximum of 4 people only in a team!!."
                return render(request, 'messages.html', context)
                # application.application_status = 'Submitted'
                # application.save()
            elif len(application.members.all()) < 2:
                context['message'] = "You need atleast 2 people in a team!!."
                return render(request, 'messages.html', context)
            else:
                application.application_status = 'Submitted'
                application.save()
                # context['message'] = "You need 4 people in a team to submit the application."
                # return render(request, 'messages.html', context)
        else:
            context['message'] = "Only Team Admin can submit the application"
            return render(request, 'messages.html', context)
    return redirect('home')


def organizer_dashboard(request):
    context = {}
    applications = Application.objects.all()
    context['applications'] = applications
    return render(request, 'organizer_db.html', context)