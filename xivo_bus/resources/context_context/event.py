# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class ContextContextConfigEvent(ResourceConfigEvent):

    def __init__(self, context_id, context_ids):
        self.context_id = context_id
        self.context_ids = context_ids

    def marshal(self):
        return {
            'context_id': self.context_id,
            'context_ids': self.context_ids,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['context_id'],
            msg['context_ids'])

    def __eq__(self, other):
        return (self.context_id == other.context_id
                and self.context_ids == other.context_ids)

    def __ne__(self, other):
        return not (self == other)


class ContextContextsAssociatedEvent(ContextContextConfigEvent):
    name = 'contexts_associated'
    routing_key = 'config.contexts.contexts.updated'
