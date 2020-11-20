from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# from user.models import CustomUser
from accounts.models import Account
from .choices import *
# Create your models here.

class ParticipantProfile(models.Model):
    user = models.OneToOneField(Account, related_name='profile', on_delete=models.CASCADE)

    team_status = models.CharField(max_length=10, choices=TEAM_STATUS_CHOICES, default='Has Team', blank=False)
    name = models.CharField(max_length=256, blank=False)
    contact = models.CharField(max_length=13, blank=False)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
    bio = models.TextField()
    tshirt_size = models.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')
    #emergency conatct
    skills = models.TextField()
    educational_institution = models.CharField(max_length= 128)
    field_of_study = models.CharField(max_length=64, choices=FIELD_OF_STUDY_CHOICES, blank=True, verbose_name='Field of Study')
    is_ieee = models.BooleanField(default=False, blank=False, verbose_name="Are you an IEEE member?")
    shipping_address = models.TextField(blank=False, default=' ')
    state = models.CharField(max_length=41, choices=STATE_OF_RESIDENCE_CHOICES, blank=False, default='Kerala', verbose_name='State/Province of Residence')
    educational_status = models.CharField(max_length=12, blank=False, choices=EDUCATIONAL_STATUS_CHOICES, default='Bachelors')
    year_of_graduation = models.IntegerField(choices=YEAR_OF_GRADUATION_CHOICES, blank=False, default=2023)
    # previous_projects
    github_profile_link = models.URLField(verbose_name="GitHub Profile Link", blank=True)
    twitter_profile_link = models.URLField(verbose_name="Twitter Profile Link", blank=True)
    linkedin_profile_link = models.URLField(verbose_name="LinkedIn Profile Link", blank=True)
    # resume_link = models.URLField(verbose_name="Link to your resume", blank=True)

    def __str__(self):
        return self.user.email

# @receiver(post_save, sender=Account)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         ParticipantProfile.objects.create(user=instance)
#     instance.ParticipantProfile.save()


# class VolunteerProfile(models.Model):
#     user = models.OneToOneField(Account, on_delete=models.CASCADE)
#     batch = models.CharField(max_length=4, blank=False, default=' ', choices=CLASS_CHOICES)
#     name = models.CharField(max_length=256, blank=False)
#     email = models.EmailField(max_length=256, blank=False, unique=True)
#     contact = models.IntegerField( blank=False)
#     dob = models.DateField()
#     gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
#     tshirt_size = models.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')

# class OrganizerProfile(moels.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     batch = models.CharField(max_length=4, blank=False, default=' ', choices=CLASS_CHOICES)
#     name = models.CharField(max_length=256, blank=False)
#     contact = models.IntegerField( blank=False)
#     dob = models.DateField()
#     gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)