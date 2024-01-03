# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from xivo_bus.resources.common.event import TenantEvent


class IncallExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_extension_associated'
    routing_key_fmt = 'config.incalls.extensions.updated'

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'incall_id': incall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class IncallExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'incall_extension_dissociated'
    routing_key_fmt = 'config.incalls.extensions.deleted'

    def __init__(
        self,
        incall_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'incall_id': incall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
