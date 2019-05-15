from django.conf.urls import url

from api.views.user import UserProfileView

api_urls = [
    url(r'^users$', UserProfileView.as_view(), name='userProfileView'),
]
