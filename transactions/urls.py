from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView, TransferMoneyView, \
    SavingsTransactionRepostView, get_data

app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("savingsreport/", SavingsTransactionRepostView.as_view(), name="transaction_report_savings"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("transfer/", TransferMoneyView.as_view(), name="transfer_money"),
    path("report/data/", get_data, name="get_chart_data"),

]
