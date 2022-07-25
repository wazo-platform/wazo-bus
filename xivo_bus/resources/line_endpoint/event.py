# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent


class LineEndpointSIPAssociatedEvent(TenantEvent):
    name = 'line_endpoint_sip_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated'
    )

    def __init__(self, line, sip, tenant_uuid):
        content = {'line': line, 'endpoint_sip': sip}
        super(LineEndpointSIPAssociatedEvent, self).__init__(content, tenant_uuid)


class LineEndpointSIPDissociatedEvent(TenantEvent):
    name = 'line_endpoint_sip_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted'
    )

    def __init__(self, line, sip, tenant_uuid):
        content = {'line': line, 'endpoint_sip': sip}
        super(LineEndpointSIPDissociatedEvent, self).__init__(content, tenant_uuid)


class LineEndpointSCCPAssociatedEvent(TenantEvent):
    name = 'line_endpoint_sccp_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[uuid]}.updated'
    )

    def __init__(self, line, sccp, tenant_uuid):
        content = {'line': line, 'endpoint_sccp': sccp}
        super(LineEndpointSCCPAssociatedEvent, self).__init__(content, tenant_uuid)


class LineEndpointSCCPDissociatedEvent(TenantEvent):
    name = 'line_endpoint_sccp_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[uuid]}.deleted'
    )

    def __init__(self, line, sccp, tenant_uuid):
        content = {'line': line, 'endpoint_sccp': sccp}
        super(LineEndpointSCCPDissociatedEvent, self).__init__(content, tenant_uuid)


class LineEndpointCustomAssociatedEvent(TenantEvent):
    name = 'line_endpoint_custom_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_custom[uuid]}.updated'
    )

    def __init__(self, line, custom, tenant_uuid):
        content = {'line': line, 'endpoint_custom': custom}
        super(LineEndpointCustomAssociatedEvent, self).__init__(content, tenant_uuid)


class LineEndpointCustomDissociatedEvent(TenantEvent):
    name = 'line_endpoint_custom_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[uuid]}.deleted'
    )

    def __init__(self, line, custom, tenant_uuid):
        content = {'line': line, 'endpoint_custom': custom}
        super(LineEndpointCustomDissociatedEvent, self).__init__(content, tenant_uuid)
