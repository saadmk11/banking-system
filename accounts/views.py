from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
import requests
from .forms import UserRegistrationForm, UserAddressForm

User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:transaction_report')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST)
        address_form = UserAddressForm(self.request.POST)

        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
            address = address_form.save(commit=False)
            address.user = user
            address.save()
            url = 'https://otp-tp.herokuapp.com/api/v1/user'
            payload = {"email": user.email}
            requests.post(url, json=payload)
            login(self.request, user)
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.account.account_no}. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_validation')
            )

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
                address_form=address_form
            )
        )

    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    redirect_authenticated_user = True

    def post(self, request, *args, **kwargs):
        request.session["email"] = request.POST["username"]
        email = request.session["email"]
        send_otp(email)
        return HttpResponseRedirect(
            reverse_lazy('accounts:user_validation')
        )


class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserValidationView(TemplateView):
    template_name = 'accounts/user_otp.html'

    def get(self, request, *args, **kwargs):

        if not request.session["email"]:
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
            )
        if not User.objects.get(email=request.session["email"]).is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
            )

        return render(request, 'accounts/user_otp.html')

    def post(self, request, *args, **kwargs):
        otp = request.POST["otp"]
        if len(otp) < 6:
            messages.error(
                self.request,
                (
                    f'Wrong OTP - length. '
                )
            )
            return render(request, 'accounts/user_otp.html')

        url = 'https://otp-tp.herokuapp.com/api/v1/user/otp/validate/' + request.session["email"] + "?otp=" + otp
        r = requests.get(url)
        if r.status_code == 401:
            messages.error(
                self.request,
                (
                    f'Wrong OTP. '
                )
            )
            return render(request, 'accounts/user_otp.html')

        login(self.request, User.objects.get(email=request.session["email"]))
        return HttpResponseRedirect(

            reverse_lazy('transactions:deposit_money')

        )

def send_otp(email):
    url = 'https://otp-tp.herokuapp.com/api/v1/user/otp/generate/' + email
    requests.get(url)