import datetime

from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView
import requests
import random
from banking_system.settings import ACCOUNT_NUMBER_START_FROM
from transactions.constants import DEPOSITTSA, WITHDRAWALFSA
from transactions.models import Transaction, SavingTransaction
from .forms import UserRegistrationForm, UserAddressForm
from .models import User
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SavingAccountForm
from .models import UserBankAccount, BankAccountType

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
            messages.success(
                self.request,
                (
                    f'Thank You For Creating A Bank Account. '
                    f'Your Account Number is {user.accounts.first().account_no}. '
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


class UserRegistrationSavingAccountView(View):
    template_name = 'accounts/create_saving_account.html'
    form_class = SavingAccountForm

    def get(self, request, account_id):
        user = request.user
        account = UserBankAccount.objects.get(user_id=user.id)
        account_type = BankAccountType.objects.get(is_saving_account=True)

        initial_data = {
            'user': account.user,
            'account_type': account_type,
            'account_no': account.account_no,
            'gender': account.gender,
            'birth_date': account.birth_date,
            'balance': 0,
            'interest_start_date': account.interest_start_date,
            'initial_deposit_date': account.initial_deposit_date
        }

        form = self.form_class(initial=initial_data)

        return render(request, self.template_name, {'form': form})

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            request.session["email"] = request.POST["username"]
            email = request.session["email"]
            send_otp(email)
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_validation')
            )
        else:
            messages.error(
                self.request,
                (
                    f'Wrong credentials. '
                )
            )
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
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

        if not request.session.get("email"):
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
            )
        if not User.objects.get(email=request.session["email"]).is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('accounts:user_login')
            )

        return render(request, 'accounts/user_otp.html')

    def post(self, request, *args, **kwargs):
        otp = request.POST.get("otp", 0)
        if otp == 0:
            email = request.session["email"]
            send_otp(email)
            return render(request, 'accounts/user_otp.html')

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


class UserAccountView(TemplateView):
    template_name = 'transactions/transaction_report.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(email=request.session["email"])
        accounts = UserBankAccount.objects.filter(user_id=user.id, account_type__name="Checking").first()
        return HttpResponseRedirect("/transactions/report/?account_id=" + str(accounts.account_no))


def send_otp(email):
    url = 'https://otp-tp.herokuapp.com/api/v1/user/otp/generate/' + email
    print(url)
    response = requests.get(url)
    print(response)


