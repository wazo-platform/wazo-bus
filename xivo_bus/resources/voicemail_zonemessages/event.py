# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class EditVoicemailZoneMessagesEvent(object):
    name = 'voicemail_zonemessages_edited'
    routing_key = 'config.voicemail_zonemessages.edited'

    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, msg):
        return cls()

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other
