# -*- coding: utf-8 -*-
# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import TenantEvent


class CallLogExportCreatedEvent(TenantEvent):
    name = 'call_logd_export_created'
    routing_key_fmt = 'call_logd.export.created'

    def __init__(self, export_data, tenant_uuid):
        super(CallLogExportCreatedEvent, self).__init__(export_data, tenant_uuid)


class CallLogExportUpdatedEvent(TenantEvent):
    name = 'call_logd_export_updated'
    routing_key_fmt = 'call_logd.export.updated'

    def __init__(self, export_data, tenant_uuid):
        super(CallLogExportUpdatedEvent, self).__init__(export_data, tenant_uuid)


class CallLogRetentionUpdatedEvent(TenantEvent):
    name = 'call_logd_retention_updated'
    routing_key_fmt = 'call_logd.retention.updated'

    def __init__(self, retention_data, tenant_uuid):
        super(CallLogRetentionUpdatedEvent, self).__init__(retention_data, tenant_uuid)
