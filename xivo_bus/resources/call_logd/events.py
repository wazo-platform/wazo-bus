# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from ..common.types import Format
from .types import CallLogExportDataDict


class CallLogExportCreatedEvent(TenantEvent):
    service = 'call_logd'
    name = 'call_logd_export_created'
    routing_key_fmt = 'call_logd.export.created'

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(export_data, tenant_uuid)


class CallLogExportUpdatedEvent(TenantEvent):
    service = 'call_logd'
    name = 'call_logd_export_updated'
    routing_key_fmt = 'call_logd.export.updated'

    def __init__(
        self,
        export_data: CallLogExportDataDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(export_data, tenant_uuid)


class CallLogRetentionUpdatedEvent(TenantEvent):
    service = 'call_logd'
    name = 'call_logd_retention_updated'
    routing_key_fmt = 'call_logd.retention.updated'

    def __init__(
        self,
        retention_data: CallLogExportDataDict,
        tenant_uuid: Annotated[str, Format('uuid')],
    ):
        super().__init__(retention_data, tenant_uuid)
