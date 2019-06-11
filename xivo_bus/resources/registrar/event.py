# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class DeleteRegistrarEvent(BaseEvent):
    name = 'registrar_deleted'
    routing_key_fmt = 'config.registrar.deleted'

    def __init__(self, registrar_info):
        self._body = registrar_info
        super(DeleteRegistrarEvent, self).__init__()


class EditRegistrarEvent(BaseEvent):
    name = 'registrar_edited'
    routing_key_fmt = 'config.registrar.edited'

    def __init__(self, registrar_info):
        self._body = registrar_info
        super(EditRegistrarEvent, self).__init__()


class CreateRegistrarEvent(BaseEvent):
    name = 'registrar_created'
    routing_key_fmt = 'config.registrar.created'

    def __init__(self, registrar_info):
        self._body = registrar_info
        super(CreateRegistrarEvent, self).__init__()
