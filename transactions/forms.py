from django import forms

from .models import Deposit, Withdraw, Transaction


class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["amount"]


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ["amount"]

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'