# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class BaseTransferEvent(object):

    def __init__(self, initiator_uuid, transfer_dict):
        self.transfer = transfer_dict
        self.required_acl = 'events.transfers.{}'.format(initiator_uuid)

    def marshal(self):
        return self.transfer

    @classmethod
    def unmarshal(cls, msg):
        return cls(None, msg)

    def __eq__(self, other):
        return self.transfer == other.transfer

    def __ne__(self, other):
        return self.transfer != other.transfer


class CreateTransferEvent(BaseTransferEvent):

    name = 'transfer_created'
    routing_key = 'calls.transfer.created'


class UpdateTransferEvent(BaseTransferEvent):

    name = 'transfer_updated'
    routing_key = 'calls.transfer.updated'


class AnswerTransferEvent(BaseTransferEvent):
    name = 'transfer_answered'
    routing_key = 'calls.transfer.edited'


class CancelTransferEvent(BaseTransferEvent):
    name = 'transfer_cancelled'
    routing_key = 'calls.transfer.edited'


class CompleteTransferEvent(BaseTransferEvent):
    name = 'transfer_completed'
    routing_key = 'calls.transfer.edited'


class AbandonTransferEvent(BaseTransferEvent):
    name = 'transfer_abandoned'
    routing_key = 'calls.transfer.edited'


class EndTransferEvent(BaseTransferEvent):
    name = 'transfer_ended'
    routing_key = 'calls.transfer.deleted'
