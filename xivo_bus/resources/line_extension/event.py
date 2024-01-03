# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class LineExtensionAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_associated'
    routing_key_fmt = 'config.line_extension_associated.updated'

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super().__init__(content, tenant_uuid)


class LineExtensionDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_extension_dissociated'
    routing_key_fmt = 'config.line_extension_associated.deleted'

    def __init__(
        self,
        line_id: int,
        extension_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'line_id': line_id, 'extension_id': extension_id}
        super().__init__(content, tenant_uuid)
