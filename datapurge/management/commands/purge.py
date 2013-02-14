# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from datapurge.exceptions import AmbiguousSettingsError
from datapurge.purge.actions import purge

class Command(BaseCommand):
    help = 'Purges old data'

    def handle(self, *args, **options):
        try:
            purge()
        except AmbiguousSettingsError, err:
            raise CommandError(str(err))
