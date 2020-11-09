from django.contrib import admin

from .models import Team, Application, JoinRequest

class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin',)
    search_fields = ('name','admin')

class ApplicationAdim(admin.ModelAdmin):
    list_display = ('team', 'team_members', 'member_count', 'application_status',)
    search_fields = ('team',)
    list_filter = ('application_status', )

    # def members(self, obj):
    #     return "\n".join(t.members for t in obj.Team.all()

class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'team', 'request_status',)
    search_fields = ('team',)
    

admin.site.register(Team, TeamAdmin) 
admin.site.register(Application, ApplicationAdim) 
admin.site.register(JoinRequest, JoinRequestAdmin) 
