# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from importlib import import_module
from threading import Lock
from collections import defaultdict, namedtuple

# from xivo_bus import BusConsumer, BusPublisherFailFast, BusPublisherLongLived
from xivo_bus.middlewares import Middleware


class MessageBroker(object):
    Handler = namedtuple('Handler', 'handler, headers, routing_key')

    def __init__(self):
        self._messages = defaultdict(list)
        self._handlers = defaultdict(list)
        self.lock = Lock()

    def _filter_headers(self, headers):
        headers = headers or {}
        return {k: v for k, v in headers.items() if not k.startswith('x-')}

    def enqueue(self, event, message):
        with self.lock:
            self._messages[event].append(message)

    def dequeue(self, event):
        with self.lock:
            return self._messages.pop(event, [])

    def bind_handler(self, event, handler, headers=None, routing_key=None):
        handler = self.Handler(handler, self._filter_headers(headers), routing_key)
        with self.lock:
            self._handlers[event].append(handler)

    def get_handlers(self, event):
        with self.lock:
            return self._handlers[event].copy()

    def unbind_handler(self, event, headers=None, routing_key=None):
        headers = self._filter_headers(headers)
        with self.lock:
            for idx, handler in enumerate(self._handlers[event]):
                if handler.headers == headers and handler.routing_key == routing_key:
                    self._handlers[event].pop(idx)
                    return handler.handler


class MiddlewareManager(object):
    def __init__(self):
        module = import_module('xivo_bus.middlewares')
        self._middlewares = {}

        for attr in dir(module):
            if attr.startswith('__') and attr.endswith('__'):
                continue

            obj = getattr(module, attr)
            if not isinstance(obj, Middleware) and not callable(obj):
                continue

            self._middlewares[attr] = getattr(module, attr)

    @property
    def all(self):
        return list(self._middlewares)

    def get(self, name, _default=None):
        try:
            return self._middlewares[name]
        except KeyError:
            pass
        return _default
