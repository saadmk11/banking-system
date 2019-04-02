from django.db.models import Sum
from django.shortcuts import render

from transactions.models import Deposit, Withdraw, Interest, Transaction
from accounts.models import User, Address, Account


def home(request):
    if not request.user.is_authenticated:
        return render(request, "core/home.html", {})
    else:
        try:
            user = request.user
            account = Account.objects.get(user_id=request.user.id)
            address = Address.objects.get(user_id=request.user.id)


            deposit = Deposit.objects.filter(user=user)
            deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
            withdraw = Withdraw.objects.filter(user=user)
            withdraw_sum = withdraw.aggregate(Sum('amount'))['amount__sum']
            interest = Interest.objects.filter(user=user)
            interest_sum = interest.aggregate(Sum('amount'))['amount__sum']
            transaction = Transaction.objects.filter(source_id=request.user.id)

            context = {
                        "user": user,
                        "address": address,
                        "account": account,
                        "deposit": deposit,
                        "deposit_sum": deposit_sum,
                        "withdraw": withdraw,
                        "withdraw_sum": withdraw_sum,
                        "interest": interest,
                        "interest_sum": interest_sum,
                        "transaction": transaction,
                      }

            return render(request, "core/transactions.html", context)
        except:
            print("HI")
            user = request.user
            account = Account.objects.get(user_id=request.user.id)
            deposit = Deposit.objects.filter(user=user)
            deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
            withdraw = Withdraw.objects.filter(user=user)
            withdraw_sum = withdraw.aggregate(Sum('amount'))['amount__sum']
            interest = Interest.objects.filter(user=user)
            interest_sum = interest.aggregate(Sum('amount'))['amount__sum']
            transaction = Transaction.objects.filter(source_id=request.user.id)
            print("trassfkajfjsahgjdsahkhgkdasg: ", transaction)

            context = {
                        "user": user,
                        "account": account,
                        "deposit": deposit,
                        "deposit_sum": deposit_sum,
                        "withdraw": withdraw,
                        "withdraw_sum": withdraw_sum,
                        "interest": interest,
                        "interest_sum": interest_sum,
                      }

            return render(request, "core/transactions.html", context)

def about(request):
    return render(request, "core/about.html", {})
