# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
from tastypie import fields
from tastypie.api import Api
from tastypie.cache import SimpleCache
from tastypie.exceptions import (
    ImmediateHttpResponse,
    InvalidFilterError,
    NotFound
)
from tastypie.http import HttpForbidden
from tastypie.resources import ALL, ALL_WITH_RELATIONS

from ficuspumila.core.api.resources import UserResource
from ficuspumila.core.content.resources import ContentResource
from ficuspumila.core.resources import (
    EXACT,
    EXACT_IN,
    EXACT_IN_CONTAINS,
    EXACT_IN_GTE_LTE,
    EXACT_IN_GET_LTE_DATE,
    EXACT_IN_STARTSWITH,
    Meta, ServiceMeta,
)
from ficuspumila.core.content.common.models import (
    FileType, Genre, GenreLocalization,
    ResourceType, Source, SourceAttribute,
)
from .models import (
    FileSpecification, FileSpecificationAttribute,
    Owner,
    SourceEvent, SourceNotification,
)


logger = logging.getLogger(__name__)


class GenreResource(ContentResource):

    class Meta:

        queryset = Genre.objects.all()
        resource_name = 'genre'
        allowed_methods = ('get',)
        cache = SimpleCache()
        filtering = {
            'type': EXACT_IN,
        }


class GenreLocalizationResource(ContentResource):

    class Meta:

        queryset = GenreLocalization.objects.all()
        resource_name = 'genrelocalization'
        allowed_methods = ('get',)
        cache = SimpleCache()
        filtering = {
            'genre'   : ALL_WITH_RELATIONS,
            'language': EXACT_IN,
            'name'    : EXACT_IN_STARTSWITH,
        }

    genre = fields.ForeignKey(GenreResource, 'genre')


class SourceResource(ContentResource):

    class Meta(ServiceMeta):

        queryset = Source.objects.all()
        resource_name = 'source'
        allowed_methods = ('get',)
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'name': EXACT_IN_CONTAINS,
            'source_owener_id': EXACT_IN_STARTSWITH,
        }

    user = fields.ForeignKey(UserResource, 'user')

    def apply_authorization_limits(self, request, object_list):
        if hasattr(request.user, 'owner'):
            return object_list.filter(pk=request.user.owner.source.pk)

        raise ImmediateHttpResponse(response=HttpForbidden())


class SourceAttributeResource(ContentResource):

    class Meta(Meta):

        queryset = SourceAttribute.objects.all()
        resource_name = 'sourceattribute'
        allowed_methods = ('get',)
        filtering = {
            'source': ALL_WITH_RELATIONS,
            'name'  : EXACT_IN_STARTSWITH,
            'value' : EXACT_IN_STARTSWITH,
        }

    source = fields.ForeignKey(SourceResource, 'source')


class SourceEventResource(ContentResource):

    class Meta(Meta):

        queryset = SourceEvent.objects.all()
        resource_name = 'sourceevent'
        allowed_methods = ('get', 'post', 'put')
        filtering = {
            'source' : ALL_WITH_RELATIONS,
            'event'  : EXACT_IN,
            'message': EXACT_IN_CONTAINS,
            'ctime'  : EXACT_IN_GET_LTE_DATE,
            'utime'  : EXACT_IN_GET_LTE_DATE,
        }

    source = fields.ForeignKey(SourceResource, 'source')


class SourceNotificationResource(ContentResource):

    class Meta(Meta):

        queryset = SourceNotification.objects.all()
        resource_name = 'sourcenotification'
        allowed_methods = ('get',)
        filtering = {
            'event'      : ALL_WITH_RELATIONS,
            'url'        : EXACT_IN_CONTAINS,
            'status_code': EXACT_IN,
            'content'    : EXACT_IN_CONTAINS,
            'ctime'      : EXACT_IN_GET_LTE_DATE,
            'utime'      : EXACT_IN_GET_LTE_DATE,
        }

    event = fields.ForeignKey(SourceEventResource, 'event')


class FileTypeResource(ContentResource):

    class Meta(Meta):

        queryset = FileType.objects.all()
        resource_name = 'filetype'
        allowed_methods = ('get',)
        filtering = {
            'name'     : EXACT_IN_STARTSWITH,
            'mimetype' : EXACT_IN_CONTAINS,
            'extention': EXACT_IN_STARTSWITH,
        }


class FileSpecificationResource(ContentResource):

    class Meta(Meta):

        queryset = FileSpecification.objects.all()
        resource_name = 'filespecification'
        allowed_methods = ('get', 'post', 'put', 'patch',)
        filtering = {
            'source': ALL_WITH_RELATIONS,
            'name'  : EXACT_IN_STARTSWITH,
            'type'  : ALL_WITH_RELATIONS,
        }

    source = fields.ForeignKey(SourceResource, 'source')
    type = fields.ForeignKey(FileTypeResource, 'type')


class FileSpecificationAttributeResource(ContentResource):

    class Meta(Meta):

        queryset = FileSpecificationAttribute.objects.all()
        resource_name = 'filespecificationattribute'
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete',)
        filtering = {
            'spec' : ALL_WITH_RELATIONS,
            'name' : EXACT_IN_STARTSWITH,
            'value': EXACT_IN_STARTSWITH,
        }

    spec = fields.ForeignKey(FileSpecificationResource, 'spec')


class ResourceTypeResource(ContentResource):

    class Meta(Meta):

        queryset = ResourceType.objects.all()
        resource_name = 'resourcetype'
        allowed_methods = ('get',)
        filtering = {
            'name'      : EXACT_IN_STARTSWITH,
            'category'  : EXACT_IN,
            'limited'   : EXACT,
            'streamable': EXACT,
        }


class OwnerResource(ContentResource):

    class Meta(Meta):

        queryset = Owner.objects.all()
        resource_name = 'owner'
        allowed_methods = ('get',)
        filtering = {
            'user'  : ALL_WITH_RELATIONS,
            'source': ALL_WITH_RELATIONS,
            'source_owner_id': EXACT_IN_STARTSWITH,
        }

    user = fields.ForeignKey(UserResource, 'user')
    source = fields.ForeignKey(SourceResource,
                               'source')


def get_urls(version=1):
    api = Api(api_name='content')

    if version == 1:
        api.register(GenreResource())
        api.register(GenreLocalizationResource())
        api.register(SourceResource())
        api.register(SourceAttributeResource())
        api.register(SourceEventResource())
        api.register(SourceNotificationResource())
        api.register(FileTypeResource())
        api.register(FileSpecificationResource())
        api.register(FileSpecificationAttributeResource())
        api.register(ResourceTypeResource())

        api.register(OwnerResource())

    return api.urls
