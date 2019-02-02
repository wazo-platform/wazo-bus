# -*- coding: utf-8 -*-
# Copyright 2016-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class OutcallExtensionConfigEvent(object):

    def __init__(self, outcall_id, extension_id):
        self.outcall_id = outcall_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'outcall_id': self.outcall_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['outcall_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.outcall_id == other.outcall_id
                and self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class OutcallExtensionAssociatedEvent(OutcallExtensionConfigEvent):
    name = 'outcall_extension_associated'
    routing_key = 'config.outcalls.extensions.updated'


class OutcallExtensionDissociatedEvent(OutcallExtensionConfigEvent):
    name = 'outcall_extension_dissociated'
    routing_key = 'config.outcalls.extensions.deleted'
