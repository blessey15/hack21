from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import TeamCreateForm
from .models import Application, Team, JoinRequest
from accounts.models import Account
from profiles.models import ParticipantProfile
from accounts.views import home
from hack21.decorators import organizer_view, participant_view

# Create your views here.

@login_required(login_url='login')
def team_detail_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    context['team'] = team
    try:
        application = Application.objects.get(team=team)
        # print("has team")
        context['application'] = application
        context['number_of_members'] = len(application.members.all())
        if len(Application.objects.filter(members__id = request.user.id))>0:
            context['has_a_team'] = True
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


@login_required(login_url='login')
@participant_view
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
            if len(Application.objects.filter(members__id = request.user.id))>0:
                context['message'] = "You are already part of a team!!"
                return  render(request, 'messages.html', context)
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

@login_required(login_url='login')
@participant_view
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
 
@login_required(login_url='login')
@participant_view
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


@login_required(login_url='login')
# @organizer_view
def organizer_dashboard(request):
    context = {}
    applications = Application.objects.all()
    context['applications'] = applications
    number_of_applications = len(applications)
    context['number_of_applications'] = number_of_applications
    number_of_accounts = len(Account.objects.all())
    context['number_of_accounts'] = number_of_accounts
    number_of_teams = len(Team.objects.all())
    context['number_of_teams'] = number_of_teams
    # incomplete_applications = Application.objects.filter(application_status='Not Submitted')
    incomplete_applications = len(Application.objects.filter(application_status='Not Submitted'))
    context['incomplete_applications'] = incomplete_applications

    review_pending_applications = len(Application.objects.filter(application_status='Submitted'))
    context['review_pending_applications'] = review_pending_applications
    review_pending_applications_percent = int((review_pending_applications/number_of_applications)*100)
    context['review_pending_applications_percent'] = review_pending_applications_percent

    accepted_applications = len(Application.objects.filter(application_status='Accepted'))
    context['accepted_applications'] = accepted_applications
    accepted_applications_percent = int((accepted_applications/number_of_applications)*100)
    context['accepted_applications_percent'] = accepted_applications_percent

    declined_applications = len(Application.objects.filter(application_status='Declined'))
    context['declined_applications'] = declined_applications
    declined_applications_percent = int((declined_applications/number_of_applications)*100)
    context['declined_applications_percent'] = declined_applications_percent

    Waitinglist_applications = len(Application.objects.filter(application_status='Waitinglist'))
    context['Waitinglist_applications'] = Waitinglist_applications
    # Waitinglist_applications_percent = 100-accepted_applications_percent-declined_applications_percent
    Waitinglist_applications_percent = int((Waitinglist_applications/number_of_applications)*100)
    context['Waitinglist_applications_percent'] = Waitinglist_applications_percent
    
    progress = 100 - int((incomplete_applications/number_of_applications)*100)
    context['progress'] = progress


    science_count = len(ParticipantProfile.objects.filter(Q(field_of_study='BSc') | Q(field_of_study='MSc')))
    context['science_count'] = science_count
    arts_count = len(ParticipantProfile.objects.filter(Q(field_of_study='BA') | Q(field_of_study='MA')))
    context['arts_count'] = arts_count
    engg_count = len(ParticipantProfile.objects.filter(Q(field_of_study='BTech') | Q(field_of_study='MTech')))
    context['engg_count'] = engg_count
    comm_count = len(ParticipantProfile.objects.filter(Q(field_of_study='BCom') | Q(field_of_study='MCom')))
    context['comm_count'] = comm_count
    school_count = len(ParticipantProfile.objects.filter(field_of_study='School'))
    context['school_count'] = school_count
    others_count = len(ParticipantProfile.objects.filter(field_of_study='Other'))
    context['others_count'] = others_count
    context['bar_graph_upper_limit'] = max(science_count, arts_count, engg_count, comm_count, school_count, others_count)

    # GENDER CHART
    total_profile = len(ParticipantProfile.objects.all())

    male_count = len(ParticipantProfile.objects.filter(gender='m'))
    # male_percent = int((male_count/total_profile)*100)
    context['male_count'] = male_count

    female_count = len(ParticipantProfile.objects.filter(gender='f'))
    # female_percent = int((female_count/total_profile)*100)
    context['female_count'] = female_count

    non_binary_count = len(ParticipantProfile.objects.filter(gender='n'))
    # non_binary_percent = int((non_binary_count/total_profile)*100)
    context['non_binary_count'] = non_binary_count

    pnts_count = len(ParticipantProfile.objects.filter(gender='na'))
    # pnts_percent = int((pnts_count/total_profile)*100)
    # pnts_percent = 100-male_percent-female_percent-non_binary_percent
    context['pnts_count'] = pnts_count

    # IEEE CHART
    is_ieee_count = len(ParticipantProfile.objects.filter(is_ieee=1))
    # is_ieee_percent = int((is_ieee_count/total_profile)*100)
    context['is_ieee_count'] = is_ieee_count
    not_ieee_count = len(ParticipantProfile.objects.filter(is_ieee=0))
    # not_ieee_percent = int((not_ieee_count/total_profile)*100)
    context['not_ieee_count'] = not_ieee_count

    # BOTTOM CARDS
    highschool_count = len(ParticipantProfile.objects.filter(educational_status='High School'))
    context['highschool_count'] = highschool_count
    bachelors_count = len(ParticipantProfile.objects.filter(educational_status='Bachelors'))
    context['bachelors_count'] = bachelors_count
    masters_count = len(ParticipantProfile.objects.filter(educational_status='Masters'))
    context['masters_count'] = masters_count
    phd_count = len(ParticipantProfile.objects.filter(educational_status='PhD'))
    context['phd_count'] = phd_count

    return render(request, 'org_db.html', context)

