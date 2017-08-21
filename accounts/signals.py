from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import User


@receiver(pre_save, sender=User)
def create_account_no(sender, instance, *args, **kwargs):
    if not instance.account_no:
        largest = User.objects.all().aggregate(Max("account_no"))
        num = largest.get('account_no__max')

        if num != None:
            instance.account_no = num + 1
        else:
            instance.account_no = 10000000
