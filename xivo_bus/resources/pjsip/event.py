# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class PJSIPGlobalUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'pjsip_global_updated'
    routing_key_fmt = 'config.pjsip_global.updated'

    def __init__(self):
        super(PJSIPGlobalUpdatedEvent, self).__init__()


class PJSIPSystemUpdatedEvent(ServiceEvent):
    service = 'confd'
    name = 'pjsip_system_updated'
    routing_key_fmt = 'config.pjsip_system.updated'

    def __init__(self):
        super(PJSIPSystemUpdatedEvent, self).__init__()


class SIPTransportCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_created'
    routing_key_fmt = 'config.sip.transports.created'

    def __init__(self, transport):
        super(SIPTransportCreatedEvent, self).__init__(transport)


class SIPTransportDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_deleted'
    routing_key_fmt = 'config.sip.transports.deleted'

    def __init__(self, transport):
        super(SIPTransportDeletedEvent, self).__init__(transport)


class SIPTransportEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'sip_transport_edited'
    routing_key_fmt = 'config.sip.transports.edited'

    def __init__(self, transport):
        super(SIPTransportEditedEvent, self).__init__(transport)
