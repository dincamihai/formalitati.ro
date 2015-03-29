# coding=utf-8
"""Should have a home page feature tests."""

import django
import pytest
from django.conf import settings
from django_webtest import DjangoTestApp
from functools import partial
from pytest_bdd import (scenario, given, then)


scenario = partial(scenario, '../features/home.feature')


@pytest.fixture
def client():
    django.setup()
    # code borrowed from django_webtest/__init__.py
    webtest_auth_middleware = "django_webtest.middleware.WebtestUserMiddleware"
    django_auth_middleware = (
        "django.contrib.auth.middleware.AuthenticationMiddleware"
    )

    middleware = list(settings.MIDDLEWARE_CLASSES)
    if django_auth_middleware not in settings.MIDDLEWARE_CLASSES:
        middleware.append(webtest_auth_middleware)
    else:
        index = middleware.index(django_auth_middleware)
        middleware.insert(index+1, webtest_auth_middleware)
    settings.MIDDLEWARE_CLASSES = middleware

    disable_csrf_middleware = 'django_webtest.middleware.DisableCSRFCheckMiddleware'
    if not disable_csrf_middleware in settings.MIDDLEWARE_CLASSES:
        settings.MIDDLEWARE_CLASSES.insert(0, disable_csrf_middleware)

    auth_backends = ["restapi.tests.common.WebtestCustomUserBackend"]
    auth_backends += list(settings.AUTHENTICATION_BACKENDS)
    settings.AUTHENTICATION_BACKENDS = auth_backends

    settings.DEBUG_PROPAGATE_EXCEPTIONS = True

    return DjangoTestApp()


@pytest.fixture
def context():
    return dict()


@scenario('Visit home page')
def test_visit_home_page():
    """Visit home page."""


@given('I request the home page')
def i_request_the_home_page(client, context):
    """I request the home page."""
    context['response'] = client.get('/', status=200)


@then('the page should be displayed')
def the_page_should_be_displayed(context):
    """the page should be displayed."""
    assert "home page" in context['response'].content
