# -*- coding: utf-8 -*-
import logging

from core.proxies import get, Proxy
from . import models


COMMON_MODELS = 'core.content.common.models'

logger = logging.getLogger(__name__)


class GenreProxy(Proxy):

    pass


class GenreLocalizationProxy(Proxy):

    pass


class SourceProxy(Proxy):

    pass


class SourceAttributeProxy(Proxy):

    pass


class SourceEventProxy(Proxy):

    pass


class SourceNotificationProxy(Proxy):

    pass


class OwnerProxy(Proxy):

    pass


Genre              = get('Genre', COMMON_MODELS)
GenreLocaliazation = get('GenreLocalization', COMMON_MODELS)
Source             = get('Source', COMMON_MODELS)
SourceAttribute    = get('SourceAttribute', COMMON_MODELS)
SourceEvent        = get('SourceEvent', COMMON_MODELS)
SourceNotification = get('SourceNotification', COMMON_MODELS)
Owner              = get('Owner')