class UserSavingAccountView(TemplateView):
    template_name = 'transactions/transaction_savings.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['balance'] = self.request.user.account.balance
    #     context["interest_rate"] = self.request.user.account.account_type.annual_interest_rate
    #     return context

    def get(self, request, *args, **kwargs):
        accountDebet = self.request.user.accounts.first()
        accountSaving = self.request.user.accounts.filter(account_type__is_saving_account=True).first()
        if (accountSaving == None):
            savings_view = UserRegistrationSavingAccountView.as_view()
            return savings_view(request, account_id=request.GET.get("account_id"))
        balance = accountDebet.balance
        savings_balance = accountSaving.balance
        interest_rate = accountSaving.account_type.annual_interest_rate
        context = {
            'account_no': accountSaving.account_no,
            'balance': balance,
            'savings_balance': savings_balance,
            'interest_rate': interest_rate,
        }
        return render(request, 'transactions/transaction_savings.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user

        if UserBankAccount.objects.filter(user_id=user.id, account_type__is_saving_account=True).exists() is not True:
            form = SavingAccountForm(request.POST)
            if form.is_valid():
                # Save the new saving account
                saving_account = form.save(commit=False)
                saving_account.interest_start_date = datetime.datetime.now()
                saving_account.account_no = ACCOUNT_NUMBER_START_FROM + (
                            random.randint(1, 1000) * random.randint(1, 1000))
                saving_account.user = self.request.user
                saving_account.save()

                return HttpResponseRedirect("/accounts/dashboard/")

            else:
                # If the request method is not POST, display the form
                form = SavingAccountForm()

            return render(request, 'accounts/create_saving_account.html', {'form': form})

        ###
        accountDebet = self.request.user.accounts.first()
        accountSaving = self.request.user.accounts.filter(account_type__is_saving_account=True).first()
        if 'depositToSavingAcc' in request.POST:
            amount = int(request.POST.get('depositToSavingAcc'))

            # if not account.initial_deposit_date:
            #     now = timezone.now()
            #     if account.account_type.interest_calculation_per_year != 0:
            #         next_interest_month = int(
            #             12 / account.account_type.interest_calculation_per_year
            #         )
            #     else:
            #         next_interest_month = 0
            #     account.initial_deposit_date = now
            #     account.interest_start_date = (
            #             now + relativedelta(
            #         months=+next_interest_month
            #     )
            #     )

            if amount <= 0:
                messages.error(request, "Invalid operation.")
            elif accountDebet.balance >= amount:
                accountDebet.balance -= amount
                accountSaving.balance += amount
                accountDebet.save(
                    update_fields=[
                        'balance'
                    ]
                )
                accountSaving.save(
                    update_fields=[
                        'balance'
                    ]
                )

                messages.success(
                    self.request,
                    f'{amount}$ was deposited to your saving account from debet account successfully'
                )

                created_transactions = []
                created_transactionsSavings = []
                transaction_obj = Transaction(
                    account=accountDebet,
                    transaction_type=DEPOSITTSA,
                    amount=-amount,
                    balance_after_transaction=accountDebet.balance
                )
                transaction_objSavings = Transaction(
                    account=accountSaving,
                    transaction_type=DEPOSITTSA,
                    amount=amount,
                    balance_after_transaction=accountSaving.balance
                )
                created_transactions.append(transaction_obj)
                created_transactionsSavings.append(transaction_objSavings)
                if created_transactions:
                    Transaction.objects.bulk_create(created_transactions)
                    SavingTransaction.objects.bulk_create(created_transactionsSavings)

            else:
                messages.error(request, "Not enough money on debet account!")

            balance = accountDebet.balance
            savings_balance = accountSaving.balance
            interest_rate = accountSaving.account_type.annual_interest_rate
            context = {
                'account_no': accountDebet.account_no,
                'balance': balance,
                'savings_balance': savings_balance,
                'interest_rate': interest_rate,
            }

            return render(request, 'transactions/transaction_savings.html', context)
        elif 'withdrawFromSavingAccount' in request.POST:
            amount = int(request.POST.get('withdrawFromSavingAccount'))

            if amount <= 0:
                messages.error(request, "Invalid operation.")
            elif accountSaving.balance >= amount:
                accountSaving.balance -= amount
                accountDebet.balance += amount
                accountDebet.save(
                    update_fields=[
                        'balance'
                    ]
                )
                accountSaving.save(
                    update_fields=[
                        'balance'
                    ]
                )

                messages.success(
                    self.request,
                    f'{amount}$ was deposited to your debet account from saving account successfully'
                )

                created_transactions = []
                created_transactionsSavings = []
                transaction_obj = Transaction(
                    account=accountDebet,
                    transaction_type=WITHDRAWALFSA,
                    amount=amount,
                    balance_after_transaction=accountDebet.balance
                )
                transaction_objSavings = Transaction(
                    account=accountSaving,
                    transaction_type=WITHDRAWALFSA,
                    amount=-amount,
                    balance_after_transaction=accountSaving.balance
                )
                created_transactions.append(transaction_obj)
                created_transactionsSavings.append(transaction_objSavings)
                if created_transactions:
                    Transaction.objects.bulk_create(created_transactions)
                    SavingTransaction.objects.bulk_create(created_transactionsSavings)

            else:
                messages.error(request, "Not enough money on your saving account!")

            balance = accountDebet.balance
            savings_balance = accountSaving.balance
            interest_rate = accountSaving.account_type.annual_interest_rate
            context = {
                'account_no': accountSaving.account_no,
                'balance': balance,
                'savings_balance': savings_balance,
                'interest_rate': interest_rate,
            }
            return render(request, 'transactions/transaction_savings.html', context)
        else:
            messages.error(request, "Invalid operation.")
            balance = accountDebet.balance
            savings_balance = accountSaving.balance
            interest_rate = accountSaving.account_type.annual_interest_rate
            context = {
                'account_no': accountSaving.account_no,
                'balance': balance,
                'savings_balance': savings_balance,
                'interest_rate': interest_rate,
            }
            return render(request, 'transactions/transaction_savings.html', context)
