from django import forms

from .models import Diposit, Withdrawal


class DepositForm(forms.ModelForm):
    class Meta:
        model = Diposit
        fields = ["amount"]


class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount"]
