# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.
NAME_REGEX = '^[a-zA-Z ]*$'
GENDER_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
    )


class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True, blank=True)
    account_no = models.PositiveIntegerField(unique=True, 
                                             validators=[MinValueValidator(10000000),
                                                         MaxValueValidator(99999999)
                                                         ]
                                            )
    full_name = models.CharField(max_length=256, blank=False,
                                  validators=[
                                        RegexValidator(
                                        regex = NAME_REGEX,
                                        message = 'Name must be Alphabetic',
                                        code='invalid_last_name'
                                        )]
                                )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True, null=True, blank=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    nationality = models.CharField(max_length=256)
    Occupation = models.CharField(max_length=256)
    picture = models.ImageField(null=True, 
                                blank=True, 
                                height_field="height_field", 
                                width_field="width_field",
                                )
    height_field = models.IntegerField(default=600, null=True)
    width_field = models.IntegerField(default=600, null=True)
    USERNAME_FIELD = 'account_no' # use email to log in
    REQUIRED_FIELDS = ['username', 'email'] # required when user is created

    def __str__(self):
        return str(self.account_no) 

    # def get_absolute_url(self):
    #     return reverse("user_profile", kwargs={"account_no": self.account_no})
    