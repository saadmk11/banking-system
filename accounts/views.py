from django.contrib import messages
from django.contrib.auth import (authenticate,
                                 login,
                                 logout,
                                 )
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserLoginForm, UserRegistrationForm, AddressFrom
from .models import User, Address, Account


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
            entry = User.objects.get(id=request.user.id)
            account = Account(balance=0, user=entry)
            account.save()
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





def update_view(request):
    if request.method =='POST':
        form = AddressFrom(request.POST)
        if form.is_valid():

            street = request.POST.get("street", '')
            city = request.POST.get("city", '')
            district = request.POST.get("district", '')
            entry = User.objects.get(id=request.user.id)

            print("entry: ", entry.full_name)
            address = Address(street=street, city=city, district=district, user=entry)
            address.save()

            return redirect('home')

    else:
        form = AddressFrom()

    return render(request,"accounts/form.html", {'form': form, 'title': 'Updates'})


def delete_account(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        print("hello")
        user = User.objects.get(id = request.user.id)
        user.delete()
        messages.success(request, "The user is deleted")
        return redirect("home")

'''
def update_view(request):


    if request.method =='POST':
        form = AddressFrom(request.POST)
        if form.is_valid():
            address.street = request.POST.get("street")
            address.city = request.POST.get("city")
            address.district = request.POST.get("district")
            address = AddressFrom.save(commit=False)
            address.save()
            return redirect('home')

    else:
        form = AddressFrom()

    return render(request,"accounts/form.html", {'form': form})

'''
'''
def update_view(request):
    template_name = "accounts/form.html"

    def get(self, request):
        form = AddressFrom()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AddressFrom(request.POST)
        if form.is_valid():
            street = form.cleaned_data['street']
            city = form.cleaned_data['city']
            district = form.cleaned_data['district']
            form = AddressFrom()
            return redirect('home')

        context = {"form": form,
                   "street": street,
                   "city": city,
                   "district": district,
                   }
        return render(request, self.template_name, context)
'''
'''
def update_view(request):  # Creates a New Account & login New users
    if request.method == "POST":
        form = AddressFrom(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            print("KAYDETTI")
            messages.success(
                request,
                'Your Personal Informations has been updated Mr.{}.'.format("HELLO"))

            return redirect("home")
        return render(request, "accounts/form.html", {'form': form})
'''