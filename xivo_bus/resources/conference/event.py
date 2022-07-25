# -*- coding: utf-8 -*-
# Copyright 2016-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent


class ConferenceCreatedEvent(TenantEvent):
    name = 'conference_created'
    routing_key_fmt = 'config.conferences.created'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceCreatedEvent, self).__init__(content, tenant_uuid)


class ConferenceDeletedEvent(TenantEvent):
    name = 'conference_deleted'
    routing_key_fmt = 'config.conferences.deleted'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceDeletedEvent, self).__init__(content, tenant_uuid)


class ConferenceEditedEvent(TenantEvent):
    name = 'conference_edited'
    routing_key_fmt = 'config.conferences.edited'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceEditedEvent, self).__init__(content, tenant_uuid)


class ConferenceRecordStartedEvent(TenantEvent):
    name = 'conference_record_started'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceRecordStartedEvent, self).__init__(content, tenant_uuid)


class ConferenceRecordStoppedEvent(TenantEvent):
    name = 'conference_record_stopped'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id, tenant_uuid):
        content = {'id': conference_id}
        super(ConferenceRecordStoppedEvent, self).__init__(content, tenant_uuid)


class ConferenceParticipantJoinedEvent(TenantEvent):
    name = 'conference_participant_joined'
    routing_key_fmt = 'conferences.{conference_id}.participants.joined'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantJoinedEvent, self).__init__(content, tenant_uuid)


class ConferenceParticipantLeftEvent(TenantEvent):
    name = 'conference_participant_left'
    routing_key_fmt = 'conferences.{conference_id}.participants.left'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantJoinedEvent, self).__init__(content, tenant_uuid)


class ConferenceParticipantMutedEvent(TenantEvent):
    name = 'conference_participant_muted'
    routing_key_fmt = 'conferences.{conference_id}.participants.mute'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantMutedEvent, self).__init__(content, tenant_uuid)


class ConferenceParticipantUnmutedEvent(TenantEvent):
    name = 'conference_participant_unmuted'
    routing_key_fmt = 'conferences.{conference_id}.particpants.mute'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantUnmutedEvent, self).__init__(content, tenant_uuid)


class ConferenceParticipantTalkStartedEvent(TenantEvent):
    name = 'conference_participant_talk_started'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantTalkStartedEvent, self).__init__(
            content, tenant_uuid
        )


class ConferenceParticipantTalkStoppedEvent(TenantEvent):
    name = 'conference_participant_talk_stopped'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceParticipantTalkStoppedEvent, self).__init__(
            content, tenant_uuid
        )


class ConferenceUserParticipantJoinedEvent(UserEvent):
    name = 'conference_user_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.joined'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceUserParticipantJoinedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantLeftEvent(UserEvent):
    name = 'conference_user_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.left'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceUserParticipantLeftEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantTalkStartedEvent(UserEvent):
    name = 'conference_user_participant_talk_started'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceUserParticipantTalkStartedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class ConferenceUserParticipantTalkStoppedEvent(UserEvent):
    name = 'conference_user_participant_talk_stopped'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.talk'

    def __init__(self, conference_id, participant, tenant_uuid, user_uuid):
        content = {'conference_id': conference_id}
        content.update(participant)
        super(ConferenceUserParticipantTalkStartedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
