# -*- coding: utf-8 -*-
# Copyright 2018-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class AsteriskReloadProgressEvent(BaseEvent):

    name = 'asterisk_reload_progress'
    routing_key_fmt = 'sysconfd.asterisk.reload.{uuid}.{status}'

    def __init__(self, uuid, status, command, request_uuids):
        self._body = {
            'uuid': uuid,
            'status': status,
            'command': command,
            'request_uuids': request_uuids,
        }
        super(AsteriskReloadProgressEvent, self).__init__()
