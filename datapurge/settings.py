# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils import timezone

DATAPURGE_GRACEFULLY = getattr(settings, "DATAPURGE_GRACEFULLY", False)
DATAPURGE_GRACE_STEP = getattr(settings, "DATAPURGE_GRACE_STEP", 100)
DATAPURGE_GRACE_WAIT = getattr(settings, "DATAPURGE_GRACE_WAIT", timezone.timedelta(seconds=0.3))

DATAPURGE_MODELS = getattr(settings, "DATAPURGE_MODELS", ())