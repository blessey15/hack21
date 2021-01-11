from django.db import models

from application.models import Application

PROBLEM_STATEMENT_CHOICES = (
    ('Good Health and Well-being', 'Good Health and Well-being'),
    ('Quality Education', 'Quality Education'),
    ('Industry, Innovation and Infrastructure', 'Industry, Innovation and Infrastructure'),
    ('Life on Land', 'Life on Land'),
    ('Affordable and Clean Energy', 'Affordable and Clean Energy'),
    ('Agriculture & Rural Development', 'Agriculture & Rural Development'),
)

class Abstract(models.Model):
    application = models.OneToOneField(Application,  on_delete=models.CASCADE, related_name='abstract')
    problem_statement = models.CharField(max_length=40, choices=PROBLEM_STATEMENT_CHOICES, blank=False)
    project_title = models.CharField(max_length=60, blank=False)
    abstract = models.TextField(max_length=1000, blank=False)

    date_submitted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def get_team(self):
        return self.application.team.name
    
    def get_team_size(self):
        return self.application.member_count()
    
    def __str__(self):
        return self.project_title