# -*- coding: utf-8 -*-

# Copyright (C) 2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class IncallExtensionConfigEvent(object):

    def __init__(self, incall_id, extension_id):
        self.incall_id = incall_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'incall_id': self.incall_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['incall_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.incall_id == other.incall_id and
                self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class IncallExtensionAssociatedEvent(IncallExtensionConfigEvent):
    name = 'incall_extension_associated'
    routing_key = 'config.incalls.extensions.updated'


class IncallExtensionDissociatedEvent(IncallExtensionConfigEvent):
    name = 'incall_extension_dissociated'
    routing_key = 'config.incalls.extensions.deleted'
