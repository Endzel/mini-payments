from django.conf.urls import url

from api.views.user import UserProfileView, LoginView, LogoutView
from api.views.account import AccountView

api_urls = [
    url(r'^users$', UserProfileView.as_view(), name='userProfileView'),
    url(r'^login$', LoginView.as_view(), name='loginView'),
    url(r'^logout$', LogoutView.as_view(), name='logoutView'),
    url(r'^accounts$', AccountView.as_view(), name='userAccountView'),
]
