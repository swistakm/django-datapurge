"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from datapurge.purge.actions import purge
from datapurge.purge.policies import CallablePolicy, ExpireFieldPolicy, LifetimePolicy
from datapurge.purge.tasks import PurgeTask


class TestWith100Users(TestCase):
    def setUp(self):
        dt = datetime.datetime.now()
        self.users = []

        # we use User model for test because it's in contrib and has datetime field we want
        for number in range(100):
            new_user = User.objects.create(
                username="testUser%s" % number,
                date_joined=dt - datetime.timedelta(days=number))
            self.users.append(new_user)

        #reverse to preserve chronological order
        self.users.reverse()

        self.assertEqual(User.objects.count(), 100)

class PoliciesTest(TestWith100Users):
    def test_CallablePolicy(self):
        expire_date = self.users[59].date_joined
        callable = lambda model: model.objects.filter(date_joined__lte=expire_date)

        policy = CallablePolicy(callable=callable)
        policy.apply_policy(User)

        self.assertEqual(User.objects.count(), 40)

    def test_ExpireFieldPolicy(self):
        fake_now = self.users[59].date_joined

        policy = ExpireFieldPolicy(expire_field="date_joined")
        policy.apply_policy(model=User, now=fake_now)

        self.assertEqual(User.objects.count(), 40)

    def test_LifetimePolicy(self):
        lifetime = self.users[-1].date_joined - self.users[59].date_joined
        fake_now = self.users[-1].date_joined

        policy = LifetimePolicy(lifetime=lifetime, created_field="date_joined")
        policy.apply_policy(model=User, now=fake_now)

        self.assertEqual(User.objects.count(), 40)

class PurgeTaskTest(TestWith100Users):
    def test_purge_by_expire_field(self):
        fake_now = self.users[59].date_joined

        relation = "auth.User"
        params =  {
            "expire_field": "date_joined",
        }

        task = PurgeTask.create_from_conf(relation, params, fake_now)
        task()

        self.assertEqual(User.objects.count(), 40)

    def test_purge_by_lifetime_field(self):
        lifetime = self.users[-1].date_joined - self.users[59].date_joined
        fake_now = self.users[-1].date_joined

        relation = "auth.User"
        params = {
            "lifetime": lifetime,
            "created_field": "date_joined"
        }

        task = PurgeTask.create_from_conf(relation, params, fake_now)
        task()

        self.assertEqual(User.objects.count(), 40)

    def test_purge_with_callable(self):
        expire_date = self.users[59].date_joined

        relation = "auth.User"
        params = {
            "callable": lambda model: model.objects.filter(date_joined__lte=expire_date)
        }

        task = PurgeTask.create_from_conf(relation, params)
        task()

        self.assertEqual(User.objects.count(), 40)

class PurgeActionTest(TestWith100Users):
    def test_purge_action(self):
        expire_date = self.users[59].date_joined

        # monkeypatch datapurge settings
        from datapurge import settings
        settings.DATAPURGE_MODELS = {
            "auth.User": {
                "callable": lambda model: model.objects.filter(date_joined__lte=expire_date)
            }
        }

        purge()

        self.assertEqual(User.objects.count(), 40)
