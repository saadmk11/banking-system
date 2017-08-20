import datetime
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms.extras.widgets import SelectDateWidget
from .models import User

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=SelectDateWidget(years=range(1940, 2010)))
    class Meta:
        model = User
        fields = ("full_name",
                  "gender", 
                  "birth_date", 
                  "email", 
                  "contact_no", 
                  "Address", 
                  "city", 
                  "country", 
                  "nationality", 
                  "Occupation", 
                  "picture",
                  "password1", 
                  "password2" )

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user