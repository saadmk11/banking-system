from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]


class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all()
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')

            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                account_type=account_type,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user
