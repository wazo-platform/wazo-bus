# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class RegisterSIPCreated(ServiceEvent):
    service = 'confd'
    name = 'register_sip_created'
    routing_key_fmt = 'config.register.sip.created'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterSIPCreated, self).__init__(content)


class RegisterSIPDeleted(ServiceEvent):
    service = 'confd'
    name = 'register_sip_deleted'
    routing_key_fmt = 'config.register.sip.deleted'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterSIPDeleted, self).__init__(content)


class RegisterSIPEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_sip_edited'
    routing_key_fmt = 'config.register.sip.edited'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterSIPEditedEvent, self).__init__(content)


class RegisterIAXCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_created'
    routing_key_fmt = 'config.register.iax.created'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterIAXCreatedEvent, self).__init__(content)


class RegisterIAXDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_deleted'
    routing_key_fmt = 'config.register.iax.deleted'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterIAXDeletedEvent, self).__init__(content)


class RegisterIAXEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'register_iax_edited'
    routing_key_fmt = 'config.register.iax.edited'

    def __init__(self, register_id):
        content = {'id': int(register_id)}
        super(RegisterIAXEditedEvent, self).__init__(content)
