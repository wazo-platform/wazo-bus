# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import (
    LineDict,
    LineEndpointCustomDict,
    LineEndpointSCCPDict,
    LineEndpointSIPDict,
)


class LineEndpointSIPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sip_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.updated'
    )

    def __init__(
        self,
        line: LineDict,
        sip: LineEndpointSIPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_sip': sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSIPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sip_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sip.{endpoint_sip[uuid]}.deleted'
    )

    def __init__(
        self,
        line: LineDict,
        sip: LineEndpointSIPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_sip': sip}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sccp_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.updated'
    )

    def __init__(
        self,
        line: LineDict,
        sccp: LineEndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_sccp': sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointSCCPDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_sccp_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.sccp.{endpoint_sccp[id]}.deleted'
    )

    def __init__(
        self,
        line: LineDict,
        sccp: LineEndpointSCCPDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_sccp': sccp}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_custom_associated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.updated'
    )

    def __init__(
        self,
        line: LineDict,
        custom: LineEndpointCustomDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_custom': custom}
        super().__init__(content, tenant_uuid)


class LineEndpointCustomDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_endpoint_custom_dissociated'
    routing_key_fmt = (
        'config.lines.{line[id]}.endpoints.custom.{endpoint_custom[id]}.deleted'
    )

    def __init__(
        self,
        line: LineDict,
        custom: LineEndpointCustomDict,
        tenant_uuid: UUIDStr,
    ):
        content = {'line': line, 'endpoint_custom': custom}
        super().__init__(content, tenant_uuid)
