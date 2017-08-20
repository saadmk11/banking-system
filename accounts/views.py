from django.shortcuts import render
from .forms import UserRegistrationForm
# Create your views here.

def register_view(request): # Creates a New Account & login New users
    title = "Register"
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password1")
        user.set_password(password)
        user.save()

    context = {"title":title, "form":form}

    return render(request, "accounts/form.html", context)