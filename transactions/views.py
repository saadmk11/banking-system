from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.http import JsonResponse
from django.utils.safestring import SafeString

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from itertools import chain
from django.shortcuts import HttpResponseRedirect, render
import pandas as pd
from datetime import datetime, timedelta
from django.utils.timezone import make_aware

from transactions.constants import DEPOSIT, WITHDRAWAL, TRANSFER
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
    TransferForm
)
from transactions.models import Transaction, SavingTransaction
from accounts.models import UserBankAccount


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def __init__(self):
        super().__init__()
        self.account_id = None

    def get(self, request, *args, **kwargs):
        if request.GET.get("account_id"):
            form = TransactionDateRangeForm(request.GET or None)
            account = UserBankAccount.objects.get(account_no=request.GET.get("account_id"))
            accounts = UserBankAccount.objects.filter(user_id=self.request.user.id)

            if account.user.id == self.request.user.id:
                self.account_id = request.GET.get("account_id")
                if form.is_valid():
                    self.form_data = form.cleaned_data
                daterange = self.form_data.get("daterange")
                if request.GET.get("transactions"):
                    if daterange:
                        transactions = Transaction.objects.filter(account_id=account.id,
                                                                  timestamp__date__range=daterange)
                    else:
                        transactions = Transaction.objects.filter(account_id=account.id)
                else:
                    if daterange:
                        transactions = Transaction.objects.filter(account_id=account.id,
                                                                  timestamp__date__range=daterange)[:10]
                    else:
                        transactions = Transaction.objects.filter(account_id=account.id)[:10]

                context = self.get_context_data(object_list=transactions)
                context['account_balance'] = account.balance
                context['account_no'] = account.account_no
                context['account_type'] = account.account_type
                context['accounts'] = accounts
                for account in accounts:
                    if account.account_type.is_saving_account:
                        context["saving_goal"]= account.saving_goal
                        context["interest_rate"] = account.account_type.annual_interest_rate
                        context['saving_goal_fulfilment'] = account.balance/account.saving_goal*100
                return render(request, self.template_name, context=context)
            else:
                return HttpResponseRedirect("/accounts/dashboard/")

        else:
            print("fgergre")
            return HttpResponseRedirect("/accounts/dashboard/")


class SavingsTransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report_savings.html'
    model = SavingTransaction
    form_data = {}

    def __init__(self):
        super().__init__()
        self.account_id = None

    def get(self, request, *args, **kwargs):
        if request.GET.get("account_id"):
            form = TransactionDateRangeForm(request.GET or None)
            account = UserBankAccount.objects.get(account_no=request.GET.get("account_id"))
            if account.user.id == self.request.user.id:
                self.account_id = request.GET.get("account_id")
                if form.is_valid():
                    self.form_data = form.cleaned_data
                transactions = self.get_queryset()
                context = self.get_context_data(object_list=transactions)
                context['account_balance'] = account.balance
                return render(request, self.template_name, context=context)
            else:
                return HttpResponseRedirect("/accounts/dashboard/")

        else:
            return HttpResponseRedirect("/accounts/dashboard/")

    def get_queryset(self):
        account = UserBankAccount.objects.get(account_no=self.account_id)
        queryset_to = super().get_queryset().filter(
            account=account
        )

        queryset = queryset_to

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': UserBankAccount.objects.get(account_no=self.account_id),
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.accounts.first()
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit Money to Your Account'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.accounts.first()

        if not account.initial_deposit_date:
            now = timezone.now()
            if account.account_type.interest_calculation_per_year != 0:
                next_interest_month = int(
                    12 / account.account_type.interest_calculation_per_year
                )
            else:
                next_interest_month = 0
            account.initial_deposit_date = now
            account.interest_start_date = (
                    now + relativedelta(
                months=+next_interest_month
            )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            f'{amount}$ was deposited to your account successfully'
        )

        form.account = account
        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.accounts.first()

        account.balance -= form.cleaned_data.get('amount')
        account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {amount}$ from your account'
        )

        form.account = account
        form.cleaned_data['amount'] = -form.cleaned_data['amount']
        return super().form_valid(form)


