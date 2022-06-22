# authentication/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    PERSONNEL = 'PERSONNEL'
    SECRETARIAT = 'SECRETARIAT'
    ADMINISTRATION = 'ADMINISTRATION'
    ROLE_CHOICES = (

        (PERSONNEL, 'PERSONNEL'),
        (SECRETARIAT, 'SECRETARIAT'),
        (ADMINISTRATION, 'ADMINISTRATION'),
    )
    profile_photo = models.ImageField(
        verbose_name='Photo de profil',blank=True)
    role = models.CharField(
        max_length=30, choices=ROLE_CHOICES, verbose_name='Rôle')

