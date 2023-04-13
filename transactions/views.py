from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from itertools import chain
from django.shortcuts import HttpResponseRedirect, render

from transactions.constants import DEPOSIT, WITHDRAWAL, TRANSFER
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
    TransferForm
)
from transactions.models import Transaction
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
            if account.user.id == self.request.user.id:
                self.account_id = request.GET.get("account_id")
                if form.is_valid():
                    self.form_data = form.cleaned_data
                return super().get(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/accounts/accounts/")

        else:
            return HttpResponseRedirect("/accounts/accounts/")

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
            'account': self.request.user.account
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
        account = self.request.user.account

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

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Withdraw Money from Your Account'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')

        self.request.user.account.balance -= form.cleaned_data.get('amount')
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {amount}$ from your account'
        )

        return super().form_valid(form)


class TransferMoneyView(CreateView):
    template_name = 'transactions/transaction_transfer.html'
    form_class = TransferForm
    form_data = {}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = TransferForm(request.POST)
        if form.is_valid():

            user_to = form.cleaned_data.get("account_to")
            if user_to:
                amount = form.cleaned_data.get('amount')
                if self.request.user.account.balance >= amount:
                    self.request.user.account.balance -= amount
                    self.request.user.account.save(update_fields=['balance'])
                    user_to = UserBankAccount.objects.get(account_no=user_to.account_no)
                    user_to.balance += amount
                    user_to.save(update_fields=['balance'])
                    user_from = UserBankAccount.objects.get(account_no=request.user.account.account_no)

                    transaction = Transaction(amount=-form.cleaned_data.get('amount'),
                                              balance_after_transaction=user_from.balance,
                                              transaction_type=TRANSFER, account=self.request.user.account,
                                              account_to=user_to
                                              )

                    transaction_to = Transaction(amount=form.cleaned_data.get('amount'),
                                                 balance_after_transaction=user_to.balance,
                                                 transaction_type=TRANSFER, account=user_to,
                                                 account_to=self.request.user.account
                                                 )
                    transaction_to.save()
                    transaction.save()
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
        return render(request, self.template_name, {'form': self.form_class})
