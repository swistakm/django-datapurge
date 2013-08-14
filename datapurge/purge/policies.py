# -*- coding: utf-8 -*-
import datetime

from datapurge.exceptions import AmbiguousSettingsError
from datapurge.settings import DATAPURGE_GRACEFULLY

class BasePurgePolicy(object):
    """Base purge policy for purging old data"""

    def __init__(self, *args, **kwargs):
        self.grecefully = DATAPURGE_GRACEFULLY
        self.model = None

    def apply_policy(self, model, now=None):
        """ Applies purge policy to specified model.

        todo: creating self-purging (or not) logs
        :param model: Model class
        """
        # todo: timezone handling
        self.now = now or datetime.datetime.utcnow()
        self.model = model
        self.purge()

    def purge(self):
        """purges data gracefully or not

        todo: do it gracefully

        """
        if not self.grecefully:
            self.get_queryset().delete()
        else:
            raise NotImplemented

    def get_queryset(self):
        """ Gets model queryset
        :return: queryset to delete
        """
        raise NotImplemented


class CallablePolicy(BasePurgePolicy):

    def __init__(self, callable):
        super(CallablePolicy, self).__init__(callable)
        self.callable = callable

    def get_queryset(self):
        return self.callable(self.model)


class ExpireFieldPolicy(BasePurgePolicy):

    def __init__(self, expire_field):
        super(ExpireFieldPolicy, self).__init__(expire_field)
        self.expire_field = expire_field

    def get_queryset(self):
        query = {self.expire_field + '__lte': self.now}
        return self.model.objects.filter(**query)


class LifetimePolicy(BasePurgePolicy):

    def __init__(self, lifetime, created_field):
        super(LifetimePolicy, self).__init__(lifetime, created_field)
        self.lifetime = lifetime
        self.created_field = created_field

    def get_queryset(self):
        query = {self.created_field + '__lte': self.now - self.lifetime}
        return self.model.objects.filter(**query)


class DummyPolicy(BasePurgePolicy):
    def purge(self):
        pass


# Map settings kwargs to policy classes, use frozensets cause are hashable
POLICY_KWARGS_MAPPING = {
    frozenset(("callable",)): CallablePolicy,
    frozenset(("expire_field",)): ExpireFieldPolicy,
    frozenset(("lifetime", "created_field",)): LifetimePolicy,
    frozenset(): DummyPolicy,
}


def create_policy(**kwargs):
    """ Guess policy class by provided kwargs and create it's object
    """
    parameters = kwargs.keys()
    try:
        PolicyClass = POLICY_KWARGS_MAPPING.get(frozenset(parameters))
        return PolicyClass(**kwargs)
    except KeyError:
        raise AmbiguousSettingsError("Can not initialize any policy class with parameters %s" % kwargs)

