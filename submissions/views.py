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
        context['message'] = 'The corresponding application could nor be found!!'
        return  render(request, 'messages.html', context)
    # abstract = Abstract.objects.get_or_create(application=application)
    try:
        abstract = Abstract.objects.get(application=application)
    except Abstract.DoesNotExist:
        abstract = Abstract(application=application)
        # abstract.save()
    # if len(application)>0:
    #     application = application[0]
    if request.POST:
        form = AbstractForm(request.POST)
        context['form'] = form
        if form.is_valid():
            abstract = form.save(commit=False)
            abstract.application = application
            abstract.save()
            return redirect('submit_abstract')
        else:
            context['form'] = form
    else:
        form = AbstractForm()
        context['form'] = form
    return render(request,'submissions/submit_abstract.html', context)