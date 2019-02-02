# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditRegisterSIPEvent(ResourceConfigEvent):
    name = 'register_sip_edited'
    routing_key = 'config.register.sip.edited'


class CreateRegisterSIPEvent(ResourceConfigEvent):
    name = 'register_sip_created'
    routing_key = 'config.register.sip.created'


class DeleteRegisterSIPEvent(ResourceConfigEvent):
    name = 'register_sip_deleted'
    routing_key = 'config.register.sip.deleted'


class EditRegisterIAXEvent(ResourceConfigEvent):
    name = 'register_iax_edited'
    routing_key = 'config.register.iax.edited'


class CreateRegisterIAXEvent(ResourceConfigEvent):
    name = 'register_iax_created'
    routing_key = 'config.register.iax.created'


class DeleteRegisterIAXEvent(ResourceConfigEvent):
    name = 'register_iax_deleted'
    routing_key = 'config.register.iax.deleted'
