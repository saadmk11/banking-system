import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget

from .models import User


class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(
      widget=SelectDateWidget(years=range(1940, 2010))
      )

    class Meta:
        model = User
        fields = ["full_name",
                  "gender",
                  "birth_date",
                  "email",
                  "contact_no",
                  "Address",
                  "city",
                  "country",
                  "nationality",
                  "occupation",
                  "picture",
                  "password1",
                  "password2"
                  ]

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    account_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        account_no = self.cleaned_data.get("account_no")
        password = self.cleaned_data.get("password")

        if account_no and password:
            user_obj = User.objects.filter(account_no=account_no).first()
            if user_obj:
                user = authenticate(email=user_obj.email, password=password)
                if not user:
                    raise forms.ValidationError("Account Does Not Exist.")
                if not user.check_password(password):
                    raise forms.ValidationError("Password Does not Match.")
                if not user.is_active:
                    raise forms.ValidationError("Account is not Active.")
            else:
                raise forms.ValidationError("Account Does Not Exist.")

        return super(UserLoginForm, self).clean(*args, **kwargs)
