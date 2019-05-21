from decimal import Decimal

from django.db import transaction
from django.db.models import Q

from api.models import Transfer, UserProfile
from api.serializers.transfer import TransferSerializer, FullTransferSerializer

from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class TransferView(mixins.ListModelMixin, generics.GenericAPIView):
    """
    Here we give the user the opportunity to complete Transfers between his account and other accounts.
    Also, to check his or her transactions history.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = TransferSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return TransferSerializer
        return FullTransferSerializer

    def get_queryset(self):
        return Transfer.objects.filter(Q(receiver=self.request.user.user_account) | Q(sender=self.request.user.user_account)).order_by('-timestamp')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'amount' not in request.data:
            return Response({"Error": "You must specify an amount to transfer."}, status=400)
        amount = Decimal(request.data['amount'])
        concept = request.data['concept']
        receiver = UserProfile.objects.filter(pk=request.data['receiver'])
        if not receiver:
            return Response({"Error": "Specified receiver does not exist."}, status=404)
        receiver_account = receiver.first().user_account
        sender_account = self.request.user.user_account
        if Decimal(sender_account.balance) - amount < 0:
            return Response({"Error": "You do not have enough funds; Please recharge your account before retrying this operation."}, status=400)
        if amount < 0:
            return Response({"Error": "You must try with a positive amount of money."}, status=400)
        if not sender_account.is_active or not receiver_account.is_active:
            return Response({"Error": "At least one of the accounts you tried to operate with is inactive."}, status=401)
        with transaction.atomic():
            sender_account.balance = Decimal(sender_account.balance) - amount
            sender_account.save()
            receiver_account.balance = Decimal(receiver_account.balance) + amount
            receiver_account.save()
            Transfer.objects.create(concept=concept, amount=amount, sender=sender_account, receiver=receiver_account, recorded_balance=sender_account.balance)
        return Response({"Success": "The transfer has been successfully completed."}, status=200)
