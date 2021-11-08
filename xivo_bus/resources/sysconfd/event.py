# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class RequestHandlersProgressEvent(BaseEvent):

    name = 'request_handlers_progress'
    routing_key_fmt = 'sysconfd.request_handlers.{uuid}.{status}'

    def __init__(self, request, status):
        self._body = {
            'uuid': request.uuid,
            'status': status,
            'context': request.context,
        }
        super(RequestHandlersProgressEvent, self).__init__()
