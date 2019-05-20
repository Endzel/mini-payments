from api.models import Account

from api.serializers.account import AccountSerializer
from api.serializers.user import UserAccountSerializer

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AccountView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Here we give the user the opportunity to create its own Account, providing the serialized details.
    Also, we will return the details of the user's Account, if it exists.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        return Account.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        if Account.objects.filter(user=self.request.user).exists():
            return Response({"ERR": "This user already has an account."}, status=400)
        return self.create(request, *args, **kwargs)


class UserAccountView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    """
    In this view, giving a user ID, we will be able to retrieve its balance
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
