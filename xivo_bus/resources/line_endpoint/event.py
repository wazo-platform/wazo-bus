# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class LineEndpointSIPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sip_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated'
    )

    def __init__(self, line, sip, tenant_uuid):
        content = {'line': line, 'endpoint_sip': sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSIPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sip_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted'
    )

    def __init__(self, line, sip, tenant_uuid):
        content = {'line': line, 'endpoint_sip': sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sccp_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.updated'
    )

    def __init__(self, line, sccp, tenant_uuid):
        content = {'line': line, 'endpoint_sccp': sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sccp_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.deleted'
    )

    def __init__(self, line, sccp, tenant_uuid):
        content = {'line': line, 'endpoint_sccp': sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_custom_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.updated'
    )

    def __init__(self, line, custom, tenant_uuid):
        content = {'line': line, 'endpoint_custom': custom}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_custom_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'
    )

    def __init__(self, line, custom, tenant_uuid):
        content = {'line': line, 'endpoint_custom': custom}
        super().__init__(content, tenant_uuid)
