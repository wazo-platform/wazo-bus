# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class LineExtensionConfigEvent(object):
    routing_key = 'config.line_extension_association.{}'

    def __init__(self,
                 line_id,
                 extension_id):
        self.line_id = int(line_id)
        self.extension_id = int(extension_id)

    def marshal(self):
        return {
            'line_id': self.line_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['line_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.line_id == other.line_id
                and self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class LineExtensionAssociatedEvent(LineExtensionConfigEvent):
    name = 'line_extension_associated'
    routing_key = LineExtensionConfigEvent.routing_key.format('created')


class LineExtensionDissociatedEvent(LineExtensionConfigEvent):
    name = 'line_extension_dissociated'
    routing_key = LineExtensionConfigEvent.routing_key.format('deleted')
