from django.contrib.auth.models import User
from django.db import models


class Mecanicien(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    specialite = models.CharField(max_length=100)
    disponibilite = models.TextField()

    def __str__(self):
        return f"ID: {self.id}, Username: {self.user.username} - Mécanicien"


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    mecanicien = models.ForeignKey(Mecanicien, on_delete=models.SET_NULL, null=True, blank=True, related_name="clients")

    def __str__(self):
        return f"ID: {self.id}, Username: {self.user.username} - Client"
