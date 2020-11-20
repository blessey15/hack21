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
            return redirect('home')

        else:
            context['participant_profile_creation_form'] = form
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
                'github_profile_link': profile.github_profile_link,
                'twitter_profile_link': profile.twitter_profile_link,
                'linkedin_profile_link': profile.linkedin_profile_link,
                
            }
        )
        
        context['participant_profile_creation_form'] = form
    
    return render(request, 'create_profile.html', context)



def participant_profile_updated_view(request):
    return render(request, 'profile_created.html')