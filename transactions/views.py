from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import DepositForm, WithdrawForm, TransactionForm
from accounts.models import Account, User
from django.shortcuts import get_object_or_404

@login_required()
def transaction_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Transaction"
        form = TransactionForm(request.POST or None)
        if form.is_valid():
            transaction = form.save(commit=False)
            print("id : ", request.user.id)
            dest_id = form.cleaned_data.get("dest")
            print("dest_id", dest_id)
            source_account = get_object_or_404(Account, user_id=request.user.id)
            dest_account = get_object_or_404(Account, user_id=dest_id)


            # adds users deposit to balance.
            source_account.balance -= transaction.amount
            dest_account.balance += transaction.amount
            transaction.save()
            source_account.save()
            dest_account.save()
            messages.success(request, 'You Have Transacted {}$.'
                             .format(transaction.amount))
            return redirect("home")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)


@login_required()
def deposit_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Deposit"
        form = DepositForm(request.POST or None)

        if form.is_valid():
            deposit = form.save(commit=False)
            print("id : ", request.user.id)
            account = get_object_or_404(Account, user_id=request.user.id)
            print("---------------->", account.user_id)

            deposit.user = request.user
            # adds users deposit to balance.
            account.balance += deposit.amount
            account.save()
            deposit.save()
            messages.success(request, 'You Have Deposited {} $.'
                             .format(account.balance))
            return redirect("home")

        context = {
                    "title": title,
                    "form": form
                  }
        return render(request, "transactions/form.html", context)

@login_required()
def withdraw_view(request):
    if not request.user.is_authenticated:
        raise Http404
    else:
        title = "Withdraw"
        form = WithdrawForm(request.POST or None)

        if form.is_valid():
            withdraw = form.save(commit=False)
            withdraw.user = request.user
            account = get_object_or_404(Account, user_id=request.user.id)


            # checks if user is tring Withdraw more than his balance.
            if account.balance >= withdraw.amount:
                # substracts users withdrawal from balance
                account.balance -= withdraw.amount
                withdraw.user.save()
                withdraw.save()
                account.save()
                messages.error(request, 'You Have Withdrawn {} $.'
                               .format(withdraw.amount))
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


