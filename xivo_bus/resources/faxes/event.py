# Copyright 2019-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent, UserEvent


class FaxOutboundCreatedEvent(TenantEvent):
    service = 'calld'
    name = 'fax_outbound_created'
    routing_key_fmt = 'faxes.outbound.created'

    def __init__(self, fax_schema, tenant_uuid):
        super().__init__(fax_schema, tenant_uuid)


class FaxOutboundSucceededEvent(TenantEvent):
    service = 'calld'
    name = 'fax_outbound_succeeded'
    routing_key_fmt = 'faxes.outbound.{id}.succeeded'

    def __init__(self, fax_schema, tenant_uuid):
        super().__init__(fax_schema, tenant_uuid)


class FaxOutboundFailedEvent(TenantEvent):
    service = 'calld'
    name = 'fax_outbound_failed'
    routing_key_fmt = 'faxes.outbound.{id}.failed'

    def __init__(self, fax_schema, tenant_uuid):
        super().__init__(fax_schema, tenant_uuid)


class FaxOutboundUserCreatedEvent(UserEvent):
    service = 'calld'
    name = 'fax_outbound_user_created'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.created'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super().__init__(fax_schema, tenant_uuid, user_uuid)


class FaxOutboundUserSucceededEvent(UserEvent):
    service = 'calld'
    name = 'fax_outbound_user_succeeded'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.succeeded'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super().__init__(fax_schema, tenant_uuid, user_uuid)


class FaxOutboundUserFailedEvent(UserEvent):
    service = 'calld'
    name = 'fax_outbound_user_failed'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.failed'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super().__init__(fax_schema, tenant_uuid, user_uuid)
