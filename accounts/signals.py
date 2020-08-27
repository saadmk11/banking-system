from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserBankAccount


@receiver(post_save, sender=UserBankAccount)
def create_account_no(sender, instance, *args, **kwargs):
    # checks if user has an account number and user is not staff or superuser
    if not (
        instance.account_no and
        (instance.user.is_staff or instance.user.is_superuser)
    ):
        # gets the largest account number
        instance.account_no = (
            instance.user.id +
            settings.ACCOUNT_NUMBER_START_FROM
        )
        instance.save()
