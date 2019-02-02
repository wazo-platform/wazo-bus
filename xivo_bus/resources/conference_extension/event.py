# -*- coding: utf-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class ConferenceExtensionConfigEvent(object):

    def __init__(self, conference_id, extension_id):
        self.conference_id = conference_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'conference_id': self.conference_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['conference_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.conference_id == other.conference_id
                and self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class ConferenceExtensionAssociatedEvent(ConferenceExtensionConfigEvent):
    name = 'conference_extension_associated'
    routing_key = 'config.conferences.extensions.updated'


class ConferenceExtensionDissociatedEvent(ConferenceExtensionConfigEvent):
    name = 'conference_extension_dissociated'
    routing_key = 'config.conferences.extensions.deleted'
