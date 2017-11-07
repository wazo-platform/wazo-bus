# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class BaseRelocateEvent(object):

    def __init__(self, initiator_uuid, relocate_dict):
        self.relocate = relocate_dict
        self.required_acl = 'events.relocates.{}'.format(initiator_uuid)

    def marshal(self):
        return self.relocate

    @classmethod
    def unmarshal(cls, msg):
        return cls(None, msg)

    def __eq__(self, other):
        return self.relocate == other.relocate

    def __ne__(self, other):
        return self.relocate != other.relocate


class RelocateInitiatedEvent(BaseRelocateEvent):

    name = 'relocate_initiated'
    routing_key = 'calls.relocate.created'


class RelocateAnsweredEvent(BaseRelocateEvent):
    name = 'relocate_answered'
    routing_key = 'calls.relocate.edited'


class RelocateCompletedEvent(BaseRelocateEvent):
    name = 'relocate_completed'
    routing_key = 'calls.relocate.edited'


class RelocateEndedEvent(BaseRelocateEvent):
    name = 'relocate_ended'
    routing_key = 'calls.relocate.deleted'
