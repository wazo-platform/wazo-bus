# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import UserEvent


class UserVoicemailAssociatedEvent(UserEvent):
    name = 'user_voicemail_associated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.updated'

    def __init__(self, voicemail_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': int(voicemail_id),
        }
        super(UserVoicemailAssociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class UserVoicemailDissociatedEvent(UserEvent):
    name = 'user_voicemail_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.deleted'

    def __init__(self, voicemail_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': user_uuid,
            'voicemail_id': int(voicemail_id),
        }
        super(UserVoicemailDissociatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
