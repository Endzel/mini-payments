from django.urls import re_path

from api.views.user import UserProfileView, LoginView, LogoutView
from api.views.account import AccountView, UserAccountView
from api.views.transfer import TransferView

api_urls = [
    re_path(r'^users$', UserProfileView.as_view(), name='userProfileView'),
    re_path(r'^login$', LoginView.as_view(), name='loginView'),
    re_path(r'^logout$', LogoutView.as_view(), name='logoutView'),

    re_path(r'^accounts$', AccountView.as_view(), name='accountView'),
    re_path(r'^accounts/(?P<pk>\d+)$', UserAccountView.as_view(), name='userAccountView'),

    re_path(r'^transfers$', TransferView.as_view(), name='transferView'),
]
