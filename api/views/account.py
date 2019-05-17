from api.models import Account

from api.serializers import AccountSerializer

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AccountView(mixins.CreateModelMixin, generics.GenericAPIView):
    """
    Here we give the user the opportunity to create its own Account, providing the serialized details.
    Also, we will return the details of the user's Account, if it exists.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return {}
        return AccountSerializer

    def get_object(self):
        return Account.objects.get(user=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['user'] = self.request.user.id
        if Account.objects.filter(user=self.request.user).exists():
            return Response({"ERR": "This user already has an account."}, status=400)
        return self.create(request, *args, **kwargs)


class UserAccountView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Account.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PATCH':
            return AccountSerializer
        return AccountSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
