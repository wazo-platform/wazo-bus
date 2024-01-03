# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent


class OutcallExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_associated'
    routing_key_fmt = 'config.outcalls.extensions.updated'

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class OutcallExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'outcall_extension_dissociated'
    routing_key_fmt = 'config.outcalls.extensions.deleted'

    def __init__(
        self,
        outcall_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'outcall_id': outcall_id,
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
