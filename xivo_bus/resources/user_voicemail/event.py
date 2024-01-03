# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import UserEvent


class UserVoicemailAssociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_voicemail_associated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.updated'

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': int(voicemail_id),
        }
        super().__init__(content, tenant_uuid, user_uuid)


class UserVoicemailDissociatedEvent(UserEvent):
    service = 'confd'
    name = 'user_voicemail_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.deleted'

    def __init__(
        self,
        voicemail_id: int,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
        user_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {
            'user_uuid': user_uuid,
            'voicemail_id': int(voicemail_id),
        }
        super().__init__(content, tenant_uuid, user_uuid)
