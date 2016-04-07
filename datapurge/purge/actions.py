# -*- coding: utf-8 -*-
import datetime

from datapurge import settings
from datapurge.purge.tasks import PurgeTask

def purge(now=None):
    # todo: timezone handling
    models = settings.DATAPURGE_MODELS
    now = now or datetime.datetime.utcnow()

    for model, conf in models.items():
        task = PurgeTask.create_from_conf(model, conf, now)
        task()
