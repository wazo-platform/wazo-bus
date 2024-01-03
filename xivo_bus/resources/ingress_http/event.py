# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format
from .types import IngressHTTPDict


class IngressHTTPCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_created'
    routing_key_fmt = 'config.ingresses.http.created'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_deleted'
    routing_key_fmt = 'config.ingresses.http.deleted'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(ingress_http, tenant_uuid)


class IngressHTTPEditedEvent(TenantEvent):
    service = 'confd'
    name = 'ingress_http_edited'
    routing_key_fmt = 'config.ingresses.http.edited'

    def __init__(
        self,
        ingress_http: IngressHTTPDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(ingress_http, tenant_uuid)
