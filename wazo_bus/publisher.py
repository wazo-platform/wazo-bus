# Copyright 2012-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from typing import Any

from .base import Base
from .mixins import PublisherMixin, QueuePublisherMixin, ThreadableMixin, WazoEventMixin

logger = logging.getLogger(__name__)


class BusPublisher(WazoEventMixin, PublisherMixin, Base):
    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        exchange_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            exchange_kwargs=exchange_kwargs,
            **kwargs,
        )


# Deprecated, thread should be avoided to respect WPEP-0004
class BusPublisherWithQueue(
    WazoEventMixin,
    ThreadableMixin,
    QueuePublisherMixin,
    Base,
):
    def __init__(
        self,
        name: str | None = None,
        service_uuid: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        exchange_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            service_uuid=service_uuid,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            exchange_kwargs=exchange_kwargs,
            **kwargs,
        )
