# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseUserVoicemailEvent(BaseEvent):

    def __init__(self, user_uuid, voicemail_id):
        self._body = {
            'user_uuid': user_uuid,
            'voicemail_id': int(voicemail_id),
        }
        super(_BaseUserVoicemailEvent, self).__init__()


class UserVoicemailAssociatedEvent(_BaseUserVoicemailEvent):

    name = 'voicemail_associated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.updated'


class UserVoicemailDissociatedEvent(_BaseUserVoicemailEvent):

    name = 'voicemail_dissociated'
    routing_key_fmt = 'config.users.{user_uuid}.voicemails.deleted'
