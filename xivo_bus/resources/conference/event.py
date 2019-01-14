# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditConferenceEvent(ResourceConfigEvent):
    name = 'conference_edited'
    routing_key = 'config.conferences.edited'


class CreateConferenceEvent(ResourceConfigEvent):
    name = 'conference_created'
    routing_key = 'config.conferences.created'


class DeleteConferenceEvent(ResourceConfigEvent):
    name = 'conference_deleted'
    routing_key = 'config.conferences.deleted'


class ParticipantJoinedConferenceEvent(object):
    name = 'conference_participant_joined'

    def __init__(self, conference_id, participant_dict):
        self.conference_id = conference_id
        self.participant = participant_dict
        self.required_acl = 'events.conferences.{conference_id}.participants.joined'.format(conference_id=conference_id)
        self.routing_key = 'conferences.{conference_id}.participants.joined'.format(conference_id=conference_id)

    def marshal(self):
        result = dict()
        result.update(self.participant)
        result['conference_id'] = self.conference_id
        return result

    @classmethod
    def unmarshal(cls, msg):
        participant = dict(msg)
        conference_id = participant.pop('conference_id')
        return cls(conference_id=conference_id, participant=msg)


class ParticipantLeftConferenceEvent(object):
    name = 'conference_participant_left'

    def __init__(self, conference_id, participant_dict):
        self.conference_id = conference_id
        self.participant = participant_dict
        self.required_acl = 'events.conferences.{conference_id}.participants.left'.format(conference_id=conference_id)
        self.routing_key = 'conferences.{conference_id}.participants.left'.format(conference_id=conference_id)

    def marshal(self):
        result = dict()
        result.update(self.participant)
        result['conference_id'] = self.conference_id
        return result

    @classmethod
    def unmarshal(cls, msg):
        participant = dict(msg)
        conference_id = participant.pop('conference_id')
        return cls(conference_id=conference_id, participant=msg)
