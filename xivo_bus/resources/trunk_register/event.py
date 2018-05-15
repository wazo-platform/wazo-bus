# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class TrunkRegisterConfigEvent(object):

    def __init__(self, trunk_id, register_id):
        self.trunk_id = trunk_id
        self.register_id = register_id

    def marshal(self):
        return {
            'trunk_id': self.trunk_id,
            'register_id': self.register_id,
        }

    @classmethod
    def unmarshal(cls, msg):
        return cls(
            msg['trunk_id'],
            msg['register_id'])

    def __eq__(self, other):
        return (self.trunk_id == other.trunk_id
                and self.register_id == other.register_id)

    def __ne__(self, other):
        return not self == other


class TrunkRegisterIAXAssociatedEvent(TrunkRegisterConfigEvent):
    name = 'trunk_register_iax_associated'
    routing_key = 'config.trunks.registers.iax.updated'


class TrunkRegisterIAXDissociatedEvent(TrunkRegisterConfigEvent):
    name = 'trunk_register_iax_dissociated'
    routing_key = 'config.trunks.registers.iax.deleted'


class TrunkRegisterSIPAssociatedEvent(TrunkRegisterConfigEvent):
    name = 'trunk_register_sip_associated'
    routing_key = 'config.trunks.registers.sip.updated'


class TrunkRegisterSIPDissociatedEvent(TrunkRegisterConfigEvent):
    name = 'trunk_register_sip_dissociated'
    routing_key = 'config.trunks.registers.sip.deleted'
