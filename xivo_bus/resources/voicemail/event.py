# -*- coding: utf-8 -*-
# Copyright 2013-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent


class VoicemailCreatedEvent(TenantEvent):
    name = 'voicemail_created'
    routing_key_fmt = 'config.voicemail.created'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailCreatedEvent, self).__init__(content, tenant_uuid)


class VoicemailDeletedEvent(TenantEvent):
    name = 'voicemail_deleted'
    routing_key_fmt = 'config.voicemail.deleted'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailDeletedEvent, self).__init__(content, tenant_uuid)


class VoicemailEditedEvent(TenantEvent):
    name = 'voicemail_edited'
    routing_key_fmt = 'config.voicemail.edited'

    def __init__(self, voicemail_id, tenant_uuid):
        content = {'id': int(voicemail_id)}
        super(VoicemailEditedEvent, self).__init__(content, tenant_uuid)


class UserVoicemailEditedEvent(UserEvent):
    name = 'user_voicemail_edited'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.edited'

    def __init__(self, voicemail_id, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
        }
        super(UserVoicemailEditedEvent, self).__init__(content, tenant_uuid, user_uuid)


class UserVoicemailMessageCreatedEvent(UserEvent):
    name = 'user_voicemail_message_created'
    routing_key_fmt = 'voicemails.messages.created'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(self, message_id, voicemail_id, message, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super(UserVoicemailMessageCreatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class UserVoicemailMessageUpdatedEvent(UserEvent):
    name = 'user_voicemail_message_updated'
    routing_key_fmt = 'voicemails.messages.updated'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(self, message_id, voicemail_id, message, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super(UserVoicemailMessageUpdatedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )


class UserVoicemailMessageDeletedEvent(UserEvent):
    name = 'user_voicemail_message_deleted'
    routing_key_fmt = 'voicemails.messages.deleted'
    required_acl_fmt = 'events.users.{user_uuid}.voicemails'

    def __init__(self, message_id, voicemail_id, message, tenant_uuid, user_uuid):
        content = {
            'user_uuid': str(user_uuid),
            'voicemail_id': voicemail_id,
            'message_id': message_id,
            'message': message,
        }
        super(UserVoicemailMessageDeletedEvent, self).__init__(
            content, tenant_uuid, user_uuid
        )
