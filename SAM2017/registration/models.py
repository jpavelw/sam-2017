from django.db import models


class Role(models.Model):
    # Jairo added the code field

    AUT = "AUT"
    PCM = "PCM"
    PCC = "PCC"
    ADM = "ADM"

    role_choices = (
        (AUT, "Author"),
        (PCM, "Program committee member"),
        (PCC, "Program committee chair"),
        (ADM, "Administrator")
    )
    code = models.CharField(max_length=5, unique=True, db_index=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_role_choices(self):
        return dict(self.code).get(self.role_choices)


class User(models.Model):
    email = models.EmailField(db_index=True, unique=True,)
    first_name = models.CharField(max_length=50)
    middle_initial = models.CharField(max_length=1, blank=True)
    last_name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role)
    phone_number = models.CharField(max_length=12, help_text='Ex.: 555-555-5555')

    # string representation
    def __str__(self):
        return str(self.id) + ': ' + self.email
