# Copyright 2019-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Annotated

from ..common.event import TenantEvent
from .types import ApplicationDict, LineDict


class LineApplicationAssociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_associated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.updated'

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {'line': line, 'application': application}
        super().__init__(content, tenant_uuid)


class LineApplicationDissociatedEvent(TenantEvent):
    service = 'confd'
    name = 'line_application_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.deleted'

    def __init__(
        self,
        line: LineDict,
        application: ApplicationDict,
        tenant_uuid: Annotated[str, {'format': 'uuid'}],
    ):
        content = {'line': line, 'application': application}
        super().__init__(content, tenant_uuid)
