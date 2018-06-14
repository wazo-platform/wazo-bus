# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class QueueExtensionConfigEvent(object):

    def __init__(self, queue_id, extension_id):
        self.queue_id = queue_id
        self.extension_id = extension_id

    def marshal(self):
        return {
            'queue_id': self.queue_id,
            'extension_id': self.extension_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['queue_id'],
            msg['extension_id'])

    def __eq__(self, other):
        return (self.queue_id == other.queue_id
                and self.extension_id == other.extension_id)

    def __ne__(self, other):
        return not self == other


class QueueExtensionAssociatedEvent(QueueExtensionConfigEvent):
    name = 'queue_extension_associated'
    routing_key = 'config.queues.extensions.updated'


class QueueExtensionDissociatedEvent(QueueExtensionConfigEvent):
    name = 'queue_extension_dissociated'
    routing_key = 'config.queues.extensions.deleted'
