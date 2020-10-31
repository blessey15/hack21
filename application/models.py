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
class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_column='id')
    name = models.CharField(max_length=64, blank=False)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='team')
    # strength = models.IntegerField(default=0)
    # application_status = models.CharField(max_length=14, choices=APPLICATION_STATUS_CHOICES, default='Not Submitted')
    # members = models.ManyToManyField(Account, related_name='team_name')

    def __str__(self):
        return self.name

class Application(models.Model):
    team = models.OneToOneField(Team, related_name='application_team', on_delete=models.CASCADE)
    members = models.ManyToManyField(Account, related_name='application_user')
    application_status = models.CharField(max_length=14, choices=APPLICATION_STATUS_CHOICES, default='Not Submitted')

class JoinRequest(models.Model):
    team = models.OneToOneField(Team, related_name='request_team', on_delete=models.CASCADE)
    user = models.OneToOneField(Account, related_name='request_user', on_delete=models.CASCADE)
    application_status = models.CharField(max_length=14, choices=APPLICATION_STATUS_CHOICES, default='Not Submitted')