# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class UserCtiProfileEditedEvent(BaseEvent):
    name = 'cti_profile_edited'
    routing_key_fmt = 'config.user_cti_profile_association.edited'

    def __init__(self, user_id, cti_profile_id, enabled):
        self._body = {
            'user_id': user_id,
            'cti_profile_id': cti_profile_id,
            'enabled': enabled
        }
        super(UserCtiProfileEditedEvent, self).__init__()
