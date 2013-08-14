# -*- coding: utf-8 -*-
from datapurge.purge.policies import DummyPolicy, create_policy
from datapurge.compat import get_model

class PurgeTask(object):
    def __init__(self, model, policy=None, now=None):
        """
         :type policy: datapurge.purge.policies.BasePurgePolicy
        """
        self.model = model
        self.now = now
        self.policy = policy or DummyPolicy()

    def __call__(self, *args, **kwargs):
        self.policy.apply_policy(self.model, self.now)

    @classmethod
    def create_from_conf(cls, model_relation, options, force_now=None):
        app_label, model_name = model_relation.split(".")
        model = get_model(app_label, model_name)

        policy = create_policy(**options)
        return cls(model, policy, force_now)
