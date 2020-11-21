from django import forms
 
from .models import ParticipantProfile
from .choices import *


DOB_CHOICES = []
for i in range(1901, 2099):
    DOB_CHOICES.append(str(i))
    
class PartcicpantProfileForm(forms.ModelForm):
    team_status = forms.ChoiceField(choices=TEAM_STATUS_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    name = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    contact = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    dob = forms.DateField( required=False,
        widget=forms.SelectDateWidget(years=DOB_CHOICES,
            attrs={
                "class": "form-control py-1 form-control-user dob-form"
            }
        )
    )
    gender = forms.ChoiceField( choices=GENDER_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    bio = forms.CharField( required=False,
        widget = forms.Textarea(
            attrs={
                "placeholder": "Your short bio",
                "class": "form-control py-1"
            }
        )
    )
    tshirt_size = forms.ChoiceField( choices=T_SHIRT_SIZE_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    #emergency conatct
    skills = forms.CharField( required=False,
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    educational_institution =forms.CharField( required=False,
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    field_of_study = forms.ChoiceField( required=False, choices=FIELD_OF_STUDY_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user",
            }
        )
    )
    is_ieee = forms.ChoiceField(choices=BOOLEAN_CHOICES,
        widget = forms.Select(
            attrs={
                "class": 'form-control',
            }
        )
    )
    shipping_address = forms.CharField( required=False,
        widget = forms.Textarea(
            attrs={
                "class": "form-control py-1"
            }
        )
    )
    state = forms.ChoiceField( choices=STATE_OF_RESIDENCE_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    educational_status = forms.ChoiceField(choices=EDUCATIONAL_STATUS_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    year_of_graduation = forms.ChoiceField(choices=YEAR_OF_GRADUATION_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    github_profile_link = forms.URLField( required=False,
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    twitter_profile_link = forms.URLField( required=False,
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    linkedin_profile_link = forms.URLField( required=False,
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    class Meta:
        model = ParticipantProfile
        fields = ('team_status', 'name', 'contact', 'dob', 'gender', 'bio', 'tshirt_size' ,'skills', 'educational_status',
         'educational_institution', 'field_of_study', 'year_of_graduation', 'is_ieee', 'shipping_address', 'state',
          'github_profile_link', 'twitter_profile_link', 'linkedin_profile_link')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        try:
            contact = int(contact)
        except ValueError:
            raise forms.ValidationError("The mobile number entered is not valid!!")
        return contact

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        return dob

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        return gender

    def clean_bio(self):
        bio = self.cleaned_data.get('bio')
        return bio

    def clean_tshirt_size(self):
        tshirt_size = self.cleaned_data.get('tshirt_size')
        return tshirt_size

    def clean_skills(self):
        skills = self.cleaned_data.get('skills')
        return skills
    
    def clean_educational_institution(self):
        educational_institution = self.cleaned_data.get('educational_institution')
        return educational_institution

    def clean_field_of_study(self):
        field_of_study = self.cleaned_data.get('field_of_study')
        return field_of_study