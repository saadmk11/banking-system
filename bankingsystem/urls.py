from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from accounts.views import (login_view,
                            register_view,
                            logout_view,
                            delete_account,
                            update_view,
                            )

from core.views import home, about

urlpatterns = [
    # admin
    url(r'^admin/', admin.site.urls),
    # Accounts
    url(r'^login/$', login_view, name='login'),
    url(r'^register/$', register_view, name='register'),
    url(r'^logout/$', logout_view, name='logout'),
    # core
    url(r'^$', home, name='home'),
    url(r'^about/$', about, name='about'),
    # transactions
    url(r'^', include('transactions.urls', namespace='transactions')),
    url(r'^delete/$', delete_account, name='delete'),
    url(r'^detail/$', update_view, name='detail'),

]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
        )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
