# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
from collections.abc import Callable
from contextlib import AbstractContextManager

from amqp.exceptions import NotFound
from kombu import Exchange
from kombu import binding as Binding
from kombu.transport.base import StdChannel

OpenChannelType = Callable[[], AbstractContextManager[StdChannel]]


class UpstreamBindings:
    '''
    Bindings from an upstream exchange to the consuming exchange, one per
    subscribed event name. Not thread-safe: the owner serializes the calls.
    '''

    def __init__(self, exchange_name: str | None, log: logging.Logger):
        self._exchange = Exchange(exchange_name, 'headers') if exchange_name else None
        self._log = log
        self._binding_by_event: dict[str, Binding] = {}
        self._live: set[Binding] = set()
        self._last_error: str | None = None

    def add(self, event_name: str) -> None:
        if self._exchange is None or event_name in self._binding_by_event:
            return
        headers = {'name': event_name}
        self._binding_by_event[event_name] = Binding(
            self._exchange, None, headers, headers
        )

    def discard(self, event_name: str) -> None:
        self._binding_by_event.pop(event_name, None)

    def reset(self) -> None:
        self._live = set()

    def is_synced(self) -> bool:
        return self._live == set(self._binding_by_event.values())

    def changes(self) -> tuple[set[Binding], set[Binding]]:
        desired = set(self._binding_by_event.values())
        return desired - self._live, self._live - desired

    def apply(
        self,
        to_add: set[Binding],
        to_remove: set[Binding],
        destination: Exchange,
        open_channel: OpenChannelType,
        errors: tuple[type[Exception], ...],
    ) -> tuple[set[Binding], set[Binding]]:
        assert self._exchange is not None
        added: set[Binding] = set()
        removed: set[Binding] = set()

        # NOTE: removals first: a resubscribed event's binding has the same arguments
        try:
            for binding in to_remove:
                try:
                    with open_channel() as channel:
                        binding.unbind(destination, channel=channel)
                except NotFound:
                    # NOTE: a missing exchange holds no binding; NotFound closed the channel
                    pass
                removed.add(binding)
            if to_add:
                with open_channel() as channel:
                    destination.bind(channel).declare()
                    for binding in to_add:
                        binding.bind(destination, channel=channel)
                        added.add(binding)
        except errors as exc:
            log = self._log.debug
            if str(exc) != self._last_error:
                self._last_error = str(exc)
                log = self._log.warning
            log(
                'Failed to update bindings from upstream exchange \'%s\' '
                'to \'%s\', will retry: %s',
                self._exchange.name,
                destination.name,
                exc,
            )
        else:
            self._last_error = None

        return added, removed

    def commit(self, added: set[Binding], removed: set[Binding]) -> None:
        self._live |= added
        self._live -= removed
