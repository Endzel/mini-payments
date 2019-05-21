from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import UserProfile
from api.serializers.user import UserProfileSerializer


class UnsafeSessionAuthentication(SessionAuthentication):

    def authenticate(self, request):
        http_request = request._request
        user = getattr(http_request, 'user', None)

        if not user or not user.is_active:
            return None

        return (user, None)


class LoginView(APIView):
    """
    Gives the token to the requester after a successful login.
    """
    permission_classes = (AllowAny,)
    authentication_classes = (UnsafeSessionAuthentication,)

    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        if not user:
            return Response({"ERR": "Wrong credentials; Unauthorized access."}, status=401)
        login(request, user)
        update_last_login(sender=self, user=self.request.user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({"SUCCESS": "Successful login.", "token": token.key}, status=200)


class LogoutView(APIView):
    """
    Logs out user session.
    """
    permission_classes = (AllowAny,)
    authentication_classes = (UnsafeSessionAuthentication,)

    def get(self, request, *args, **kwargs):
        logout(request)
        return Response({"SUCCESS": "User logged out successfully."}, status=200)


class UserProfileView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Manage your current user through this view. Also, allow users to be registered.
    """

    permission_classes = (AllowAny,)
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        if self.request.method != "POST":
            if not self.request.user.is_authenticated:
                raise NotAuthenticated()
        return self.request.user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
