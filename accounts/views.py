from django.contrib import messages
from django.contrib.auth import (authenticate,
                                 login,
                                 logout
                                 )
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegistrationForm
from .models import User


def register_view(request):  # Creates a New Account & login New users
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Create a Bank Account"
        form = UserRegistrationForm(
            request.POST or None,
            request.FILES or None
            )

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            new_user = authenticate(email=user.email, password=password)
            login(request, new_user)
            messages.success(
                request,
                '''Thank You For Creating A Bank Account {}.
                Your Account Number is {}, Please use this number to login
                '''.format(new_user.full_name, new_user.account_no))

            return redirect("home")

        context = {"title": title, "form": form}

        return render(request, "accounts/form.html", context)


def login_view(request):  # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect("home")
    else:
        title = "Load Account Details"
        form = UserLoginForm(request.POST or None)

        if form.is_valid():
            account_no = form.cleaned_data.get("account_no")
            user_obj = User.objects.filter(account_no=account_no).first()
            password = form.cleaned_data.get("password")
            # authenticates Email & Password
            user = authenticate(email=user_obj.email, password=password)
            login(request, user)
            messages.success(request, 'Welcome, {}!' .format(user.full_name))
            return redirect("home")

        context = {"form": form,
                   "title": title
                   }

        return render(request, "accounts/form.html", context)


def logout_view(request):  # logs out the logged in users
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        logout(request)
        return redirect("home")
