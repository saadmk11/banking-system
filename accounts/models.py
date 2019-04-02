# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    RegexValidator,
    MinValueValidator,
    MaxValueValidator
)
from django.db import models
from django.urls import reverse

from .managers import UserManager
from django.conf import settings

NAME_REGEX = '^[a-zA-Z ]*$'

GENDER_CHOICE = (
    ("Male", "Male"),
    ("Female", "Female"),
)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None

    account_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ]
    )

    full_name = models.CharField(
        max_length=256,
        blank=False,
        validators=[
            RegexValidator(
                regex=NAME_REGEX,
                message='Name must be Alphabetic',
                code='invalid_full_name'
            )
        ]
    )

    gender = models.CharField(max_length=6, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'  # use email to log in
    REQUIRED_FIELDS = []  # required when user is created

    def __str__(self):
        return str(self.account_no)


class Address(models.Model):
    street = models.TextField()
    district = models.TextField()
    city = models.TextField()
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)


class Account(models.Model):
    balance = models.FloatField()
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
