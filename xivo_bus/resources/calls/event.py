# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import UserEvent
from .types import CallDict, RelocateDict, TransferDict


class CallCreatedEvent(UserEvent):
    service = 'calld'
    name = 'call_created'
    routing_key_fmt = 'calls.call.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call: CallDict, tenant_uuid: str, user_uuid: str):
        super().__init__(call, tenant_uuid, user_uuid)


class CallEndedEvent(UserEvent):
    service = 'calld'
    name = 'call_ended'
    routing_key_fmt = 'calls.call.ended'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call: CallDict, tenant_uuid: str, user_uuid: str):
        super().__init__(call, tenant_uuid, user_uuid)


class CallUpdatedEvent(UserEvent):
    service = 'calld'
    name = 'call_updated'
    routing_key_fmt = 'calls.call.updated'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call: CallDict, tenant_uuid: str, user_uuid: str):
        super().__init__(call, tenant_uuid, user_uuid)


class CallAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'call_answered'
    routing_key_fmt = 'calls.call.answered'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call: CallDict, tenant_uuid: str, user_uuid: str):
        super().__init__(call, tenant_uuid, user_uuid)


class CallDTMFEvent(UserEvent):
    service = 'calld'
    name = 'call_dtmf_created'
    routing_key_fmt = 'calls.dtmf.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(
        self, call_id: str, digit_number: str, tenant_uuid: str, user_uuid: str
    ):
        content = {
            'call_id': call_id,
            'digit': digit_number,
            'user_uuid': str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class CallHeldEvent(UserEvent):
    service = 'calld'
    name = 'call_held'
    routing_key_fmt = 'calls.hold.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_id: str, tenant_uuid: str, user_uuid: str):
        content = {
            'call_id': call_id,
            'user_uuid': str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class CallResumedEvent(UserEvent):
    service = 'calld'
    name = 'call_resumed'
    routing_key_fmt = 'calls.hold.deleted'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_id: str, tenant_uuid: str, user_uuid: str):
        content = {
            'call_id': call_id,
            'user_uuid': str(user_uuid),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class MissedCallEvent(UserEvent):
    service = 'calld'
    name = 'user_missed_call'
    routing_key_fmt = 'calls.missed'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call: CallDict, tenant_uuid: str, user_uuid: str):
        super().__init__(call, tenant_uuid, user_uuid)


class CallRelocateInitiatedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_initiated'
    routing_key_fmt = 'calls.relocate.created'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate: RelocateDict, tenant_uuid: str, user_uuid: str):
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'relocate_answered'
    routing_key_fmt = 'calls.relocate.edited'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate: RelocateDict, tenant_uuid: str, user_uuid: str):
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateCompletedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_completed'
    routing_key_fmt = 'calls.relocate.edited'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate: RelocateDict, tenant_uuid: str, user_uuid: str):
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallRelocateEndedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_ended'
    routing_key_fmt = 'calls.relocate.deleted'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate: RelocateDict, tenant_uuid: str, user_uuid: str):
        super().__init__(relocate, tenant_uuid, user_uuid)


class CallTransferCreatedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_created'
    routing_key_fmt = 'calls.transfer.created'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferUpdatedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_updated'
    routing_key_fmt = 'calls.transfer.created'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'transfer_answered'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferCancelledEvent(UserEvent):
    service = 'calld'
    name = 'transfer_cancelled'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferCompletedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_completed'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferAbandonedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_abandoned'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)


class CallTransferEndedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_ended'
    routing_key_fmt = 'calls.transfer.deleted'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer: TransferDict, tenant_uuid: str, user_uuid: str):
        super().__init__(transfer, tenant_uuid, user_uuid)
