# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class RegistrarCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_created'
    routing_key_fmt = 'config.registrar.created'

    def __init__(self, registrar):
        super(RegistrarCreatedEvent, self).__init__(registrar)


class RegistrarDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_deleted'
    routing_key_fmt = 'config.registrar.deleted'

    def __init__(self, registrar):
        super(RegistrarDeletedEvent, self).__init__(registrar)


class RegistrarEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'registrar_edited'
    routing_key_fmt = 'config.registrar.edited'

    def __init__(self, registrar):
        super(RegistrarEditedEvent, self).__init__(registrar)
