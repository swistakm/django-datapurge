# -*- coding: utf-8 -*-
from datapurge import settings
from django.utils import timezone
from datapurge.purge.tasks import PurgeTask

def purge(now=None):
    models = settings.DATAPURGE_MODELS
    now = now or timezone.now()

    for model, conf in models.iteritems():
        task = PurgeTask.create_from_conf(model, conf, now)
        task()
