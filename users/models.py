from django.db import models

# Create your models here.
class Afiliado(models.Model):
    # we need the document number and if it has okay its seguridad social
    # all the properties it has
    document_number = models.IntegerField()
    # state could be one of three
    # G: Good
    # P: In process
    # B: Bad
    GOOD = 'G'
    BAD = 'B'
    PROCESS = 'P'
    ls_posibilities = [(GOOD, "Good"),
                        (PROCESS, "Process"),
                        (BAD, "Bad"),]
        # First validation
    first_val = models.CharField(
        max_length=2,
        choices=ls_posibilities,
        default=PROCESS
    )
    # Second validation
    second_val = models.CharField(
        max_length=2,
        choices=ls_posibilities,
        default=PROCESS
    )

    third_val = models.CharField(
        max_length=2,
        choices=ls_posibilities,
        default=PROCESS
    )
    # Third validation
    state = models.CharField(
        max_length=2,
        choices=ls_posibilities,
        default=PROCESS
    )

    # Date in which it was uploaded
    date_upload = models.DateField(auto_now=True)
    # Range of period 6-2021
    # period = models.CharField(max_length=8, default="6-2021")

    def __str__(self):
        return f"{self.document_number}: {self.state}, Date: {self.date_upload}"


class Period(models.Model):

    person = models.ForeignKey(Afiliado, on_delete=models.CASCADE)
    period = models.CharField(max_length=8, default="6-2021")
        

    def __str__(self):
        return f"{self.period}: {self.person}"