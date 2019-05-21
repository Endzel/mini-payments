from decimal import Decimal

from rest_framework.test import APIRequestFactory, force_authenticate
from django.test import TestCase
from django.conf import settings

from api.views.user import LoginView, LogoutView, UserProfileView
from api.views.account import AccountView
from api.views.transfer import TransferView
from api.models import UserProfile, Account, Transfer


"""
USER PROFILE TESTS
"""


class LoginTest(TestCase):
    user = None
    url = "http://" + settings.BASE_API + "/api/login"
    object_view = LoginView
    data = {'username': 'test@gmail.com', 'password': '12345678'}
    invalid_data = {'username': 'test@gmail.com', 'password': 'whatever'}

    def setUp(self):
        UserProfile.objects.create(email="test@gmail.com",
                                    first_name="Test",
                                    last_name="Account",
                                    phone_number="+34666666666",
                                    password="12345678")

    def test_login_unauthorized(self):
        request = APIRequestFactory().post(self.url, self.invalid_data)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 401)


class UserProfileTest(TestCase):
    user = None
    url = "http://" + settings.BASE_API + "/api/users"
    object_view = UserProfileView
    data = {'email': 'test1@gmail.com', "first_name": "Testo", "last_name": "Accounto", "phone_number": "+34666666665", 'password': '12345678'}
    invalid_data = {}

    def setUp(self):
        self.user = UserProfile.objects.create(email="test@gmail.com",
                                               first_name="Test",
                                               last_name="Account",
                                               phone_number="+34666666666",
                                               password="12345678")

    def test_user_profile_unauthorized(self):
        self.user = None
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 401)

    def test_user_profile_authorized(self):
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.user)
        response = object_view(request)
        self.assertEqual(response.status_code, 200)

    def test_user_profile_creation(self):
        self.user = None
        request = APIRequestFactory().post(self.url, self.data)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 201)

    def test_user_profile_creation_invalid(self):
        self.user = None
        request = APIRequestFactory().post(self.url, self.invalid_data)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 400)


class AccountTest(TestCase):
    user = None
    url = "http://" + settings.BASE_API + "/api/accounts"
    object_view = AccountView
    creation_data = {}

    def setUp(self):
        self.user = UserProfile.objects.create(email="test@gmail.com",
                                               first_name="Test",
                                               last_name="Account",
                                               phone_number="+34666666666",
                                               password="12345678")

    def test_account_unauthorized(self):
        self.user = None
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 401)

    def test_account_authorized(self):
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.user)
        response = object_view(request)
        self.assertEqual(response.status_code, 200)

    def test_account_creation(self):
        request = APIRequestFactory().post(self.url, self.creation_data)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.user)
        response = object_view(request)
        self.assertEqual(response.status_code, 201)
        response = object_view(request)
        self.assertEqual(response.status_code, 400)


class TransferTest(TestCase):
    sender = None
    receiver = None
    sender_account = None
    receiver_account = None
    url = "http://" + settings.BASE_API + "/api/transfers"
    object_view = TransferView
    sent_data = {"amount": 200.89, "receiver": 6, "concept": "Will not send more money again."}
    invalid_amount_data = {"amount": 200000.89, "receiver": 12, "concept": "Will not send more money again."}
    empty_data = {}

    def setUp(self):
        self.sender = UserProfile.objects.create(email="sender@gmail.com",
                                               first_name="Sender",
                                               last_name="Account",
                                               phone_number="+34666666666",
                                               password="12345678")
        self.receiver = UserProfile.objects.create(email="receiver@gmail.com",
                                               first_name="Receiver",
                                               last_name="Account",
                                               phone_number="+34666666666",
                                               password="12345678")
        self.sender_account = Account.objects.create(user=self.sender)
        self.receiver_account = Account.objects.create(user=self.receiver)
        self.sender_account.balance = Decimal(10000.00)
        self.receiver_account.balance = Decimal(100.00)
        self.previous_receiver_balance = self.receiver_account.balance

    def test_transfer_unauthorized(self):
        self.sender = None
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        response = object_view(request)
        self.assertEqual(response.status_code, 401)

    def test_transfer_history_authorized(self):
        request = APIRequestFactory().get(self.url)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.sender)
        response = object_view(request)
        self.assertEqual(response.status_code, 200)

    def test_transfer_invalid_amount(self):
        request = APIRequestFactory().post(self.url, self.invalid_amount_data)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.sender)
        response = object_view(request)
        self.assertEqual(response.status_code, 400)

    def test_transfer_empty_data(self):
        request = APIRequestFactory().post(self.url, self.empty_data)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.sender)
        response = object_view(request)
        self.assertEqual(response.status_code, 400)

    def test_transfer_authorized(self):
        request = APIRequestFactory().post(self.url, self.sent_data)
        object_view = self.object_view.as_view()
        force_authenticate(request, self.sender)
        response = object_view(request)
        self.assertEqual(response.status_code, 200)
        transfer = Transfer.objects.get(pk=1)
        self.assertEqual(transfer.concept, self.sent_data['concept'])
        self.assertEqual(transfer.recorded_balance, self.sender_account.balance)
