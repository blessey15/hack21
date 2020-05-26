from django.contrib import admin

from .models import ParticipantProfile, VolunteerProfile
# Register your models here.
class ParticipantProfileAdmin(admin.ModelAdmin):
    model = ParticipantProfile

class VolunteerProfileAdmin(admin.ModelAdmin):
    model = VolunteerProfile

admin.site.register(ParticipantProfile, ParticipantProfileAdmin)
admin.site.register(VolunteerProfile, VolunteerProfileAdmin)