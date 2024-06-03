# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import TenantEvent
from ..common.types import UUIDStr
from .types import ParkedCallDict, ParkedCallTimedOutDict, UnparkedCallDict


class CallParkedEvent(TenantEvent):
    service = 'calld'
    name = 'call_parked'
    routing_key_fmt = 'parkings.{parking_id}.calls.updated'
    required_acl_fmt = 'events.parkings.{parking_id}.calls.updated'

    def __init__(self, parked_call: ParkedCallDict, tenant_uuid: UUIDStr):
        super().__init__(parked_call, tenant_uuid)


class CallUnparkedEvent(TenantEvent):
    service = 'calld'
    name = 'call_unparked'
    routing_key_fmt = 'parkings.{parking_id}.calls.updated'
    required_acl_fmt = 'events.parkings.{parking_id}.calls.updated'

    def __init__(self, unparked_call: UnparkedCallDict, tenant_uuid: str):
        super().__init__(unparked_call, tenant_uuid)


class ParkedCallHungupEvent(TenantEvent):
    service = 'calld'
    name = 'parked_call_hungup'
    routing_key_fmt = 'parkings.{parking_id}.calls.updated'
    required_acl_fmt = 'events.parkings.{parking_id}.calls.updated'

    def __init__(self, parked_call: ParkedCallDict, tenant_uuid: str):
        super().__init__(parked_call, tenant_uuid)


class ParkedCallTimedOutEvent(TenantEvent):
    service = 'calld'
    name = 'parked_call_timed_out'
    routing_key_fmt = 'parkings.{parking_id}.calls.updated'
    required_acl_fmt = 'events.parkings.{parking_id}.calls.updated'

    def __init__(self, parked_call: ParkedCallTimedOutDict, tenant_uuid: str):
        super().__init__(parked_call, tenant_uuid)
