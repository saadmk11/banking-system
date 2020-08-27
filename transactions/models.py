from django.contrib.auth import get_user_model
from django.db import models

from .constants import TRANSACTION_TYPE_CHOICES


User = get_user_model()


class Transaction(models.Model):
    user = models.ForeignKey(
        User,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
