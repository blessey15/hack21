from django.shortcuts import render, redirect

from .models import Abstract
from application.models import Application
from .forms import AbstractForm

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