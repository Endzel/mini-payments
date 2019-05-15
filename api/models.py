from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

import uuid


class CustomUserManager(BaseUserManager):
    """
    A custom user manager will be necessary in order to create a custom
    implementation of the User model.
    """
    def create(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You must set an email in order to create an user')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(blank=True, max_length=140, verbose_name='First name')
    last_name = models.CharField(blank=True, max_length=140, verbose_name='Last name')
    phone_number = PhoneNumberField(verbose_name='Mobile phone', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'User'

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return self.email


class Account(models.Model):

    id = models.CharField(max_length=255, default=uuid.uuid4, primary_key=True, verbose_name='Account ID')
    balance = models.DecimalField(max_digits=19, null=True, blank=True, decimal_places=2, verbose_name='Total balance')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='Start time')
    is_active = models.BooleanField(default=True)

    # Relations
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='user_accounts', verbose_name='UserProfile')

    def __str__(self):
        return self.original_title
