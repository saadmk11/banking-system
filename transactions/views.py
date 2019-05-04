from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawalForm


@login_required()
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        messages.success(
            request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
        )
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)
