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
    application = models.ForeignKey(Application,  on_delete=models.CASCADE)
    problem_statement = models.CharField(max_length=40, choices=PROBLEM_STATEMENT_CHOICES, blank=False)
    project_title = models.CharField(max_length=60, blank=True)
    abstract = models.TextField(max_length=1000, blank=False)
