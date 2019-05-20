from django.conf.urls import url

from api.views.user import UserProfileView, LoginView, LogoutView
from api.views.account import AccountView, UserAccountView
from api.views.transfer import TransferView

api_urls = [
    url(r'^users$', UserProfileView.as_view(), name='userProfileView'),
    url(r'^login$', LoginView.as_view(), name='loginView'),
    url(r'^logout$', LogoutView.as_view(), name='logoutView'),

    url(r'^accounts$', AccountView.as_view(), name='accountView'),
    url(r'^accounts/(?P<pk>\d+)$', UserAccountView.as_view(), name='userAccountView'),

    url(r'^transfers$', TransferView.as_view(), name='transferView'),
]
