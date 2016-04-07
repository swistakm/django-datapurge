# -*- coding: utf-8 -*-
from functools import partial
import django

if django.VERSION >= (1,9):
    from django.apps import apps
    get_model = apps.get_model
elif django.VERSION >= (1,7):
    from django.db.models import get_model
    get_model = get_model
elif django.VERSION >= (1,4):
    from django.db.models import get_model
    get_model = partial(get_model, seed_cache=False, only_installed=True)
else:
    from django.db.models import get_model
    get_model = partial(get_model, seed_cache=False)