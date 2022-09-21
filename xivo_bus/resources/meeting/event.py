# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent


class _MeetingMixin(object):
    def __init__(self, content, meeting_uuid, *args):
        super(_MeetingMixin, self).__init__(content, *args)
        if meeting_uuid is None:
            raise ValueError('meeting_uuid must have a value')
        self.meeting_uuid = str(meeting_uuid)


class MeetingCreatedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_created'
    routing_key_fmt = 'config.meetings.created'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingCreatedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingDeletedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_deleted'
    routing_key_fmt = 'config.meetings.deleted'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingDeletedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingEditedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_updated'
    routing_key_fmt = 'config.meetings.updated'

    def __init__(self, meeting, tenant_uuid):
        super(MeetingEditedEvent, self).__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingProgressEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_progress'
    routing_key_fmt = 'config.meetings.progress'

    def __init__(self, meeting, status, tenant_uuid):
        content = dict(meeting)
        content['status'] = status
        super(MeetingProgressEvent, self).__init__(
            content, meeting['uuid'], tenant_uuid
        )


class MeetingUserProgressEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_progress'
    routing_key_fmt = 'config.users.{user_uuid}.meetings.progress'

    def __init__(self, meeting, status, tenant_uuid, user_uuid):
        content = dict(meeting)
        content['status'] = status
        content['user_uuid'] = user_uuid
        super(MeetingUserProgressEvent, self).__init__(
            content, meeting['uuid'], tenant_uuid, user_uuid
        )


class MeetingParticipantJoinedEvent(_MeetingMixin, TenantEvent):
    service = 'calld'
    name = 'meeting_participant_joined'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.joined'

    def __init__(self, participant_data, meeting_uuid, tenant_uuid):
        content = dict(participant_data, meeting_uuid=meeting_uuid)
        super(MeetingParticipantJoinedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid
        )


class MeetingParticipantLeftEvent(_MeetingMixin, TenantEvent):
    service = 'calld'
    name = 'meeting_participant_left'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.left'

    def __init__(self, participant_data, meeting_uuid, tenant_uuid):
        content = dict(participant_data, meeting_uuid=meeting_uuid)
        super(MeetingParticipantLeftEvent, self).__init__(
            content, meeting_uuid, tenant_uuid
        )


class MeetingUserParticipantJoinedEvent(_MeetingMixin, UserEvent):
    service = 'calld'
    name = 'meeting_user_participant_joined'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.joined'
    required_acl_fmt = 'events.users.{user_uuid}.meetings.participants.joined'

    def __init__(self, participant_data, meeting_uuid, tenant_uuid, user_uuid):
        content = dict(participant_data, meeting_uuid=meeting_uuid)
        super(MeetingUserParticipantJoinedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingUserParticipantLeftEvent(_MeetingMixin, UserEvent):
    service = 'calld'
    name = 'meeting_user_participant_left'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.left'
    required_acl_fmt = 'events.users.{user_uuid}.meetings.participants.left'

    def __init__(self, participant_data, meeting_uuid, tenant_uuid, user_uuid):
        content = dict(participant_data, meeting_uuid=meeting_uuid)
        super(MeetingUserParticipantLeftEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingAuthorizationCreatedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_created'
    routing_key_fmt = 'config.meeting_guest_authorizations.created'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationCreatedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingAuthorizationDeletedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_deleted'
    routing_key_fmt = 'config.meeting_guest_authorizations.deleted'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationDeletedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingAuthorizationEditedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_updated'
    routing_key_fmt = 'config.meeting_guest_authorizations.updated'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid):
        super(MeetingAuthorizationEditedEvent, self).__init__(
            meeting_authorization, meeting_uuid, tenant_uuid
        )


class MeetingUserAuthorizationCreatedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_created'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.created'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.created'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super(MeetingUserAuthorizationCreatedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingUserAuthorizationDeletedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_deleted'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.deleted'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.deleted'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super(MeetingUserAuthorizationDeletedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )


class MeetingUserAuthorizationEditedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_updated'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.updated'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.updated'

    def __init__(self, meeting_authorization, meeting_uuid, tenant_uuid, user_uuid):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super(MeetingUserAuthorizationEditedEvent, self).__init__(
            content, meeting_uuid, tenant_uuid, user_uuid
        )
