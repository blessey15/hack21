import csv, xlwt

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# HTML MAIL ESSENTIALS
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

from .forms import PartcicpantProfileForm
from .models import ParticipantProfile
from accounts.models import Account
from hack21.decorators import organizer_view
from hack21.emailthread import EmailThread
# Create your views here.

@login_required(login_url='login')
def participant_profile_creation_view(request):
    context = {}
    try:
        profile = request.user.profile
    except ParticipantProfile.DoesNotExist:
        profile = ParticipantProfile(user = request.user)

    # if request.user.has_profile:
    #     profile = request.user.profile
    # else:
    #     profile = ParticipantProfile(user = request.user)

    if request.POST:
        form = PartcicpantProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            # profile.user.has_profile = True
            profile.save()
            if not profile.welcome_mail_sent:
                ctx = {'user': request.user}
                message = get_template('emails/welcome.html').render(ctx)
                subject = "Welcome to .hack();"
                recepient_list = [request.user.email]
                EmailThread(subject, message, recepient_list).start()
                profile.welcome_mail_sent = True
                profile.save()
                print("Welcome message sent")
            return redirect('home')

        else:
            context['form'] = form
    else:
        form = PartcicpantProfileForm(
            initial= {
                'team_status': profile.team_status,
                'name': profile.name,
                'contact': profile.contact,
                'dob': profile.dob,
                'gender': profile.gender,
                'bio': profile.bio,
                'tshirt_size': profile.tshirt_size ,
                'skills': profile.skills,
                'educational_status': profile.educational_status,
                'educational_institution': profile.educational_institution,
                'field_of_study': profile.field_of_study,
                'year_of_graduation': profile.year_of_graduation,
                'is_ieee': profile.is_ieee,
                'shipping_address': profile.shipping_address,
                'state': profile.state,
                'avatar_choice': profile.avatar_choice,
                'website_link': profile.website_link,
                'github_profile_link': profile.github_profile_link,
                'twitter_profile_link': profile.twitter_profile_link,
                'linkedin_profile_link': profile.linkedin_profile_link,
                
            }
        )
        
        context['form'] = form
    
    return render(request, 'create_profile.html', context)


@login_required(login_url='login')
def participant_profile_updated_view(request):
    return render(request, 'profile_created.html')



@login_required(login_url='login')
@organizer_view
def participant_profile_view(request, id):
    context = {}
    user = get_object_or_404(Account, id=id)
    profile = user.profile
    context['user'] = user
    context['profile'] = profile
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def own_profile_view(request):
    context = {}
    user = request.user
    profile = user.profile
    context['user'] = user
    context['profile'] = profile
    return render(request, 'profile.html', context)


# DATA EXPORTING
@login_required(login_url='login')
@organizer_view
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="profiles.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact', 'Date of Birth', 'Gender', 'Educational Status', 'Educational Institution', 
    'Field of study', 'Year of Graduation', 'Is IEEE', 'Shipping Address', 'State of Residence', 'Personal Website', 'GitHub','Twitter', 'LinkedIn'])

    profiles = ParticipantProfile.objects.all().values_list('name', 'contact', 'dob', 'gender', 'educational_status','website_link',
    'educational_institution', 'field_of_study', 'year_of_graduation', 'is_ieee', 'shipping_address', 'state', 
      'github_profile_link', 'twitter_profile_link', 'linkedin_profile_link',)
    for profile in profiles:
        writer.writerow(profile)

    return response

@login_required(login_url='login')
@organizer_view
def export_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="profiles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('profiles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Contact', 'Gender', 'Educational Status', 'Educational Institution', 
    'Field of study', 'Year of Graduation', 'Is IEEE', 'Shipping Address', 'State of Residence', 'Personal Website', 'GitHub','Twitter', 'LinkedIn']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = ParticipantProfile.objects.all().values_list('name', 'contact', 'gender', 'educational_status',
    'educational_institution', 'field_of_study', 'year_of_graduation', 'is_ieee', 'shipping_address', 'state', 'website_link',
      'github_profile_link', 'twitter_profile_link', 'linkedin_profile_link',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response