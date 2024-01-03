# Copyright 2014-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format


class FuncKeyTemplateCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_created'
    routing_key_fmt = 'config.funckey.template.created'

    def __init__(self, template_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_deleted'
    routing_key_fmt = 'config.funckey.template.deleted'

    def __init__(self, template_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)


class FuncKeyTemplateEditedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_edited'
    routing_key_fmt = 'config.funckey.template.edited'

    def __init__(self, template_id: int, tenant_uuid: Annotated[str, Format('uuid')]):
        content = {'id': template_id}
        super().__init__(content, tenant_uuid)
