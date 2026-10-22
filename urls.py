from django.urls import include, re_path
from django.contrib import admin

from api.urls import api_urls

urlpatterns = [
    re_path(r'^api/', include(api_urls)),
    re_path(r'^admin/', admin.site.urls),
]
