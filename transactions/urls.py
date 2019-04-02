from django.conf.urls import url

from .views import deposit_view, withdraw_view, transaction_view

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    url(r'^deposit/$', deposit_view, name='deposit'),
    url(r'^withdraw/$', withdraw_view, name='withdraw'),
    url(r'^transaction/$', transaction_view, name='transaction'),

]
