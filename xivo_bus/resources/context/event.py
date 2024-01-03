# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from .types import ContextDict


class ContextCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'context_created'
    routing_key_fmt = 'config.contexts.created'

    def __init__(
        self, context_data: ContextDict, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        super().__init__(context_data, tenant_uuid)


class ContextDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'context_deleted'
    routing_key_fmt = 'config.contexts.deleted'

    def __init__(
        self, context_data: ContextDict, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        super().__init__(context_data, tenant_uuid)


class ContextEditedEvent(TenantEvent):
    service = 'confd'
    name = 'context_edited'
    routing_key_fmt = 'config.contexts.edited'

    def __init__(
        self, context_data: ContextDict, tenant_uuid: Annotated[str, {'format': 'uuid'}]
    ):
        super().__init__(context_data, tenant_uuid)
