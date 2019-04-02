from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from accounts.models import User
# Create your models here.
User = settings.AUTH_USER_MODEL


class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Interest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(
      decimal_places=2,
      max_digits=12,
      validators=[
          MinValueValidator(Decimal('10.00'))
          ]
      )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Transaction(models.Model):
    source = models.ForeignKey(User, null=True, related_name='source')
    dest   = models.ForeignKey(User, null=True, related_name='dest')
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
