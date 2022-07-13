from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    The User model
    """
    username = models.CharField(max_length=55, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
