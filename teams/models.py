from django.db import models

from accounts import models as accountmodels

class Team(models.Model):
    name = models.CharField(max_length=64, blank=False)
    admin = models.ForeignKey(accountmodels.Account, on_delete=models.CASCADE, related_name='team')
    # strength = models.IntegerField(default=1)