@login_required(login_url='login')
@organizer_view
def accept_team_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    application = team.application_team
    if application.application_status == 'Not Submitted':
        context['message'] = "The aplication has not been submitted yet"
        return (request, 'messages.html', context)
    else:
        application.application_status = 'Accepted'
        application.save()
        return redirect("organizer_dashboard")
    return render(request, 'team_detail.html', context)

@login_required(login_url='login')
@organizer_view
def decline_team_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    application = team.application_team
    if application.application_status == 'Not Submitted':
        context['message'] = "The aplication has not been submitted yet"
        return (request, 'messages.html', context)
    else:
        application.application_status = 'Declined'
        application.save()
        return redirect("organizer_dashboard")
    return render(request, 'team_detail.html', context)

@login_required(login_url='login')
@organizer_view
def waitinglist_team_view(request, team_id):
    context = {}
    team = get_object_or_404(Team, id=team_id)
    application = team.application_team
    if application.application_status == 'Not Submitted':
        context['message'] = "The aplication has not been submitted yet"
        return (request, 'messages.html', context)
    else:
        application.application_status = 'Waitinglist'
        application.save()
        return redirect("organizer_dashboard")
    return render(request, 'team_detail.html', context)


# def application_status_update_view(request, team_id):
#     context = {}
#     application = Application.objects.filter(members__id = request.user.id)
#     if request.POST:
#         status = request.POST.get('application_status')
#         if status == "Accepted":
#             application.application_status = "Accepted"
#             application.save()
#             return redirect ('organizer_dashboard')
#         elif status == "Declined":
#             application.application_status = "Declined"
#             application.save()
#             return redirect ('organizer_dashboard')
#         elif status == "Waitinglist":
#             application.application_status = "Waitinglist"
#             application.save()
#             return redirect ('organizer_dashboard')
#     return redirect('team_detail')
    # if application.application_status == 'Not Submitted':
    #     context['message'] = "The aplication has not been submitted yet"
    #     return (request, 'messages.html', context)
    # else:
    #     application.application_status = 'Accepted'
    #     application.save()
    #     return redirect("organizer_dashboard")
    # return render(request, 'team_detail.html', context)
