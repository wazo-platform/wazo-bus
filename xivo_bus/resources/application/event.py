# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import TenantEvent

from .types import ApplicationDict


class ApplicationCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'application_created'
    routing_key_fmt = 'config.applications.created'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        super().__init__(application, tenant_uuid)


class ApplicationDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'application_deleted'
    routing_key_fmt = 'config.applications.deleted'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        super().__init__(application, tenant_uuid)


class ApplicationEditedEvent(TenantEvent):
    service = 'confd'
    name = 'application_edited'
    routing_key_fmt = 'config.applications.edited'

    def __init__(
        self,
        application: ApplicationDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        super().__init__(application, tenant_uuid)
