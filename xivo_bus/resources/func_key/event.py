# -*- coding: utf-8 -*-
# Copyright 2014-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class FuncKeyTemplateCreatedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_created'
    routing_key_fmt = 'config.funckey.template.created'

    def __init__(self, template_id, tenant_uuid):
        content = {'id': template_id}
        super(FuncKeyTemplateCreatedEvent, self).__init__(content, tenant_uuid)


class FuncKeyTemplateDeletedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_deleted'
    routing_key_fmt = 'config.funckey.template.deleted'

    def __init__(self, template_id, tenant_uuid):
        content = {'id': template_id}
        super(FuncKeyTemplateDeletedEvent, self).__init__(content, tenant_uuid)


class FuncKeyTemplateEditedEvent(TenantEvent):
    service = 'confd'
    name = 'func_key_template_edited'
    routing_key_fmt = 'config.funckey.template.edited'

    def __init__(self, template_id, tenant_uuid):
        content = {'id': template_id}
        super(FuncKeyTemplateEditedEvent, self).__init__(content, tenant_uuid)
