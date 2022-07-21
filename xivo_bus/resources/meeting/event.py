# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent, BaseEvent


class _MeetingTenantEvent(TenantEvent):
    def __init__(self, content, meeting_uuid, tenant_uuid):
        super(_MeetingTenantEvent, self).__init__(content, tenant_uuid)
        if meeting_uuid is None:
            raise ValueError('meeting_uuid must have a value')
        self.meeting_uuid = str(meeting_uuid)


class _MeetingUserEvent(UserEvent):
    def __init__(self, content, meeting_uuid, tenant_uuid, user_uuid):
        super(_MeetingUserEvent, self).__init__(content, tenant_uuid, user_uuid)
        if meeting_uuid is None:
            raise ValueError('meeting_uuid must have a value')
        self.meeting_uuid = str(meeting_uuid)


class MeetingCreatedEvent(_MeetingTenantEvent):
    name = 'meeting_created'
    routing_key_fmt = 'config.meetings.created'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingCreatedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingDeletedEvent(_MeetingTenantEvent):
    name = 'meeting_deleted'
    routing_key_fmt = 'config.meetings.deleted'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingDeletedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingUpdatedEvent(_MeetingTenantEvent):
    name = 'meeting_updated'
    routing_key_fmt = 'config.meetings.updated'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingUpdatedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingProgressEvent(_MeetingTenantEvent):
    name = 'meeting_progress'
    routing_key_fmt = 'config.meetings.progress'

    def __init__(self, meeting, status, tenant_uuid):
        content = dict(meeting)
        content['status'] = status
        super(MeetingProgressEvent, self).__init__(
            content, meeting['uuid'], tenant_uuid
        )


class MeetingUserProgress(_MeetingUserEvent):
    name = 'meeting_user_progress'
    routing_key_fmt = 'config.users.{user_uuid}.meetings.progress'

    def __init__(self, meeting, status, tenant_uuid, user_uuid):
        content = dict(meeting)
        content['status'] = status
        content['user_uuid'] = user_uuid
        super(MeetingUserProgress, self).__init__(
            content, meeting['uuid'], tenant_uuid, user_uuid
        )


class _BaseParticipantMeetingEvent(BaseEvent):
    def __init__(self, meeting_uuid, participant_dict):
        self._body = {'meeting_uuid': meeting_uuid}
        self._body.update(participant_dict)
        super(_BaseParticipantMeetingEvent, self).__init__()


class ParticipantJoinedMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_participant_joined'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.joined'

    def __init__(self, meeting_uuid, participant_dict):
        super(ParticipantJoinedMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )


class ParticipantLeftMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_participant_left'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.left'

    def __init__(self, meeting_uuid, participant_dict):
        super(ParticipantLeftMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )


class UserParticipantJoinedMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_user_participant_joined'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.joined'

    def __init__(self, meeting_uuid, participant_dict, user_uuid=None):
        super(UserParticipantJoinedMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = (
                'events.users.{user_uuid}.meetings.participants.joined'.format(
                    user_uuid=user_uuid
                )
            )


class UserParticipantLeftMeetingEvent(_BaseParticipantMeetingEvent):
    name = 'meeting_user_participant_left'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.left'

    def __init__(self, meeting_uuid, participant_dict, user_uuid=None):
        super(UserParticipantLeftMeetingEvent, self).__init__(
            meeting_uuid, participant_dict
        )
        if user_uuid:
            self.routing_key = self.routing_key_fmt.format(user_uuid=user_uuid)
            self.required_acl = (
                'events.users.{user_uuid}.meetings.participants.left'.format(
                    user_uuid=user_uuid
                )
            )


class _BaseMeetingAuthorizationEvent(BaseEvent):
    def __init__(self, meeting_authorization):
        self._body = meeting_authorization
        super(_BaseMeetingAuthorizationEvent, self).__init__()


class MeetingAuthorizationCreatedEvent(_MeetingTenantEvent):
    name = 'meeting_guest_authorization_created'
    routing_key_fmt = 'config.meeting_guest_authorizations.created'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationCreatedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingAuthorizationDeletedEvent(_MeetingTenantEvent):
    name = 'meeting_guest_authorization_deleted'
    routing_key_fmt = 'config.meeting_guest_authorizations.deleted'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationDeletedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingAuthorizationUpdatedEvent(_MeetingTenantEvent):
    name = 'meeting_guest_authorization_updated'
    routing_key_fmt = 'config.meeting_guest_authorizations.updated'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationUpdatedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingUserAuthorizationCreatedEvent(_MeetingUserEvent):
    name = 'meeting_user_guest_authorization_created'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.created'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        self.required_acl = (
            'events.users.{user_uuid}.meeting_guest_authorizations.created'.format(
                user_uuid=user_uuid
            )
        )
        content = dict(meeting_authorization)
        content['user_uuid'] = user_uuid
        super(MeetingUserAuthorizationCreatedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingUserAuthorizationDeletedEvent(_MeetingUserEvent):
    name = 'meeting_user_guest_authorization_deleted'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.deleted'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        self.required_acl = (
            'events.users.{user_uuid}.meeting_guest_authorizations.deleted'.format(
                user_uuid=user_uuid
            )
        )
        content = dict(meeting_authorization)
        content['user_uuid'] = user_uuid
        super(MeetingUserAuthorizationDeletedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingUserAuthorizationEditedEvent(_MeetingUserEvent):
    name = 'meeting_user_guest_authorization_updated'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.updated'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        self.required_acl = (
            'events.users.{user_uuid}.meeting_guest_authorizations.updated'.format(
                user_uuid=user_uuid
            )
        )
        content = dict(meeting_authorization)
        content['user_uuid'] = user_uuid
        super(MeetingUserAuthorizationEditedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )
