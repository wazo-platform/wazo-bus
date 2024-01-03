# Copyright 2021-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Annotated

from ..common.event import ServiceEvent


class RequestHandlersProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'request_handlers_progress'
    routing_key_fmt = 'sysconfd.request_handlers.{uuid}.{status}'

    def __init__(
        self,
        request_uuid: Annotated[str, {'format': 'uuid'}],
        request_context: dict | None,
        status: str,
    ):
        content = {
            'uuid': str(request_uuid),
            'status': status,
            'context': request_context,
        }
        super().__init__(content)


class AsteriskReloadProgressEvent(ServiceEvent):
    service = 'sysconfd'
    name = 'asterisk_reload_progress'
    routing_key_fmt = 'sysconfd.asterisk.reload.{uuid}.{status}'

    def __init__(
        self,
        uuid: Annotated[str, {'format': 'uuid'}],
        status: str,
        command: str,
        request_uuids: list[str],
    ):
        content = {
            'uuid': str(uuid),
            'status': status,
            'command': command,
            'request_uuids': request_uuids,
        }
        super().__init__(content)
