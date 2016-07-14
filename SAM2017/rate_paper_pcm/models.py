from django.db import models
from paper.models import Paper
from registration.models import User


# Create your models here.
class Paper_PCM_Rate(models.Model):
    pcm = models.ForeignKey(User)
    paper = models.ForeignKey(Paper)
    review = models.TextField(null=False)
    decision = models.IntegerField()  # 0 = rejected; 1 = accepted; 2 = accepted with modification

    has_conflict = models.BooleanField(default=False)

    def __str__(self):
        return 'Reviewer: ' + str(self.pcm.email) + ' Paper name: ' + self.paper.title