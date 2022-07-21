# -*- coding: utf-8 -*-
# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, BaseEvent
from xivo.permission import escape as escape_acl
from xivo_bus.resources.common.routing_key import escape as escape_key


class SwitchboardEvent(TenantEvent):
    def __init__(self, content, switchboard_uuid, tenant_uuid):
        super(TenantEvent, self).__init__(content, tenant_uuid)
        if switchboard_uuid is None:
            raise ValueError('switchboard_uuid must have a value')
        self.switchboard_uuid = str(switchboard_uuid)


class SwitchboardCreatedEvent(SwitchboardEvent):
    name = 'switchboard_created'
    routing_key_fmt = 'config.switchboards.{uuid}.created'

    def __init__(self, switchboard, tenant_uuid):
        uuid = switchboard['uuid']
        self.required_acl = 'switchboards.{uuid}.created'.format(uuid=uuid)
        super(SwitchboardCreatedEvent, self).__init__(switchboard, uuid, tenant_uuid)


class SwitchboardDeletedEvent(SwitchboardEvent):
    name = 'switchboard_deleted'
    routing_key_fmt = 'config.switchboards.{uuid}.deleted'

    def __init__(self, switchboard, tenant_uuid):
        uuid = switchboard['uuid']
        self.required_acl = 'switchboards.{uuid}.deleted'.format(uuid=uuid)
        super(SwitchboardDeletedEvent, self).__init__(switchboard, uuid, tenant_uuid)


class SwitchboardEditedEvent(SwitchboardEvent):
    name = 'switchboard_edited'
    routing_key_fmt = 'config.switchboards.{uuid}.edited'

    def __init__(self, switchboard, tenant_uuid):
        uuid = switchboard['uuid']
        self.required_acl = 'switchboards.{uuid}.edited'.format(uuid=uuid)
        super(SwitchboardEditedEvent, self).__init__(switchboard, uuid, tenant_uuid)


class SwitchboardFallbackEditedEvent(SwitchboardEvent):
    name = 'switchboard_fallback_edited'
    routing_key_fmt = 'config.switchboards.fallbacks.edited'
    required_acl = 'switchboards.fallbacks.edited'

    def __init__(self, fallback, switchboard_uuid, tenant_uuid):
        super(SwitchboardFallbackEditedEvent, self).__init__(
            fallback, switchboard_uuid, tenant_uuid
        )


class _BaseSwitchboardEvent(BaseEvent):
    def __init__(self, body):
        self._body = body
        super(_BaseSwitchboardEvent, self).__init__()
        self.required_acl = self.required_acl_fmt.format(**body)


class EditSwitchboardFallbackEvent(_BaseSwitchboardEvent):
    name = 'switchboard_fallback_edited'
    routing_key_fmt = 'config.switchboards.fallbacks.edited'
    required_acl_fmt = 'switchboards.fallbacks.edited'


class SwitchboardQueuedCallsUpdatedEvent(_BaseSwitchboardEvent):
    name = 'switchboard_queued_calls_updated'
    routing_key_fmt = 'switchboards.{switchboard_uuid}.calls.queued.updated'
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.queued.updated'


class SwitchboardQueuedCallAnsweredEvent(_BaseSwitchboardEvent):
    name = 'switchboard_queued_call_answered'
    routing_key_fmt = 'switchboards.{uuid}.calls.queued.{call_id}.answer.updated'
    required_acl_fmt = (
        'events.switchboards.{uuid}.calls.queued.{call_id}.answer.updated'
    )

    def __init__(self, body):
        uuid = body['switchboard_uuid']
        call_id = body['queued_call_id']
        self._body = body

        self.routing_key = self.routing_key_fmt.format(
            uuid=uuid, call_id=escape_key(call_id)
        )
        self.required_acl = self.required_acl_fmt.format(
            uuid=uuid, call_id=escape_acl(call_id)
        )


class SwitchboardHeldCallsUpdatedEvent(_BaseSwitchboardEvent):
    name = 'switchboard_held_calls_updated'
    routing_key_fmt = 'switchboards.{switchboard_uuid}.calls.held.updated'
    required_acl_fmt = 'events.switchboards.{switchboard_uuid}.calls.held.updated'


class SwitchboardHeldCallAnsweredEvent(_BaseSwitchboardEvent):
    name = 'switchboard_held_call_answered'
    routing_key_fmt = 'switchboards.{uuid}.calls.held.{call_id}.answer.updated'
    required_acl_fmt = 'events.switchboards.{uuid}.calls.held.{call_id}.answer.updated'

    def __init__(self, body):
        uuid = body['switchboard_uuid']
        call_id = body['held_call_id']
        self._body = body

        self.routing_key = self.routing_key_fmt.format(
            uuid=uuid,
            call_id=escape_key(call_id),
        )
        self.required_acl = self.required_acl_fmt.format(
            uuid=uuid, call_id=escape_acl(call_id)
        )
