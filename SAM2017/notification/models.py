from django.db import models
from registration.models import User

import datetime


# Create your models here.
class Notifications(models.Model):
    sender = models.ForeignKey(User, related_name='Sender')
    receiver = models.ForeignKey(User, related_name='Receiver')
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return str(self.id) + ': ' + self.sender.first_name
