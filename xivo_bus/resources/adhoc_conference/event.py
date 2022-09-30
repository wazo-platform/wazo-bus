# Copyright 2020-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class AdhocConferenceCreatedEvent(UserEvent):
    name = 'conference_adhoc_created'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.created'
    service = 'calld'

    def __init__(self, conference_id, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        super(AdhocConferenceCreatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class AdhocConferenceDeletedEvent(UserEvent):
    name = 'conference_adhoc_deleted'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.deleted'
    service = 'calld'

    def __init__(self, conference_id, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        super(AdhocConferenceDeletedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class AdhocConferenceParticipantJoinedEvent(UserEvent):
    name = 'conference_adhoc_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.joined'
    service = 'calld'

    def __init__(self, conference_id, call_id, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id, 'call_id': call_id}
        super(AdhocConferenceParticipantJoinedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class AdhocConferenceParticipantLeftEvent(UserEvent):
    name = 'conference_adhoc_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.left'
    service = 'calld'

    def __init__(self, conference_id, call_id, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id, 'call_id': call_id}
        super(AdhocConferenceParticipantLeftEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
