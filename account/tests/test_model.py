from account.models import CustomUser, Address
from model_bakery import baker
from django.test import TestCase


class TestCustomUser(TestCase):
    def setUp(self):
        self.user = baker.make(CustomUser, email="mamad@gmail.com")

    def test_model_str(self):
        self.assertEqual(str(self.user), 'mamad@gmail.com')


class TestAddress(TestCase):
    def setUp(self):
        self.address = baker.make(Address, city="tehran", street="jenah")

    def test_model_str(self):
        self.assertEqual(str(self.address), ' city --> tehran street --> jenah')
