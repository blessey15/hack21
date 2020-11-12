from django.db import models
import uuid

from accounts.models import Account
import accounts

APPLICATION_STATUS_CHOICES = (
    ('Not Submitted','Not Submitted'),
    ('Submitted','Submitted'),
    ('Under Review','Under Review'),
    ('Declined','Declined'),
    ('Waitinglist','Waitinglist'),
    ('Accepted','Accepted'),
)

REQUEST_STATUS_CHOICES = (
    ("Submitted", "Submitted"),
    ("Declined", "Declined"),
    ("Accepted", "Accepted"),
)
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    name = models.CharField(max_length=64, blank=False)
    admin = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='team')
    # strength = models.IntegerField(default=0)
    # application_status = models.CharField(max_length=14, choices=APPLICATION_STATUS_CHOICES, default='Not Submitted')
    # members = models.ManyToManyField(Account, related_name='team_name')

    def __str__(self):
        return self.name

class Application(models.Model):
    team = models.OneToOneField(Team, related_name='application_team', on_delete=models.CASCADE)
    members = models.ManyToManyField(Account, related_name='application_team')
    # member_count = models.IntegerField(blank=False, default=0)
    application_status = models.CharField(max_length=14, choices=APPLICATION_STATUS_CHOICES, default='Not Submitted')

    def team_members(self):
        return ',  '.join([str(m) for m in self.members.all()])
    
    def member_count(self):
        return len(self.members.all())

    def __str__(self):
        return self.team.name

class JoinRequest(models.Model):
    team = models.ForeignKey(Team, related_name='request_team', on_delete=models.CASCADE)
    user = models.OneToOneField(Account, related_name='join_request', on_delete=models.CASCADE)
    request_status = models.CharField(max_length=14, choices=REQUEST_STATUS_CHOICES, default='Not Submitted')
