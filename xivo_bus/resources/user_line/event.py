# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseUserLineEvent(BaseEvent):

    def __init__(self, user_uuid, user_id, line_id, main_user, main_line, tenant_uuid):
        self._body = {
            'user_uuid': str(user_uuid),
            'user_id': int(user_id),
            'line_id': int(line_id),
            'main_user': bool(main_user),
            'main_line': bool(main_line),
            'tenant_uuid': str(tenant_uuid),
        }
        super(_BaseUserLineEvent, self).__init__()


class UserLineAssociatedEvent(_BaseUserLineEvent):

    name = 'line_associated'
    routing_key_fmt = 'config.user_line_association.created'


class UserLineDissociatedEvent(_BaseUserLineEvent):

    name = 'line_dissociated'
    routing_key_fmt = 'config.user_line_association.deleted'
