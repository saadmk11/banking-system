from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawalForm
# Create your views here.
def diposit_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = DepositForm(request.POST or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.user.balance += deposit.amount
            deposit.user.save()
            deposit.save()
            return redirect("/")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)


def withdrawal_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdrawal"
        form = WithdrawalForm(request.POST or None)

        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            if withdrawal.user.balance >= withdrawal.amount:
                withdrawal.user.balance -= withdrawal.amount
                withdrawal.user.save()
                withdrawal.save()
                return redirect("/")
            else:
                raise Http404

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)