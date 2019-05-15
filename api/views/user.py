from django.contrib.auth.models import update_last_login

from rest_framework import generics, mixins
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from api.models import UserProfile
from api.serializers import UserProfileSerializer


class UserProfileView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    Manage your current user through this view.
    """

    permission_classes = (IsAuthenticated,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        if not self.request.user.is_authenticated():
            raise NotAuthenticated()
        update_last_login(sender=self, user=self.request.user)
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
