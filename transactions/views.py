from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawalForm


@login_required()
def diposit_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = DepositForm(request.POST or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # adds users deposit to balance.
            deposit.user.balance += deposit.amount
            deposit.user.save()
            deposit.save()
            messages.success(request, 'You Have Deposited {} $.'
                             .format(deposit.amount))
            return redirect("home")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)


@login_required()
def withdrawal_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdraw"
        form = WithdrawalForm(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user

            # checks if user is tring Withdraw more than his balance.
            if withdrawal.user.balance >= withdrawal.amount:
                # substracts users withdrawal from balance
                withdrawal.user.balance -= withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                messages.error(request, 'You Have Withdrawn {} $.'
                               .format(withdrawal.amount))
                return redirect("home")

            else:
                messages.error(
                    request,
                    'You Can Not Withdraw More Than You Balance.'
                    )

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)
