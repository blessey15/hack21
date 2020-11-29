import csv,xlwt

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core import mail
# HTML MAIL ESSENTIALS
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.utils.html import strip_tags
from hack21.emailthread import EmailThread

from accounts.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from application.models import Team, Application, JoinRequest
from application.forms import TeamCreateForm, TeamSearchForm
from hack21.decorators import unauthenticated_user, participant_view, organizer_view
from .models import Account
from profiles.models import ParticipantProfile
# from  application.views import create_team_view

def landing_page_view(request):
    # send_mail(
    #     'Mail Client Set',
    #     'Mail Client set aayi',
    #     'postmaster@mg.ieeemace.org',
    #     ['melvin_thomas@ieee.org'],
    #     fail_silently=False,
    # )
    # with mail.get_connection() as connection:
    #     mail.EmailMessage(
    #         'TEST MAIL SUBJECT',
    #          'TEST MAIL BODY', 
    #          'postmaster@sandbox5e247a864ddc4e418abb514b8d73e12b.mailgun.org',
    #           ['melvinchooranolil@gmail.com'],
    #         connection=connection,
    #     ).send()
    return render(request, 'index.html', {})

def sponsor_view(request):
    return render(request, 'sponsor.html', {})

def base_view(request):
    return render(request, 'base.html', {})

def temp_view(request):
    return render(request, 'home2.html', {})

def email_view(request):
    return render(request, 'emails/welcome.html', {})

@login_required(login_url='login')
@participant_view
def home(request):
    # create_team_view(request)
    context = {}
    no_teams_found = False
    try:
            profile = ParticipantProfile.objects.get(user=request.user)
    except ParticipantProfile.DoesNotExist:
        return redirect('profile-update')
    # print(application)
    # print(len(application))
    if request.user.is_authenticated:
        application = Application.objects.filter(members__id = request.user.id)
        if not(len(application) == 0):
            application = application[0]
            context['application'] = application
            team = application.team
            print("team ind")
            user_has_team = True
            context['users_team'] = team
        else:
            team = Team(admin = request.user)
            print("team indaakki")
            # team.save() 
            user_has_team = False

            # try:
            #     application = application[0]
            #     team = application.team
            #     print("team ind")
            #     user_has_team = True
            #     context['users_team'] = team
            # except Team.DoesNotExist:
            #     team = Team(admin = request.user)
            #     print("team indaakki")
            #     # team.save() 
            #     user_has_team = False

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
        context['team_form'] = team_form
        search_form = TeamSearchForm()
        context['search_form'] = search_form
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
                        return render(request, 'messages.html', context )
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
                            ctx = {'user': request.user, 'team_name': application.team.name, "team_id": application.team.id }
                            message = get_template('emails/team_created.html').render(ctx)
                            # msg = EmailMessage(
                            #     "Team Created",
                            #     message,
                            #     'hack@mg.ieeemace.org',
                            #     [request.user.email],
                            #     )
                            # msg.content_subtype = "html"
                            # msg.send()
                            subject = "Team Created"
                            recepient_list = [request.user.email]
                            EmailThread(subject, message, recepient_list).start()

                            print("Team Created message sent")
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
                        # context['message'] = 'Team Created Successfully'
                        # return render(request, 'home.html', context )
                        return redirect('home')
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
            # elif "accept_request" in request.POST:
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
            # elif "decline_request" in request.POST:
            #     pass
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

        # try:
        #     application = Application.objects.get(team=team)
        #     # context['user_has_team'] = True
        #     print("has team")
        #     context['application'] = application
        #     print(team.application_team.team.name)
        # except Application.DoesNotExist:
        #     print("except of appli in end executed")

        # if team.admin == request.user:
        #     join_requests = JoinRequest.objects.filter(team=team, request_status="Submitted")
        #     context['join_requests'] = join_requests
    return render(request, 'home.html', context )
    # return render(request, 'home.html')

@unauthenticated_user
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
            ctx = {'user': request.user}
            message = get_template('emails/welcome.html').render(ctx)
            # message = render_to_string("emails/test_template_welcome.html", ctx)
            # message = strip_tags(message)
            # msg = EmailMessage(
            #     "Welcome to .hack();",
            #     message,
            #     'hack@mg.ieeemace.org',
            #     [request.user.email],
            #     )
            # msg.content_subtype = "html"
            # msg.send()
            subject = "Welcome to .hack();"
            recepient_list = [email]
            EmailThread(subject, message, recepient_list).start()
            print("Welcome message sent")
            # ctx = {'user': request.user}
            # message = get_template('emails/account_created.html').render(ctx)
            # msg = EmailMessage(
            #     "Welcome to .hack();",
            #     message,
            #     'postmaster@mg.ieeemace.org',
            #     [request.user.email],
            #     )
            # msg.content_subtype = "html"
            # msg.send()
            # print("message sent")
            return redirect('profile-update')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'register.html', context)

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('landing_page')

@unauthenticated_user
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


@login_required(login_url='login')
def account_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = AccountUpdateForm(
            initial = {
                'email': request.user.email,
                'username': request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, 'account.html', context)



# # DATA EXPORTING THE CODE WORKS FINE, BUT COMMENTED OUT BECUSE THIS MIGHT NOT BE EXACTLY WHAT WE NEED
# @login_required(login_url='login')
# @organizer_view
# def export_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="users.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Username', 'Email address'])

#     users = Account.objects.all().values_list('username', 'email')
#     for user in users:
#         writer.writerow(user)

#     return response

# @login_required(login_url='login')
# @organizer_view
# def export_xls(request):
#     response = HttpResponse(content_type='application/ms-excel')
#     response['Content-Disposition'] = 'attachment; filename="users.xls"'

#     wb = xlwt.Workbook(encoding='utf-8')
#     ws = wb.add_sheet('Users')

#     # Sheet header, first row
#     row_num = 0

#     font_style = xlwt.XFStyle()
#     font_style.font.bold = True

#     columns = ['Username', 'Email address', ]

#     for col_num in range(len(columns)):
#         ws.write(row_num, col_num, columns[col_num], font_style)

#     # Sheet body, remaining rows
#     font_style = xlwt.XFStyle()

#     rows = Account.objects.all().values_list('username', 'email')
#     for row in rows:
#         row_num += 1
#         for col_num in range(len(row)):
#             ws.write(row_num, col_num, row[col_num], font_style)

#     wb.save(response)
#     return response

def email_template_test_view(request):
    return render(request, 'emails/test_template_password_reset.html', {})