from django.db import models

class Reservation(models.Model):
    full_name = models.CharField(max_length=200)
    CIN = models.IntegerField()
    debut_reservation = models.DateField()
    fin_reservation = models.DateField()
    num_tel = models.IntegerField()
    montant = models.IntegerField()
