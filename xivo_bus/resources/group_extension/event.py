# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class GroupExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_extension_associated'
    routing_key_fmt = 'config.groups.extensions.updated'

    def __init__(
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        extension_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)


class GroupExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'group_extension_dissociated'
    routing_key_fmt = 'config.groups.extensions.deleted'

    def __init__(
        self,
        group_id: int,
        group_uuid: Annotated[str, Format('uuid')],
        extension_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'group_id': group_id,
            'group_uuid': str(group_uuid),
            'extension_id': extension_id,
        }
        super().__init__(content, tenant_uuid)
