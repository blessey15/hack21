from django import forms
from django.core.validators import URLValidator
 
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
                "class": "form-control py-1 form-control-user",
                "placeholder": "Enter Your Name"
            }
        )
    )
    contact = forms.CharField(
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "so we can reach out to you"
            }
        )
    )
    dob = forms.DateField( required=True,
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
    bio = forms.CharField( required=False,help_text="Tell us more about yourself and why you want to be a part of .hack();",
        widget = forms.Textarea(
            attrs={
                "placeholder": "Your short bio",
                "class": "form-control py-1"
            }
        )
    )
    tshirt_size = forms.ChoiceField( choices=T_SHIRT_SIZE_CHOICES, help_text="You got it. We are shipping tshirts and other goodies to top 200 participants.",
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    #emergency conatct
    skills = forms.CharField( required=False,help_text="Tell us about your skills so that we can choose the best candidates",
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    educational_institution =forms.CharField( required=True, help_text="Just making sure you are a student.",
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    field_of_study = forms.ChoiceField( required=True, choices=FIELD_OF_STUDY_CHOICES,
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user",
            }
        )
    )
    is_ieee = forms.ChoiceField(choices=BOOLEAN_CHOICES, label="Are you an IEEE Member?", help_text=".hack(); is open to all college and school students. We are just curious to know how many IEEEians are among the innovators.",
        widget = forms.Select(
            attrs={
                "class": 'form-control py-1 form-control-user',
            }
        )
    )
    shipping_address = forms.CharField( required=True,help_text="This will be used to ship your prizes and the goodies for top teams.",
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
    pin_code = forms.CharField( required=True,
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Enter Pin Code"
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
    avatar_choice = forms.ChoiceField( choices=AVATAR_CHOICES, help_text="Just curious to know more...", 
    label="Which of the following characters do you relate yourself to the most?",
        widget = forms.Select(
            attrs={
                "class": "form-control py-1 form-control-user"
            }
        )
    )
    website_link = forms.URLField( required=False,
        error_messages = {
            'invalid': "Please enter a valid URL or leave it blank"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to your Personal Website"
            }
        )
    )
    github_profile_link = forms.URLField( required=False,
        error_messages = {
            'invalid': "Please enter a valid URL or leave it blank"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to your GitHub Profile"
            }
        )
    )
    twitter_profile_link = forms.URLField( required=False,
        error_messages = {
            'invalid': "Please enter a valid URL or leave it blank"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to your Twitter Profile"
            }
        )
    )
    linkedin_profile_link = forms.URLField( required=False,
        error_messages = {
            'invalid': "Please enter a valid URL or leave it blank"
        },
        widget = forms.URLInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Link to your LinkedIn Profile"
            }
        )
    )
    referral_id = forms.CharField( required=False,
        widget = forms.TextInput(
            attrs={
                "class": "form-control py-1 form-control-user",
                "placeholder": "Enter Referral ID"
            }
        )
    )
    class Meta:
        model = ParticipantProfile
        fields = ('team_status', 'name', 'contact', 'dob', 'gender', 'bio', 'tshirt_size' ,'skills', 'educational_status',
         'educational_institution', 'field_of_study', 'year_of_graduation', 'is_ieee', 'shipping_address', 'state', 'pin_code', 
         'avatar_choice', 'website_link','github_profile_link', 'twitter_profile_link', 'linkedin_profile_link', 'referral_id')

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
    # def clean_website_link(self):
    #     website_link = self.cleaned_data.get('website_link')
    #     try:
    #         URLValidator(website_link)
    #         print("validating URL")
    #         return website_link
    #     except:
    #         raise forms.ValidationError("Enter a valid URL or leave it blank")