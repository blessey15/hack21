from django.shortcuts import render, redirect

from .forms import PartcicpantProfileForm
from .models import ParticipantProfile

# Create your views here.

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
            return redirect('profile_created')

        else:
            context['participant_profile_creation_form'] = form
    else:
        form = PartcicpantProfileForm(
            initial= {
                'name': profile.name,
                'contact': profile.contact,
                'dob': profile.dob,
                'gender': profile.gender,
                'bio': profile.bio,
                'tshirt_size': profile.tshirt_size ,
                'skills': profile.skills,
                'educational_institution': profile.educational_institution,
                'field_of_study': profile.field_of_study
            }
        )
        
        context['participant_profile_creation_form'] = form
    
    return render(request, 'profile.html', context)



def participant_profile_updated_view(request):
    return render(request, 'profile_created.html')