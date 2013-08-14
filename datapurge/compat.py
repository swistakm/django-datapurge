# -*- coding: utf-8 -*-
from functools import partial
import django

if django.VERSION >= (1,4):
    from django.db.models import get_model
    get_model = partial(get_model, seed_cache=False, only_installed=True)
else:
    from django.db.models import get_model
    get_model = partial(get_model, seed_cache=False)