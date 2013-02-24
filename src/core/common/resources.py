# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from tastypie import fields
from tastypie.api import Api
from tastypie.cache import SimpleCache

from core.resources import (
    EXACT_IN,
    EXACT_IN_CONTAINS,
    EXACT_IN_GTE_LTE,
    EXACT_IN_GET_LTE_DATE,
    EXACT_IN_STARTSWITH,
    Meta, Resource,
)
from .models import Country


logger = logging.getLogger(__name__)


class UserResource(Resource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        allowed_methods = ('get',)
        cache = SimpleCache()
        excludes = ('password',)
        filtering = {
           'username': EXACT_IN,
        }

    def obj_create(self, bundle, request=None, **kwargs):
        # TODO
        pass

    def apply_authorization_limits(self, request, object_list):
        # TODO
        pass


class CountryResource(Resource):

    class Meta:
        queryset = Country.objects.all()
        resource_name = 'country'
        allowed_methods = ('get',)
        cache = SimpleCache()
        filtering = {
            'alpha2': EXACT_IN,
            'alpha3': EXACT_IN,
            'numeric3': EXACT_IN,
            'fips': EXACT_IN,
            'name': EXACT_IN_STARTSWITH,
            'capital': EXACT_IN_STARTSWITH,
            'area': EXACT_IN_GTE_LTE,
            'population': EXACT_IN_GTE_LTE,
            'continent': EXACT_IN,
            'tld': EXACT_IN,
            'currency_code': EXACT_IN,
            'currency_name': EXACT_IN_STARTSWITH,
            'phone': EXACT_IN_STARTSWITH,
            'postal_code_format': EXACT_IN_STARTSWITH,
            'postal_code_regex': EXACT_IN_STARTSWITH,
            'languages': EXACT_IN_CONTAINS,
            'geonameid': EXACT_IN_GTE_LTE,
            'neighbours': EXACT_IN_CONTAINS,
            'equivalent_fips_code': EXACT_IN,
        }


def get():
    api = Api(api_name='common')
    api.register(UserResource())
    api.register(CountryResource())
    return api.urls

urls = get()
