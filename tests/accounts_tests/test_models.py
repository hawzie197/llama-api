from tests.base_case import BaseTestCase
from django.contrib.auth.models import User

# [Python]
from model_mommy import mommy


class AccountsModelsTestCase(BaseTestCase):
    def setUp(self):
        return super(AccountsModelsTestCase, self).setUp()

    def test_user_can_create(self):
        instance = mommy.make(User)
        self.assertTrue(isinstance(instance, User))
