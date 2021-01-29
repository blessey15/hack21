from django.contrib import admin

from .models import Abstract, Submission

class AbstractAdmin(admin.ModelAdmin):
    list_display = ('get_team', 'problem_statement', 'project_title', 'get_team_size')
    search_fields = ('get_team', 'project_title')
    # list_filter = ('get_team_size',)
    readonly_fields = ('date_submitted', 'last_modified')

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('get_team',)
    search_fields = ('get_team',)
    # list_filter = ('get_team_size',)
    readonly_fields = ('date_submitted', 'last_modified')



admin.site.register(Abstract, AbstractAdmin)
admin.site.register(Submission, SubmissionAdmin)

# Register your models here.
