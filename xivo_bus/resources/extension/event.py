# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ExtensionConfigEvent(ResourceConfigEvent):
    routing_key = 'config.extension.{}'

    def __init__(self, extension_id, exten, context):
        self.id = int(extension_id)
        self.exten = exten
        self.context = context

    def marshal(self):
        return {
            'id': self.id,
            'exten': self.exten,
            'context': self.context
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(msg['id'], msg['exten'], msg['context'])


class EditExtensionEvent(ExtensionConfigEvent):
    name = 'extension_edited'
    routing_key = ExtensionConfigEvent.routing_key.format('edited')


class CreateExtensionEvent(ExtensionConfigEvent):
    name = 'extension_created'
    routing_key = ExtensionConfigEvent.routing_key.format('created')


class DeleteExtensionEvent(ExtensionConfigEvent):
    name = 'extension_deleted'
    routing_key = ExtensionConfigEvent.routing_key.format('deleted')
