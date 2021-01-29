from django.db import models

from application.models import Application

PROBLEM_STATEMENT_CHOICES = (
    ('Good Health and Well-being', 'Good Health and Well-being'),
    ('Quality Education', 'Quality Education'),
    ('Industry, Innovation and Infrastructure', 'Industry, Innovation and Infrastructure'),
    ('Life on Land', 'Life on Land'),
    ('Affordable and Clean Energy', 'Affordable and Clean Energy'),
    ('Agriculture & Rural Development', 'Sustainable Cities and Communities'),
)

class Abstract(models.Model):
    application = models.OneToOneField(Application,  on_delete=models.CASCADE, related_name='abstract')
    problem_statement = models.CharField(max_length=40, choices=PROBLEM_STATEMENT_CHOICES, blank=False)
    project_title = models.CharField(max_length=60, blank=False)
    abstract = models.TextField(max_length=2000, blank=False)

    date_submitted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def get_team(self):
        return self.application.team.name
    
    def get_team_size(self):
        return self.application.member_count()
    
    def __str__(self):
        return self.project_title


class Submission(models.Model):
    application = models.OneToOneField(Application,  on_delete=models.CASCADE, related_name='submission')
    video_link = models.URLField(verbose_name="Link to video of project", blank=False)
    code_link = models.URLField(verbose_name="Link To Code", blank=False)
    ppt_link = models.URLField(verbose_name="Link To Presentation", blank=False)

    date_submitted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def get_team(self):
        return self.application.team.name
    
    def get_team_size(self):
        return self.application.member_count()
    
    def __str__(self):
        return self.project_title