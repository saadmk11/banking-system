from __future__ import absolute_import, unicode_literals
from celery.decorators import task

from accounts.models import User
from .models import Interest


@task(name="count_interest")
def count():
    users = User.objects.all()

    if users:
        for user in users:
            balance = user.balance
            # calculates users interest
            amount = (balance * 10) / 100
            interest = Interest.objects.create(user=user, amount=amount)
            # adds users interest to balance.
            user.balance += amount
            user.save()
