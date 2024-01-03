# Copyright 2020-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import UserEvent
from ..common.types import Format


class AdhocConferenceCreatedEvent(UserEvent):
    name = 'conference_adhoc_created'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.created'
    service = 'calld'

    def __init__(
        self,
        conference_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'conference_id': conference_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceDeletedEvent(UserEvent):
    name = 'conference_adhoc_deleted'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.deleted'
    service = 'calld'

    def __init__(
        self,
        conference_id: int,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'conference_id': conference_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceParticipantJoinedEvent(UserEvent):
    name = 'conference_adhoc_participant_joined'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.joined'
    service = 'calld'

    def __init__(
        self,
        conference_id: int,
        call_id: str,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'conference_id': conference_id, 'call_id': call_id}
        super().__init__(content, tenant_uuid, user_uuid)


class AdhocConferenceParticipantLeftEvent(UserEvent):
    name = 'conference_adhoc_participant_left'
    routing_key_fmt = 'conferences.users.{user_uuid}.adhoc.participants.left'
    service = 'calld'

    def __init__(
        self,
        conference_id: int,
        call_id: str,
        tenant_uuid: Annotated[str, Format('uuid')],
        user_uuid: Annotated[str, Format('uuid')],
    ):
        content = {'conference_id': conference_id, 'call_id': call_id}
        super().__init__(content, tenant_uuid, user_uuid)
