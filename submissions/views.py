from django.shortcuts import render, redirect
# HTML MAIL ESSENTIALS
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required


from .models import Abstract
from application.models import Application
from .forms import AbstractForm
from hack21.emailthread import EmailThread


@login_required(login_url='login')
def submit_abstract_view(request):
    context = {}
    # application = request.user.application_set.all()
    applications = Application.objects.filter(members__id = request.user.id)
    if len(applications)>0:
        application = applications[0]
    else:
        context['message'] = 'The corresponding application could not be found!!'
        return  render(request, 'messages.html', context)
    # abstract = Abstract.objects.get_or_create(application=application)
    if application.application_status == "Accepted":

        if request.user == application.team.admin:
            try:
                abstract = Abstract.objects.get(application=application)
            except Abstract.DoesNotExist:
                abstract = Abstract(application=application)
                # abstract.save()
            # if len(application)>0:
            #     application = application[0]
            if request.POST:
                form = AbstractForm(request.POST, instance=abstract)
                context['form'] = form
                if form.is_valid():
                    abstract = form.save(commit=False)
                    abstract.application = application
                    abstract.save()
                    ctx = {
                        'user': request.user,
                        'team_name': application.team.name,
                        'team_id': application.team.id,
                        'admin': application.team.admin.profile.name 
                    }
                    # MAIL TO TEAM ADMIN NOTIFYING OF TEAM DELETE
                    message1 = get_template('emails/abstract_submitted_admin_mail.html').render(ctx)
                    # msg1 = EmailMessage(
                    #     "Team Deleted",
                    #     message1,
                    #     'hack@mg.ieeemace.org',
                    #     [application.team.admin.email],
                    #     )
                    # msg1.content_subtype = "html"
                    # msg1.send()
                    subject = "Project Abstract Submitted"
                    recepient_list = [application.team.admin.email]
                    EmailThread(subject, message1, recepient_list).start()
                    print("Abstract Submission message sent to ADMIN")

                    # MAIL TO MEMBER NOTIFYING TEAM DELETE
                    message2 = get_template('emails/abstract_submitted_member_mail.html').render(ctx)
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
                    subject = "Project Abstract Submitted"
                    # recepient_list = [application.team.admin.email]
                    EmailThread(subject, message2, recepient_list).start()
                    print("Abstract Submission message sent to MEMBER")
                    if application.abstract_submitted == False:
                        application.abstract_submitted=True
                        application.save()
                    return redirect('home')
                else:
                    context['form'] = form
            else:
                form = AbstractForm(
                    initial={
                        'problem_statement': abstract.problem_statement,
                        'project_title': abstract.project_title,
                        'abstract': abstract.abstract,
                    }
                )
                context['form'] = form
        else:
            context['message'] = "You are not the Admin of this team. Only Team admins can submit an abstract"
            return  render(request, 'messages.html', context)
    else:
        context['message'] = "Only accepted teams can submit a project abstract!!"
        return  render(request, 'messages.html', context)

    return render(request,'submissions/submit_abstract.html', context)

@login_required(login_url='login')
def view_abstract(request):
    context = {}
    applications = Application.objects.filter(members__id = request.user.id)
    if len(applications)>0:
        application = applications[0]
    else:
        context['message'] = 'The corresponding application could not be found!!'
        return  render(request, 'messages.html', context)
    try:
        abstract = Abstract.objects.get(application=application)
        context['abstract'] = abstract
    except Abstract.DoesNotExist:
        context['message'] = 'The corresponding Abstract could not be found!!'
        return  render(request, 'messages.html', context)
    return render(request, 'submissions/abstract.html', context)
