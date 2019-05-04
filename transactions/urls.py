from django.conf.urls import url

from .views import deposit_view, withdrawal_view

urlpatterns = [
    # url(r'^$', home_view, name='home'),
    url(r'^deposit/$', deposit_view, name='deposit'),
    url(r'^withdrawal/$', withdrawal_view, name='withdrawal'),
]
