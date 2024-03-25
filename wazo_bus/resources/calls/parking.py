# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import TenantEvent
from ..common.types import UUIDStr


class CallParkedEvent(TenantEvent):
    service = 'calld'
    name = 'call_parked'
    routing_key_fmt = 'calls.park.created'
    required_acl_fmt = 'events.calls.{call_id}'

    def __init__(
        self,
        call_id: str,
        parking_id: int,
        slot: str,
        timeout_at: str | None,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_id': call_id,
            'parking_id': parking_id,
            'slot': slot,
            'timeout_at': timeout_at,
        }
        super().__init__(content, tenant_uuid)


class CallUnparkedEvent(TenantEvent):
    service = 'calld'
    name = 'call_unparked'
    routing_key_fmt = 'calls.park.deleted'
    required_acl_fmt = 'events.calls.{call_id}'

    def __init__(
        self,
        call_id: str,
        parking_id: int,
        slot: str,
        retriever_call_id: str,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_id': call_id,
            'parking_id': parking_id,
            'slot': slot,
            'retriever_call_id': retriever_call_id,
        }
        super().__init__(content, tenant_uuid)


class ParkedCallHungupEvent(TenantEvent):
    service = 'calld'
    name = 'parked_call_hungup'
    routing_key_fmt = 'calls.park.deleted'
    required_acl_fmt = 'events.calls.{call_id}'

    def __init__(
        self,
        call_id: str,
        parking_id: int,
        slot: str,
        parked_since: str,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_id': call_id,
            'parking_id': parking_id,
            'slot': slot,
            'parked_since': parked_since,
        }
        super().__init__(content, tenant_uuid)


class ParkedCallTimedOutEvent(TenantEvent):
    service = 'calld'
    name = 'parked_call_timed_out'
    routing_key_fmt = 'calls.park.deleted'
    required_acl_fmt = 'events.calls.{call_id}'

    def __init__(
        self,
        call_id: str,
        parking_id: int,
        dialed_extension: str | None,
        parked_since: str,
        tenant_uuid: UUIDStr,
    ):
        content = {
            'call_id': call_id,
            'parking_id': parking_id,
            'dialed_extension': dialed_extension,
            'parked_since': parked_since,
        }
        super().__init__(content, tenant_uuid)
