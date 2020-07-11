from django import forms
 
from .models import ParticipantProfile, GENDER_CHOICES,T_SHIRT_SIZE_CHOICES, FIELD_OF_STUDY_CHOICES

class PartcicpantProfileForm(forms.ModelForm):
    # name = forms.CharField(max_length=256, blank=False)
    # # email = forms.EmailField(max_length=256, blank=False, unique=True)
    # contact = forms.IntegerField( blank=False)
    # dob = forms.DateField()
    # gender = forms.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
    # bio = forms.TextField()
    # tshirt_size = forms.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')
    # #emergency conatct
    # skills = forms.TextField()
    # educational_institution = forms.CharField(max_length= 128)
    # field_of_study = forms.CharField(max_length=64, choices=FIELD_OF_STUDY_CHOICES, blank=True, verbose_name='Field of Study')
    class Meta:
        model = ParticipantProfile
        fields = ('name', 'contact', 'dob', 'gender', 'bio', 'tshirt_size' ,'skills', 'educational_institution', 'field_of_study')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return name

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
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