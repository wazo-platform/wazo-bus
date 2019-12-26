# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseLineEndpointSIPEvent(BaseEvent):

    def __init__(self, line, sip):
        self._body = {
            'line': line,
            'endpoint_sip': sip,
        }
        super(_BaseLineEndpointSIPEvent, self).__init__()


class LineEndpointSIPAssociatedEvent(_BaseLineEndpointSIPEvent):

    name = 'line_endpoint_sip_associated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[id]}.updated'


class LineEndpointSIPDissociatedEvent(_BaseLineEndpointSIPEvent):

    name = 'line_endpoint_sip_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[id]}.deleted'


class _BaseLineEndpointSCCPEvent(BaseEvent):

    def __init__(self, line, sccp):
        self._body = {
            'line': line,
            'endpoint_sccp': sccp,
        }
        super(_BaseLineEndpointSCCPEvent, self).__init__()


class LineEndpointSCCPAssociatedEvent(_BaseLineEndpointSCCPEvent):

    name = 'line_endpoint_sccp_associated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.updated'


class LineEndpointSCCPDissociatedEvent(_BaseLineEndpointSCCPEvent):

    name = 'line_endpoint_sccp_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.deleted'


class _BaseLineEndpointCustomEvent(BaseEvent):

    def __init__(self, line, custom):
        self._body = {
            'line': line,
            'endpoint_custom': custom,
        }
        super(_BaseLineEndpointCustomEvent, self).__init__()


class LineEndpointCustomAssociatedEvent(_BaseLineEndpointCustomEvent):

    name = 'line_endpoint_custom_associated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.updated'


class LineEndpointCustomDissociatedEvent(_BaseLineEndpointCustomEvent):

    name = 'line_endpoint_custom_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'
