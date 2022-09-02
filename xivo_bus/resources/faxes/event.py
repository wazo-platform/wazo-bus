# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import TenantEvent, UserEvent


class FaxOutboundCreatedEvent(TenantEvent):
    name = 'fax_outbound_created'
    routing_key_fmt = 'faxes.outbound.created'

    def __init__(self, fax_schema, tenant_uuid):
        super(FaxOutboundCreatedEvent, self).__init__(fax_schema, tenant_uuid)


class FaxOutboundSucceededEvent(TenantEvent):
    name = 'fax_outbound_succeeded'
    routing_key_fmt = 'faxes.outbound.{id}.succeeded'

    def __init__(self, fax_schema, tenant_uuid):
        super(FaxOutboundSucceededEvent, self).__init__(fax_schema, tenant_uuid)


class FaxOutboundFailedEvent(TenantEvent):
    name = 'fax_outbound_failed'
    routing_key_fmt = 'faxes.outbound.{id}.failed'

    def __init__(self, fax_schema, tenant_uuid):
        super(FaxOutboundFailedEvent, self).__init__(fax_schema, tenant_uuid)


class FaxOutboundUserCreatedEvent(UserEvent):
    name = 'fax_outbound_user_created'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.created'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super(FaxOutboundUserCreatedEvent, self).__init__(
            fax_schema, tenant_uuid, user_uuid
        )


class FaxOutboundUserSucceededEvent(UserEvent):
    name = 'fax_outbound_user_succeeded'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.succeeded'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super(FaxOutboundUserSucceededEvent, self).__init__(
            fax_schema, tenant_uuid, user_uuid
        )


class FaxOutboundUserFailedEvent(UserEvent):
    name = 'fax_outbound_user_failed'
    routing_key_fmt = 'faxes.outbound.users.{user_uuid}.failed'

    def __init__(self, fax_schema, tenant_uuid, user_uuid):
        super(FaxOutboundUserFailedEvent, self).__init__(
            fax_schema, tenant_uuid, user_uuid
        )
