from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# HTML MAIL ESSENTIALS
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage


from .forms import TeamCreateForm
from .models import Application, Team, JoinRequest
from accounts.models import Account
from profiles.models import ParticipantProfile
from accounts.views import home
from hack21.decorators import organizer_view, participant_view
from hack21.emailthread import EmailThread
from .forms import SendCustomEmailForm
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
                        ctx = {
                            'user': request.user,
                            'team_name': application.team.name,
                            'team_id': application.team.id,
                            'admin': application.team.admin.profile.name 
                            }
                        # MAIL TO TEAM ADMIN NOTIFYING OF NEW MEMBER JOINING
                        message1 = get_template('emails/join_team_admin_mail.html').render(ctx)
                        # msg1 = EmailMessage(
                        #     "New Memeber Notification",
                        #     message1,
                        #     'hack@mg.ieeemace.org',
                        #     [application.team.admin.email],
                        #     )
                        # msg1.content_subtype = "html"
                        # msg1.send()
                        subject = "New Memeber Notification"
                        recepient_list = [application.team.admin.email]
                        EmailThread(subject, message1, recepient_list).start()
                        print("Team Join message sent to ADMIN")

                        # MAIL TO PARTICIPANT CONFIRMING TEAM JOINING
                        message2 = get_template('emails/join_team_member_mail.html').render(ctx)
                        # msg2 = EmailMessage(
                        #     "Joined Team",
                        #     message2,
                        #     'hack@mg.ieeemace.org',
                        #     [request.user.email],
                        #     )
                        # msg2.content_subtype = "html"
                        # msg2.send()
                        subject = "Joined Team"
                        recepient_list = [request.user.email]
                        EmailThread(subject, message2, recepient_list).start()
                        print("Team Join message sent to MEMBER")
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
    ctx = {
        'user': request.user,
        'team_name': application.team.name,
        'team_id': application.team.id,
        'admin': application.team.admin.profile.name 
        }
    if application.application_status == 'Not Submitted':
        if request.user == team.admin:
            
            # MAIL TO TEAM ADMIN NOTIFYING OF TEAM DELETE
            message1 = get_template('emails/delete_team_admin_mail.html').render(ctx)
            # msg1 = EmailMessage(
            #     "Team Deleted",
            #     message1,
            #     'hack@mg.ieeemace.org',
            #     [application.team.admin.email],
            #     )
            # msg1.content_subtype = "html"
            # msg1.send()
            subject = "Team Deleted"
            recepient_list = [application.team.admin.email]
            EmailThread(subject, message1, recepient_list).start()
            print("Team Delete message sent to ADMIN")

            # MAIL TO MEMBER NOTIFYING TEAM DELETE
            message2 = get_template('emails/delete_team_member_mail.html').render(ctx)
            recepient_list = []
            for member in application.members.all():
                if not (member == request.user):
                    recepient_list.append(member.email)
            # msg2 = EmailMessage(
            #     "Your Team was Deleted!",
            #     message2,
            #     'hack@mg.ieeemace.org',
            #     recepient_list,
            #     )
            # msg2.content_subtype = "html"
            # msg2.send()
            subject = "Your Team was Deleted!"
            # recepient_list = [application.team.admin.email]
            EmailThread(subject, message2, recepient_list).start()
            print("Team Delete message sent to MEMBER")
            application.delete()
            context['application'] = None
            team.delete()

            context['team'] = None
            return redirect('home')
        else:
            application.members.remove(request.user)
            # MAIL TO TEAM ADMIN NOTIFYING OF NEW MEMBER JOINING
            message1 = get_template('emails/leave_team_admin_mail.html').render(ctx)
            # msg1 = EmailMessage(
            #     "Member Leaving Team",
            #     message1,
            #     'hack@mg.ieeemace.org',
            #     [application.team.admin.email],
            #     )
            # msg1.content_subtype = "html"
            # msg1.send()
            subject = "Member Leaving Team"
            recepient_list = [application.team.admin.email]
            EmailThread(subject, message1, recepient_list).start()
            print("Member Leaving message sent to ADMIN")

            # MAIL TO PARTICIPANT CONFIRMING TEAM JOINING
            message2 = get_template('emails/leave_team_member_mail.html').render(ctx)
            # msg2 = EmailMessage(
            #     "You Left a Team",
            #     message2,
            #     'hack@mg.ieeemace.org',
            #     [request.user.email],
            #     )
            # msg2.content_subtype = "html"
            # msg2.send()
            subject = "You Left a Team"
            recepient_list = [request.user.email]
            EmailThread(subject, message2, recepient_list).start()
            print("Team Leaving message sent to MEMBER")

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
            # elif len(application.members.all()) < 2:
            #     context['message'] = "You need atleast 2 people in a team!!."
            #     return render(request, 'messages.html', context)
            else:
                application.application_status = 'Submitted'
                application.save()
                ctx = {
                        'user': request.user,
                        'team_name': application.team.name,
                        'team_id': application.team.id,
                        'admin': application.team.admin.profile.name 
                        }
                recepient_list = []
                for member in application.members.all():
                    recepient_list.append(member.email)
                message = get_template('emails/application_submitted_mail.html').render(ctx)
                # msg = EmailMessage(
                #     "Application SUbmitted",
                #     message,
                #     'hack@mg.ieeemace.org',
                #     recepient_list,
                #     )
                # msg.content_subtype = "html"
                # msg.send()
                subject = "Application Submitted"
                # recepient_list = [request.user.email]
                EmailThread(subject, message, recepient_list).start()
                print("Application Submission message sent")
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
    # review_pending_applications_percent = int((review_pending_applications/number_of_applications)*100)
    # context['review_pending_applications_percent'] = review_pending_applications_percent

    accepted_applications = len(Application.objects.filter(application_status='Accepted'))
    context['accepted_applications'] = accepted_applications
    # accepted_applications_percent = int((accepted_applications/number_of_applications)*100)
    # context['accepted_applications_percent'] = accepted_applications_percent

    declined_applications = len(Application.objects.filter(application_status='Declined'))
    context['declined_applications'] = declined_applications
    # declined_applications_percent = int((declined_applications/number_of_applications)*100)
    # context['declined_applications_percent'] = declined_applications_percent

    Waitinglist_applications = len(Application.objects.filter(application_status='Waitinglist'))
    context['Waitinglist_applications'] = Waitinglist_applications
    # Waitinglist_applications_percent = 100-accepted_applications_percent-declined_applications_percent
    # Waitinglist_applications_percent = int((Waitinglist_applications/number_of_applications)*100)
    # context['Waitinglist_applications_percent'] = Waitinglist_applications_percent
    
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
# @organizer_view
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
# @organizer_view
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
# @organizer_view
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

