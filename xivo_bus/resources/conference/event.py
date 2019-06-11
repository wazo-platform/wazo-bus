# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent, ResourceConfigEvent


class EditConferenceEvent(ResourceConfigEvent):
    name = 'conference_edited'
    routing_key = 'config.conferences.edited'


class CreateConferenceEvent(ResourceConfigEvent):
    name = 'conference_created'
    routing_key = 'config.conferences.created'


class DeleteConferenceEvent(ResourceConfigEvent):
    name = 'conference_deleted'
    routing_key = 'config.conferences.deleted'


class ParticipantJoinedConferenceEvent(BaseEvent):
    name = 'conference_participant_joined'
    routing_key_fmt = 'conferences.{conference_id}.participants.joined'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantJoinedConferenceEvent, self).__init__()


class ParticipantLeftConferenceEvent(BaseEvent):
    name = 'conference_participant_left'
    routing_key_fmt = 'conferences.{conference_id}.participants.left'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantLeftConferenceEvent, self).__init__()


class UserParticipantJoinedConferenceEvent(BaseEvent):
    name = 'conference_user_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.joined'

    def __init__(self, conference_id, participant_dict, user_uuid=None):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(UserParticipantJoinedConferenceEvent, self).__init__()
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = 'events.{}'.format(self.routing_key)


class UserParticipantLeftConferenceEvent(BaseEvent):
    name = 'conference_user_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.participants.left'

    def __init__(self, conference_id, participant_dict, user_uuid=None):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(UserParticipantLeftConferenceEvent, self).__init__()
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = 'events.{}'.format(self.routing_key)


class ParticipantMutedConferenceEvent(BaseEvent):
    name = 'conference_participant_muted'
    routing_key_fmt = 'conferences.{conference_id}.participants.mute'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantMutedConferenceEvent, self).__init__()


class ParticipantUnmutedConferenceEvent(BaseEvent):
    name = 'conference_participant_unmuted'
    routing_key_fmt = 'conferences.{conference_id}.participants.mute'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantUnmutedConferenceEvent, self).__init__()


class RecordStartedConferenceEvent(BaseEvent):
    name = 'conference_record_started'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id):
        self._body = {'id': conference_id}
        super(RecordStartedConferenceEvent, self).__init__()


class RecordStoppedConferenceEvent(BaseEvent):
    name = 'conference_record_stopped'
    routing_key_fmt = 'conferences.{id}.record'

    def __init__(self, conference_id):
        self._body = {'id': conference_id}
        super(RecordStoppedConferenceEvent, self).__init__()


class ParticipantTalkStartedConferenceEvent(BaseEvent):
    name = 'conference_participant_talk_started'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantTalkStartedConferenceEvent, self).__init__()


class ParticipantTalkStoppedConferenceEvent(BaseEvent):
    name = 'conference_participant_talk_stopped'
    routing_key_fmt = 'conferences.{conference_id}.participants.talk'

    def __init__(self, conference_id, participant_dict):
        self._body = {'conference_id': conference_id}
        self._body.update(participant_dict)
        super(ParticipantTalkStoppedConferenceEvent, self).__init__()
