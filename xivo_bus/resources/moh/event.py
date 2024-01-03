# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format
from .types import MOHDict


class MOHCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_created'
    routing_key_fmt = 'config.moh.created'

    def __init__(self, moh: MOHDict, tenant_uuid: Annotated[str, Format('uuid')]):
        super().__init__(moh, tenant_uuid)


class MOHDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_deleted'
    routing_key_fmt = 'config.moh.deleted'

    def __init__(self, moh: MOHDict, tenant_uuid: Annotated[str, Format('uuid')]):
        super().__init__(moh, tenant_uuid)


class MOHEditedEvent(TenantEvent):
    service = 'confd'
    name = 'moh_edited'
    routing_key_fmt = 'config.moh.edited'

    def __init__(self, moh: MOHDict, tenant_uuid: Annotated[str, Format('uuid')]):
        super().__init__(moh, tenant_uuid)
