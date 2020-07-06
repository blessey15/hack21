from django.shortcuts import render, redirect

from .forms import PartcicpantProfileForm

# Create your views here.

def participant_profile_creation_view(request):
    context = {}
    if request.POST:
        form = PartcicpantProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_created')

        else:
            context['participant_profile_creation_form'] = form
    else:
        form = PartcicpantProfileForm()
        context['participant_profile_creation_form'] = form
    
    return render(request, 'profile.html', context)



def participant_profile_updated_view(request):
    return render(request, 'profile_created.html')