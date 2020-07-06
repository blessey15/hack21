from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import CustomUser
from accounts.models import Account
# Create your models here.

GENDER_CHOICES=(
    ('m','Male'),
    ('f','Female'),
    ('n',"Non Binary"),
    ('na', 'Prefer not to say',)
)
T_SHIRT_SIZE_CHOICES=(
    ('S','S'),
    ('M','M'),
    ('L','L'),
    ('XL','XL'),
    ('XXL','XXL')
)
FIELD_OF_STUDY_CHOICES=(
    ('cs','Computer Science'),
    ('ec','Electronics and Communication'),
    ('me','Mechanical Engineering'),
    ('ce','Civil Engineering'),
    ('ee','Electrical and Electronis Engineering'),
    ('it','Information Technology')
)
CLASS_CHOICES=(
    (' ',' '),
    ('S1R','S1R'),('S3R','S3R'),('S5R','S5R'),('S7R','S7R'),
    ('S1LA','S1LA'),('S1LB','S1LB'),('S3LA','S3LA'),('S3LB','S3LB'),('S5LA','S5LA'),('S5LB','S5LB'),('S7LA','S7LA'),('S7LB','S7LB'),
    ('S1EA','S1EA'),('S1EB','S1EB'),('S3EA','S3EA'),('S3EB','S3EB'),('S5EA','S5EA'),('S5EB','S5EB'),('S7EA','S7EA'),('S7EB','S7EB'),
    ('S1CA','S1CA'),('S1CB','S1CB'),('S3CA','S3CA'),('S3CB','S3CB'),('S5CA','S5CA'),('S5CB','S5CB'),('S7CA','S7CA'),('S7CB','S7CB'),
    ('S1MA','S1MA'),('S1MB','S1MB'),('S3MA','S3MA'),('S3MB','S3MB'),('S5MA','S5MA'),('S5MB','S5MB'),('S7MA','S7MA'),('S7MB','S7MB'),   
)

class ParticipantProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)

    name = models.CharField(max_length=256, blank=False)
    contact = models.IntegerField( blank=False)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
    bio = models.TextField()
    tshirt_size = models.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')
    #emergency conatct
    skills = models.TextField()
    educational_institution = models.CharField(max_length= 128)
    field_of_study = models.CharField(max_length=64, choices=FIELD_OF_STUDY_CHOICES, blank=True, verbose_name='Field of Study')

    def __str__(self):
        return self.user.email

# @receiver(post_save, sender=Account)
# def create_or_update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         ParticipantProfile.objects.create(user=instance)
#     instance.ParticipantProfile.save()


class VolunteerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    batch = models.CharField(max_length=4, blank=False, default=' ', choices=CLASS_CHOICES)
    name = models.CharField(max_length=256, blank=False)
    email = models.EmailField(max_length=256, blank=False, unique=True)
    contact = models.IntegerField( blank=False)
    dob = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)
    tshirt_size = models.CharField(max_length=3, choices=T_SHIRT_SIZE_CHOICES, verbose_name='T-Shirt Size')

# class OrganizerProfile(moels.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     batch = models.CharField(max_length=4, blank=False, default=' ', choices=CLASS_CHOICES)
#     name = models.CharField(max_length=256, blank=False)
#     contact = models.IntegerField( blank=False)
#     dob = models.DateField()
#     gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=False)