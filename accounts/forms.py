import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from .models import User, AccountDetails, UserAddress


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact_no",
            "password1",
            "password2"
        ]


class AccountDetailsForm(forms.ModelForm):

    class Meta:
        model = AccountDetails
        fields = [
            'gender',
            'birth_date',
            'picture'
        ]


class UserAddressForm(forms.ModelForm):

    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]


class UserLoginForm(forms.Form):
    account_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        account_no = self.cleaned_data.get("account_no")
        password = self.cleaned_data.get("password")

        if account_no and password:
            user = authenticate(account_no=account_no, password=password)
            if not user:
                raise forms.ValidationError("Account Does Not Exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not user.is_active:
                raise forms.ValidationError("Account is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)
