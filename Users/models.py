from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from Users.manager import UserManager
from .validators import length_validator


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, blank=False, )
    OTP = models.IntegerField(validators=(length_validator,), null=True, blank=True, verbose_name='One Time Passcode')
    OTP_creation_time = models.DateTimeField(default=None, blank=True, null=True,
                                             verbose_name='One Time Passcode Creation Time')
    is_logged_in = models.BooleanField(default=False,)
    is_staff = models.BooleanField(_('staff status'),
                                   default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'),
                                   )
    is_active = models.BooleanField(_('active'), default=False, help_text=_(
        'Designates whether this user should be ''treated as active. Unselect this instead ''of deleting accounts.'), )
    date_joined = models.DateTimeField(_('date joined'),
                                       default=timezone.now, )
    objects = UserManager()
    USERNAME_FIELD = 'email'

