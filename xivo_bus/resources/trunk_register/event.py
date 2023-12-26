# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import TenantEvent


class TrunkRegisterIAXAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_register_iax_associated'
    routing_key_fmt = 'config.trunks.registers.iax.updated'

    def __init__(self, trunk_id: int, register_id: int, tenant_uuid: str):
        content = {'trunk_id': trunk_id, 'register_id': register_id}
        super().__init__(content, tenant_uuid)


class TrunkRegisterIAXDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'trunk_register_iax_dissociated'
    routing_key_fmt = 'config.trunks.registers.iax.deleted'

    def __init__(self, trunk_id: int, register_id: int, tenant_uuid: str):
        content = {
            'trunk_id': trunk_id,
            'register_id': register_id,
        }
        super().__init__(content, tenant_uuid)
