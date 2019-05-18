from api.models import Transfer

from api.transfer import TransferSerializer

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated


class TransferView(mixins.CreateModelMixin, mixins.UpdateModelMixin, generics.GenericAPIView):
    """
    Here we give the user the opportunity to request Transfers between two accounts.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

    def post(self, request, *args, **kwargs):
        request.data['sender'] = self.request.user.id
        return self.create(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
