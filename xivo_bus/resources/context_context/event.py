# Copyright 2018-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class ContextContextsAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'contexts_associated'
    routing_key_fmt = 'config.contexts.contexts.updated'

    def __init__(
        self,
        context_id: int,
        context_ids: list[int],
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        content = {
            'context_id': context_id,
            'context_ids': context_ids,
        }
        super().__init__(content, tenant_uuid)
