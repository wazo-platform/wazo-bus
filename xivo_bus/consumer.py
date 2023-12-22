# Copyright 2020-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import Any

from .base import Base
from .mixins import (
    ConsumerMixin,
    SubscribeExchangeDict,
    ThreadableMixin,
    WazoEventMixin,
)


class BusConsumer(WazoEventMixin, ThreadableMixin, ConsumerMixin, Base):  # type: ignore[misc]
    def __init__(
        self,
        name: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        subscribe: SubscribeExchangeDict | None = None,
        **kwargs: Any,
    ):
        super().__init__(
            name=name,
            username=username,
            password=password,
            host=host,
            port=port,
            exchange_name=exchange_name,
            exchange_type=exchange_type,
            subscribe=subscribe,
            **kwargs,
        )
