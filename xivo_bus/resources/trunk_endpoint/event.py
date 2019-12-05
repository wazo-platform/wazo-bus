# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseTrunkEndpointSIPEvent(BaseEvent):

    def __init__(self, trunk, sip):
        self._body = {
            'trunk': trunk,
            'endpoint_sip': sip,
        }
        super(_BaseTrunkEndpointSIPEvent, self).__init__()


class TrunkEndpointSIPAssociatedEvent(_BaseTrunkEndpointSIPEvent):

    name = 'trunk_endpoint_sip_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[id]}.updated'


class TrunkEndpointSIPDissociatedEvent(_BaseTrunkEndpointSIPEvent):

    name = 'trunk_endpoint_sip_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.sip.{endpoint_sip[id]}.deleted'


class _BaseTrunkEndpointIAXEvent(BaseEvent):

    def __init__(self, trunk, iax):
        self._body = {
            'trunk': trunk,
            'endpoint_iax': iax,
        }
        super(_BaseTrunkEndpointIAXEvent, self).__init__()


class TrunkEndpointIAXAssociatedEvent(_BaseTrunkEndpointIAXEvent):

    name = 'trunk_endpoint_iax_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.updated'


class TrunkEndpointIAXDissociatedEvent(_BaseTrunkEndpointIAXEvent):

    name = 'trunk_endpoint_iax_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.iax.{endpoint_iax[id]}.deleted'


class _BaseTrunkEndpointCustomEvent(BaseEvent):

    def __init__(self, trunk, custom):
        self._body = {
            'trunk': trunk,
            'endpoint_custom': custom,
        }
        super(_BaseTrunkEndpointCustomEvent, self).__init__()


class TrunkEndpointCustomAssociatedEvent(_BaseTrunkEndpointCustomEvent):

    name = 'trunk_endpoint_custom_associated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.updated'


class TrunkEndpointCustomDissociatedEvent(_BaseTrunkEndpointCustomEvent):

    name = 'trunk_endpoint_custom_dissociated'
    routing_key_fmt = 'config.trunks.{trunk[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'
