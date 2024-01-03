# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class ExtensionCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_created'
    routing_key_fmt = 'config.extensions.created'

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super().__init__(content, tenant_uuid)


class ExtensionDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_deleted'
    routing_key_fmt = 'config.extensions.deleted'

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super().__init__(content, tenant_uuid)


class ExtensionEditedEvent(TenantEvent):
    service = 'confd'
    name = 'extension_edited'
    routing_key_fmt = 'config.extensions.edited'

    def __init__(
        self,
        extension_id: int,
        exten: str,
        context: str,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'id': int(extension_id),
            'exten': exten,
            'context': context,
        }
        super().__init__(content, tenant_uuid)
