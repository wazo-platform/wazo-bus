# Copyright 2021-2025 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, NamedTuple, Protocol, Self

from kombu import Exchange
from kombu.utils.url import as_url

from .resources.common.abstract import EventProtocol


class ConnectionParams(NamedTuple):
    user: str
    password: str
    host: str
    port: int


class BaseProtocol(Protocol):
    _name: str
    _logger: logging.Logger
    _connection_params: ConnectionParams
    _exchange: Exchange

    def __init__(
        self,
        name: str | None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        **kwargs: Any,
    ):
        ...

    @property
    def url(self) -> str:
        ...

    @property
    def log(self) -> logging.Logger:
        ...

    @property
    def is_running(self) -> bool:
        ...

    def _marshal(
        self,
        event: EventProtocol,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, dict | None, str | None]:
        ...

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        ...


class Base(BaseProtocol):
    '''Base class for publishers/consumers (to be extended by mixins)'''

    def __init__(
        self,
        name: str | None = None,
        username: str = 'guest',
        password: str = 'guest',
        host: str = 'localhost',
        port: int = 5672,
        exchange_name: str = '',
        exchange_type: str = '',
        exchange_durable: bool = True,
        exchange_kwargs: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        self._name = name or type(self).__name__
        self._logger = logging.getLogger(type(self).__name__)
        self._connection_params = ConnectionParams(username, password, host, port)
        self._exchange = Exchange(
            name=exchange_name,
            type=exchange_type,
            durable=exchange_durable,
            **(exchange_kwargs or {}),
        )

    @property
    def url(self) -> str:
        return as_url('amqp', **self._connection_params._asdict())

    @property
    def log(self) -> logging.Logger:
        return self._logger

    @property
    def is_running(self) -> bool:
        return True

    def _marshal(
        self,
        event: EventProtocol,
        headers: dict | None,
        payload: dict | None,
        routing_key: str | None = None,
    ) -> tuple[dict | None, dict | None, str | None]:
        return headers, payload, routing_key

    def _unmarshal(
        self, event_name: str, headers: dict, payload: dict
    ) -> tuple[dict, dict]:
        return headers, payload
