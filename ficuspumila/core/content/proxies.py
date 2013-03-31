# -*- coding: utf-8 -*-
import logging

from ficuspumila.core.proxies import get, Proxy
from ficuspumila.core.content import models


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


class FileTypeProxy(Proxy):

    pass


class ResourceTypeProxy(Proxy):

    pass


class FileSpecificationProxy(Proxy):

    pass


class FileSpecificationAttributeProxy(Proxy):

    pass


class OwnerProxy(Proxy):

    pass


Genre              = get('Genre')
GenreLocaliazation = get('GenreLocalization')
Source             = get('Source')
SourceAttribute    = get('SourceAttribute')
SourceEvent        = get('SourceEvent')
SourceNotification = get('SourceNotification')
FileType           = get('FileType')
ResourceType       = get('ResourceType')
FileSpecification  = get('FileSpecification')
FileSpecificationAttribute = get('FileSpecificationAttribute')
Owner              = get('Owner')