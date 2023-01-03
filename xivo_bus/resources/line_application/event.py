# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class LineApplicationAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_associated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.updated'

    def __init__(self, line, application, tenant_uuid):
        content = {'line': line, 'application': application}
        super(LineApplicationAssociatedEvent, self).__init__(content, tenant_uuid)


class LineApplicationDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.deleted'

    def __init__(self, line, application, tenant_uuid):
        content = {'line': line, 'application': application}
        super(LineApplicationDissociatedEvent, self).__init__(content, tenant_uuid)
