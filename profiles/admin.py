from django.contrib import admin

from .models import ParticipantProfile #VolunteerProfile
# Register your models here.
class ParticipantProfileAdmin(admin.ModelAdmin):
    # model = ParticipantProfile
    list_display = ( 'name', 'gender', 'field_of_study', 'educational_institution', 'tshirt_size')

# class VolunteerProfileAdmin(admin.ModelAdmin):
#     model = VolunteerProfile

admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
# admin.site.register(VolunteerProfile, VolunteerProfileAdmin) 