# [Django]
from django.test import TestCase
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    def setUp(self):

        # Initialize HTTP client
        self.client = APIClient(enforce_csrf_checks=True)
