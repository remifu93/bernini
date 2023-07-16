from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):
    email = models.EmailField('Email', unique=True)
    username = None
    first_name = models.CharField('Nombre', max_length=90)
    last_name = models.CharField('Apellido', max_length=90)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = UserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.email