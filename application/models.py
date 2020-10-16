from django.db import models

from accounts.models import Account

APPLICATION_STATUS_CHOICES = (
    (1,'Submitted'),
    (2,'Declined'),
    (3,'Waitinglist'),
    (4,'Accepted'),
)
class Team(models.Model):
    name = models.CharField(max_length=64, blank=False)
    admin = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='team')
    # strength = models.IntegerField(default=1)
    application_status = models.IntegerField(choices=APPLICATION_STATUS_CHOICES)
