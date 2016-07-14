from django.db import models
from registration.models import User
# Create your models here.


class Paper(models.Model):
    PHONE = "PHO"

    EMAIL = "EMA"

    contact_choices = (
        (PHONE, "Cell phone"),
        (EMAIL, "E-mail"),
    )

    PDF = "PDF"

    WORD = "WOR"

    format_choices = (
        (PDF, "Adobe PDF"),
        (WORD, "Microsoft Word"),
    )

    ALLOWED_FORMATS = ['pdf', 'doc', 'docx']

    submitter = models.ForeignKey(User, related_name='users', db_index=True)
    title = models.CharField(max_length=50)
    list_of_authors = models.CharField(max_length=150, help_text='Ex.: author1, author2, etc...')
    preferred_contact_method = models.CharField(max_length=3, choices=contact_choices)
    has_conflict = models.BooleanField(default=False)
    format = models.CharField(max_length=3, choices=format_choices)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    final_rating = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id) + ': ' + self.title

    def get_contact_method(self):
        return dict(self.contact_choices).get(self.preferred_contact_method)

    def get_contact(self):
        if self.preferred_contact_method == self.PHONE:
            return "852-852-8520"

        elif self.preferred_contact_method == self.EMAIL:
            return self.submitter.email

    def get_format(self):
        return dict(self.format_choices).get(self.format)


class PCMs_Papers(models.Model):
    pcm = models.ForeignKey(User)
    paper = models.ForeignKey(Paper)
    is_assigned = models.BooleanField(default=False)

    def __str__(self):
        return 'Chosen paper ' + self.paper.title


class Submission(models.Model):
    file = models.FileField(upload_to="papers/%Y/%m/%d")
    paper = models.ForeignKey(Paper, related_name='submissions')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.paper.title


# class Notifications(models.Model):
#     sender = models.ForeignKey(User, related_name='Sender')
#     receiver = models.ForeignKey(User, related_name='Receiver')
#     message = models.TextField()
#     is_seen = models.BooleanField(default=False)
#
#     def __str__(self):
#         return str(self.id) + ': ' + self.sender.first_name
