# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class RequestHandlersProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'request_handlers_progress'
    routing_key_fmt = 'sysconfd.request_handlers.{uuid}.{status}'

    def __init__(self, request_uuid, request_context, status):
        content = {
            'uuid': str(request_uuid),
            'status': status,
            'context': request_context,
        }
        super(RequestHandlersProgressEvent, self).__init__(content)


class AsteriskReloadProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'asterisk_reload_progress'
    routing_key_fmt = 'sysconfd.asterisk.reload.{uuid}.{status}'

    def __init__(self, uuid, status, command, request_uuids):
        content = {
            'uuid': str(uuid),
            'status': status,
            'command': command,
            'request_uuids': request_uuids,
        }
        super(AsteriskReloadProgressEvent, self).__init__(content)