class TransferMoneyView(CreateView):
    template_name = 'transactions/transaction_transfer.html'
    form_class = TransferForm
    form_data = {}

    def get(self, request, *args, **kwargs):
        if request.GET.get("account_id"):
            return render(request, self.template_name, {'form': self.form_class})
        return HttpResponseRedirect("/accounts/dashboard/")

    def post(self, request, *args, **kwargs):
        form = TransferForm(request.POST)
        account_id = request.GET.get("account_id")
        account = UserBankAccount.objects.filter(account_no=account_id).first()
        if account:
            if form.is_valid():

                user_to = form.cleaned_data.get("account_to")
                if user_to:
                    amount = form.cleaned_data.get('amount')
                    if account.balance >= amount:
                        account.balance -= amount
                        account.save(update_fields=['balance'])
                        user_to = UserBankAccount.objects.get(account_no=user_to.account_no)
                        user_to.balance += amount
                        user_to.save(update_fields=['balance'])
                        user_from = UserBankAccount.objects.get(account_no=account_id)

                        transaction = Transaction(amount=-form.cleaned_data.get('amount'),
                                                  balance_after_transaction=user_from.balance,
                                                  transaction_type=TRANSFER, account=user_from,
                                                  account_to=user_to
                                                  )

                        transaction_to = Transaction(amount=form.cleaned_data.get('amount'),
                                                     balance_after_transaction=user_to.balance,
                                                     transaction_type=TRANSFER, account=user_to,
                                                     account_to=user_from
                                                     )
                        transaction.save()
                        transaction_to.save()
                        messages.success(
                            self.request,
                            f'Sent {amount} to {user_to.account_no}'
                        )
                    else:
                        messages.error(
                            self.request,
                            f'Not enough money'
                        )
                else:
                    messages.error(
                        self.request,
                        f'User doesnt exist'
                    )
            else:
                messages.error(
                    self.request,
                    f'Account isnt belonging to user'
                )
        return render(request, self.template_name, {'form': self.form_class})


def get_data(request):
    account = UserBankAccount.objects.get(account_no=request.GET.get("account_id"))
    print("su5")
    MONTHS = {
        0: "Jan",
        1: "Feb",
        2: "Mar",
        3: "Apr",
        4: "May",
        5: "June",
        6: "July",
        7: "Aug",
        8: "Sep",
        9: "Oct",
        10: "Nov",
        11: "Dec",

    }
    if account:
        startdate = make_aware(datetime.today())
        enddate = startdate - timedelta(days=110)

        transactions = Transaction.objects.filter(account_id=account.id, timestamp__range=(enddate, startdate))
        df = pd.DataFrame(transactions.values())
        df = df.groupby([df['timestamp'].dt.month]).agg(monthly_amount=('amount', 'sum'),
                                                        negative=('amount', lambda x: x[x < 0].sum()),
                                                        positive=('amount', lambda x: x[x > 0].sum()))

        indexes = df.index.values.tolist()
        indexes.reverse()
        print(indexes)
        months = []
        for i in range(indexes[0], indexes[0] - 5, -1):
            if i not in indexes:
                new_row = pd.DataFrame({'monthly_amount': 0, 'negative': 0, 'positive': 0},
                                       index=[i])
                df = pd.concat([new_row, df.loc[:]])
            print((indexes[0] - i) % 12)
            months.append(MONTHS[(indexes[0] - i - 1) % 12])
        df = df.sort_index()
        print(df)
        chart_data = {"negative_transactions": [-x for x in df['negative'].tolist()],
                      "positive_transactions": [x for x in df['positive'].tolist()],
                      "monthly_amount": [x for x in df['monthly_amount'].tolist()],
                      "labels": months}

        return JsonResponse(chart_data, safe=False)
