# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import UserEvent


class CallCreatedEvent(UserEvent):
    service = 'calld'
    name = 'call_created'
    routing_key_fmt = 'calls.call.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_data, tenant_uuid, user_uuid):
        super(CallCreatedEvent, self).__init__(call_data, tenant_uuid, user_uuid)


class CallEndedEvent(UserEvent):
    service = 'calld'
    name = 'call_ended'
    routing_key_fmt = 'calls.call.ended'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_data, tenant_uuid, user_uuid):
        super(CallEndedEvent, self).__init__(call_data, tenant_uuid, user_uuid)


class CallUpdatedEvent(UserEvent):
    service = 'calld'
    name = 'call_updated'
    routing_key_fmt = 'calls.call.updated'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_data, tenant_uuid, user_uuid):
        super(CallUpdatedEvent, self).__init__(call_data, tenant_uuid, user_uuid)


class CallAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'call_answered'
    routing_key_fmt = 'calls.call.answered'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_data, tenant_uuid, user_uuid):
        super(CallAnsweredEvent, self).__init__(call_data, tenant_uuid, user_uuid)


class CallDTMFEvent(UserEvent):
    service = 'calld'
    name = 'call_dtmf_created'
    routing_key_fmt = 'calls.dtmf.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_id, digit_number, tenant_uuid, user_uuid):
        content = {
            'call_id': call_id,
            'digit': digit_number,
            'user_uuid': str(user_uuid),
        }
        super(CallDTMFEvent, self).__init__(content, tenant_uuid, user_uuid)


class CallHeldEvent(UserEvent):
    service = 'calld'
    name = 'call_held'
    routing_key_fmt = 'calls.hold.created'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_id, tenant_uuid, user_uuid):
        content = {
            'call_id': call_id,
            'user_uuid': str(user_uuid),
        }
        super(CallHeldEvent, self).__init__(content, tenant_uuid, user_uuid)


class CallResumedEvent(UserEvent):
    service = 'calld'
    name = 'call_resumed'
    routing_key_fmt = 'calls.hold.deleted'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_id, tenant_uuid, user_uuid):
        content = {
            'call_id': call_id,
            'user_uuid': str(user_uuid),
        }
        super(CallResumedEvent, self).__init__(content, tenant_uuid, user_uuid)


class MissedCallEvent(UserEvent):
    service = 'calld'
    name = 'user_missed_call'
    routing_key_fmt = 'calls.missed'
    required_acl_fmt = 'events.calls.{user_uuid}'

    def __init__(self, call_schema, tenant_uuid, user_uuid):
        super(MissedCallEvent, self).__init__(call_schema, tenant_uuid, user_uuid)


class CallRelocateInitiatedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_initiated'
    routing_key_fmt = 'calls.relocate.created'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate_schema, tenant_uuid, user_uuid):
        super(CallRelocateInitiatedEvent, self).__init__(
            relocate_schema, tenant_uuid, user_uuid
        )


class CallRelocateAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'relocate_answered'
    routing_key_fmt = 'calls.relocate.edited'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate_schema, tenant_uuid, user_uuid):
        super(CallRelocateAnsweredEvent, self).__init__(
            relocate_schema, tenant_uuid, user_uuid
        )


class CallRelocateCompletedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_completed'
    routing_key_fmt = 'calls.relocate.edited'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate_schema, tenant_uuid, user_uuid):
        super(CallRelocateCompletedEvent, self).__init__(
            relocate_schema, tenant_uuid, user_uuid
        )


class CallRelocateEndedEvent(UserEvent):
    service = 'calld'
    name = 'relocate_ended'
    routing_key_fmt = 'calls.relocate.deleted'
    required_acl_fmt = 'events.relocates.{user_uuid}'

    def __init__(self, relocate_schema, tenant_uuid, user_uuid):
        super(CallRelocateEndedEvent, self).__init__(
            relocate_schema, tenant_uuid, user_uuid
        )


class CallTransferCreatedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_created'
    routing_key_fmt = 'calls.transfer.created'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferCreatedEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferUpdatedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_updated'
    routing_key_fmt = 'calls.transfer.created'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferUpdatedEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferAnsweredEvent(UserEvent):
    service = 'calld'
    name = 'transfer_answered'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferAnsweredEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferCancelledEvent(UserEvent):
    service = 'calld'
    name = 'transfer_cancelled'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferCancelledEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferCompletedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_completed'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferCompletedEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferAbandonedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_abandoned'
    routing_key_fmt = 'calls.transfer.edited'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferAbandonedEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )


class CallTransferEndedEvent(UserEvent):
    service = 'calld'
    name = 'transfer_ended'
    routing_key_fmt = 'calls.transfer.deleted'
    required_acl_fmt = 'events.transfers.{user_uuid}'

    def __init__(self, transfer_schema, tenant_uuid, user_uuid):
        super(CallTransferEndedEvent, self).__init__(
            transfer_schema, tenant_uuid, user_uuid
        )