@login_required
# @organizer_view
def send_accepted_email(request):
    context = {}
    applications = Application.objects.filter(application_status="Accepted", received_confirmation_mail=False)
    subject = "You've been accepted!!"
    for application in applications:
        print("mailing "+str(application.team.name))
        for member in application.members.all():
            ctx = {'application': application, 'member': member, 'team': application.team.name }
            message = get_template('emails/application_accepted.html').render(ctx)
            recepient_list = [member.email]
            EmailThread(subject, message, recepient_list).start()
            print("Acceptace mail sent")
        application.received_confirmation_mail = True
        application.save()
    return redirect('organizer_dashboard')
    

@login_required
# @organizer_view
def send_declined_email(request):
    context = {}
    applications = Application.objects.filter(application_status="Declined", received_confirmation_mail=False)
    subject = "Uh oh You've been Turned Down"
    for application in applications:
        print("mailing "+str(application.team.name))
        for member in application.members.all():
            ctx = {'application': application, 'member': member}
            message = get_template('emails/application_declined.html').render(ctx)
            recepient_list = [member.email]
            EmailThread(subject, message, recepient_list).start()
            print("Declination Mail sent")
        application.received_confirmation_mail = True
        application.save()
    return redirect('organizer_dashboard')
    

@login_required
# @organizer_view
def send_wtlst_email(request):
    context = {}
    applications = Application.objects.filter(application_status="Waitinglist")
    subject = "Application review in progress"
    for application in applications:
        print("mailing "+str(application.team.name))
        for member in application.members.all():
            ctx = {'application': application, 'member': member}
            message = get_template('emails/application_waitinglist.html').render(ctx)
            recepient_list = [member.email]
            EmailThread(subject, message, recepient_list).start()
            print("Waiting List Mail sent")
    return redirect('organizer_dashboard')

@login_required
# @organizer_view
def send_not_submitted_email(request):
    context = {}
    applications = Application.objects.filter(application_status="Not Submitted")
    subject = "Knock Knock Did you forget to submit your application?"
    for application in applications:
        ctx = {}
        ctx['application': application]
        print("mailing "+str(application.team.name))
        for member in application.members.all():
            ctx['member'] = member
            message = get_template('emails/not_submitted_reminder.html').render(ctx)
            recepient_list = [member.email]
            EmailThread(subject, message, recepient_list).start()
            print("Not SUbmitted Reminder Mail sent")
    return redirect('organizer_dashboard')

@login_required
# @organizer_view
def send_custom_mail_view(request):
    context = {}
    form = SendCustomEmailForm()
    context['form'] = form
    if request.POST:
        form = SendCustomEmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            content = form.cleaned_data.get('message')
            group = form.cleaned_data.get('group')
            applications = Application.objects.filter(application_status=group)
            for application in applications:
                ctx = {'message': content}
                for member in application.members.all():
                    ctx['user'] = member
                    message = get_template('emails/custom_mail.html').render(ctx)
                    recepient_list = [member.email]
                    EmailThread(subject, message, recepient_list).start()
        else:
            context['form'] = form
    else:
        context['form'] = form
    return render(request, 'custom_mails.html', context)

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
