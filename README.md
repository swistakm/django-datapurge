[![Build Status](https://travis-ci.org/swistakm/django-datapurge.png)](https://travis-ci.org/swistakm/django-datapurge)


# Django Datapurge

Simple app to help purging old data like sesions, nonces, logs etc.. It's
like `django-admin.py clearsessions` command but gives you possibility to
purge anything. Simpliest way to use `datapurge` is to run management
command (manually or via cron):

    python manage.py purge

It's easy to integrate datapurge with `celery` or `kronos`. Just wrap
`datapurge.actions.purge` function with code corresponding to your task
backend and run it the way you want.

# Requirements

* Python (2.6, 2.7, 3.4, 3.5)
* Django>=1.3.7

# Installation

Install from PyPI using pip:

    pip install django-datapurge

Or clone this repo:

    git clone git@github.com:swistakm/django-datapurge.git

Add `'datapurge'` to your `INSTALLED_APPS` setting.

    INSTALLED_APPS = (
        ...
        'datapurge',
    )

# Configuration

Add `DATAPURGE_MODELS` to your settings file and specify which models should be purged:

    DATAPURGE_MODELS = {
        'app_name.ModelName1': {
            # policy settings
            ...
            },
        'app_name.ModelName2': {
            ...
            },
    }

# Available purge policies

There are a few available policies for your use. Use what you find most convienient. Policy is
guessed from set parameters provided.


## ExpireFieldPolicy

Deletes all objects which `expire_field` datetime is older than `timezone.now()`.

Parameters:

* `'expire_field'` - name of datetime field holding expiration date

Example:

    DATAPURGE_MODELS = {
        "sessions.Session": {
            "expire_field": "expire_date",
        }
    }

## LifetimePolicy

Deletes all objects which are older than specified `lifetime`

Parameters:

* `'lifetime'` - timedelta object specifying maximum lifetime of object
* `'created_field'` - name of datetime field holding object creation time

Example:

    from timezone import timedelta

    DATAPURGE_MODELS = {
        "oauth_provider.Nonce": {
            "lifetime": timedelta(seconds=300),
            "created_field": "timestamp",
        }

## CallablePolicy

Deletes all objects from query returned by provided callable

Parameters:

* `'callable'` - function accepting model class and returning QuerySet

Example:

    DATAPURGE_MODELS = {
        "some_app.Log": {
            "callable": lambda model: model.objects.all(),
        }

