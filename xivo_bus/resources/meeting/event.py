# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..common.event import TenantEvent, UserEvent
from ..common.types import UUIDStr
from .types import MeetingAuthorizationDict, MeetingDict, MeetingParticipantDict


class _MeetingMixin:
    def __init__(
        self,
        content: Mapping,
        meeting_uuid: UUIDStr,
        *args: Any,
    ):
        super().__init__(content, *args)  # type: ignore[call-arg]
        if meeting_uuid is None:
            raise ValueError('meeting_uuid must have a value')
        self.meeting_uuid = str(meeting_uuid)


class MeetingCreatedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_created'
    routing_key_fmt = 'config.meetings.created'

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr):
        super().__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingDeletedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_deleted'
    routing_key_fmt = 'config.meetings.deleted'

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr):
        super().__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingEditedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_updated'
    routing_key_fmt = 'config.meetings.updated'

    def __init__(self, meeting: MeetingDict, tenant_uuid: UUIDStr):
        super().__init__(meeting, meeting['uuid'], tenant_uuid)


class MeetingProgressEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_progress'
    routing_key_fmt = 'config.meetings.progress'

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        tenant_uuid: UUIDStr,
    ):
        content = dict(meeting)
        content['status'] = status
        super().__init__(content, meeting['uuid'], tenant_uuid)


class MeetingUserProgressEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_progress'
    routing_key_fmt = 'config.users.{user_uuid}.meetings.progress'

    def __init__(
        self,
        meeting: MeetingDict,
        status: str,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(meeting)
        content['status'] = status
        content['user_uuid'] = user_uuid
        super().__init__(content, meeting['uuid'], tenant_uuid, user_uuid)


class MeetingParticipantJoinedEvent(_MeetingMixin, TenantEvent):
    service = 'calld'
    name = 'meeting_participant_joined'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.joined'

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid)


class MeetingParticipantLeftEvent(_MeetingMixin, TenantEvent):
    service = 'calld'
    name = 'meeting_participant_left'
    routing_key_fmt = 'meetings.{meeting_uuid}.participants.left'

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid)


class MeetingUserParticipantJoinedEvent(_MeetingMixin, UserEvent):
    service = 'calld'
    name = 'meeting_user_participant_joined'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.joined'
    required_acl_fmt = 'events.users.{user_uuid}.meetings.participants.joined'

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserParticipantLeftEvent(_MeetingMixin, UserEvent):
    service = 'calld'
    name = 'meeting_user_participant_left'
    routing_key_fmt = 'meetings.users.{user_uuid}.participants.left'
    required_acl_fmt = 'events.users.{user_uuid}.meetings.participants.left'

    def __init__(
        self,
        participant: MeetingParticipantDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(participant, meeting_uuid=meeting_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingAuthorizationCreatedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_created'
    routing_key_fmt = 'config.meeting_guest_authorizations.created'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingAuthorizationDeletedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_deleted'
    routing_key_fmt = 'config.meeting_guest_authorizations.deleted'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingAuthorizationEditedEvent(_MeetingMixin, TenantEvent):
    service = 'confd'
    name = 'meeting_guest_authorization_updated'
    routing_key_fmt = 'config.meeting_guest_authorizations.updated'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
    ):
        super().__init__(meeting_authorization, meeting_uuid, tenant_uuid)


class MeetingUserAuthorizationCreatedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_created'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.created'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.created'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserAuthorizationDeletedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_deleted'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.deleted'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.deleted'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)


class MeetingUserAuthorizationEditedEvent(_MeetingMixin, UserEvent):
    service = 'confd'
    name = 'meeting_user_guest_authorization_updated'
    routing_key_fmt = 'config.users.{user_uuid}.meeting_guest_authorizations.updated'
    required_acl_fmt = 'events.users.{user_uuid}.meeting_guest_authorizations.updated'

    def __init__(
        self,
        meeting_authorization: MeetingAuthorizationDict,
        meeting_uuid: UUIDStr,
        tenant_uuid: UUIDStr,
        user_uuid: UUIDStr,
    ):
        content = dict(meeting_authorization, user_uuid=user_uuid)
        super().__init__(content, meeting_uuid, tenant_uuid, user_uuid)
