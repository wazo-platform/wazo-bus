# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format
from .types import EndpointIAXDict


class IAXEndpointCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_created'
    routing_key_fmt = 'config.iax_endpoint.created'

    def __init__(
        self, endpoint: EndpointIAXDict, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_deleted'
    routing_key_fmt = 'config.iax_endpoint.deleted'

    def __init__(
        self, endpoint: EndpointIAXDict, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        super().__init__(endpoint, tenant_uuid)


class IAXEndpointEditedEvent(TenantEvent):
    service = 'confd'
    name = 'iax_endpoint_edited'
    routing_key_fmt = 'config.iax_endpoint.edited'

    def __init__(
        self, endpoint: EndpointIAXDict, tenant_uuid: Annotated[str, Format('uuid')]
    ):
        super().__init__(endpoint, tenant_uuid)
