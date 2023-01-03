# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent, MultiUserEvent


class _ConferenceMixin(object):
    def __init__(self, content, conference_id, *args):
        super(_ConferenceMixin, self).__init__(content, *args)
        if not conference_id:
            raise ValueError('conference_id must have a value')
        self.conference_id = conference_id


class ConferenceCreatedEvent(_ConferenceMixin, TenantEvent):
    service = 'confd'
    name = 'conference_created'
    routing_key_fmt = 'config.conferences.created'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceCreatedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceDeletedEvent(_ConferenceMixin, TenantEvent):
    service = 'confd'
    name = 'conference_deleted'
    routing_key_fmt = 'config.conferences.deleted'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceDeletedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceEditedEvent(_ConferenceMixin, TenantEvent):
    service = 'confd'
    name = 'conference_edited'
    routing_key_fmt = 'config.conferences.edited'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceEditedEvent, self).__init__(content, conference_id, tenant_uuid)


class ConferenceRecordStartedEvent(_ConferenceMixin, TenantEvent):
    service = 'calld'
    name = 'conference_record_started'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceRecordStartedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceRecordStoppedEvent(_ConferenceMixin, TenantEvent):
    service = 'calld'
    name = 'conference_record_stopped'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceRecordStoppedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceParticipantJoinedEvent(_ConferenceMixin, MultiUserEvent):
    service = 'calld'
    name = 'conference_participant_joined'
    routing_key_fmt = 'conferences.{conference_id}.participants.joined'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuids):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantJoinedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuids
        )


class ConferenceParticipantLeftEvent(_ConferenceMixin, MultiUserEvent):
    service = 'calld'
    name = 'conference_participant_left'
    routing_key_fmt = 'conferences.{conference_id}.participants.left'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuids):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantLeftEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuids
        )


class ConferenceParticipantMutedEvent(_ConferenceMixin, TenantEvent):
    service = 'calld'
    name = 'conference_participant_muted'
    routing_key_fmt = 'conferences.{conference_id}.participants.mute'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantMutedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceParticipantUnmutedEvent(_ConferenceMixin, TenantEvent):
    service = 'calld'
    name = 'conference_participant_unmuted'
    routing_key_fmt = 'conferences.{conference_id}.particpants.mute'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantUnmutedEvent, self).__init__(
            content, conference_id, tenant_uuid
        )


class ConferenceParticipantTalkStartedEvent(_ConferenceMixin, MultiUserEvent):
    service = 'calld'
    name = 'conference_participant_talk_started'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuids):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantTalkStartedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuids
        )


class ConferenceParticipantTalkStoppedEvent(_ConferenceMixin, MultiUserEvent):
    service = 'calld'
    name = 'conference_participant_talk_stopped'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuids):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceParticipantTalkStoppedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuids
        )


class ConferenceUserParticipantJoinedEvent(_ConferenceMixin, UserEvent):
    service = 'calld'
    name = 'conference_user_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.joined'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceUserParticipantJoinedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantLeftEvent(_ConferenceMixin, UserEvent):
    service = 'calld'
    name = 'conference_user_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.left'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceUserParticipantLeftEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantTalkStartedEvent(_ConferenceMixin, UserEvent):
    service = 'calld'
    name = 'conference_user_participant_talk_started'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceUserParticipantTalkStartedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantTalkStoppedEvent(_ConferenceMixin, UserEvent):
    service = 'calld'
    name = 'conference_user_participant_talk_stopped'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = dict(participant, conference_id=conference_id)
        super(ConferenceUserParticipantTalkStoppedEvent, self).__init__(
            content, conference_id, tenant_uuid, user_uuid
        )
