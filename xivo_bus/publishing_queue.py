# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from queue import Queue, Empty

logger = logging.getLogger(__name__)


class PublishingQueue:
    def __init__(self, publisher_factory):
        self._publish = None
        self._publisher_factory = publisher_factory
        self._queue = Queue()
        self._running = False
        self._should_stop = False
        self._flushing = False

    def run(self):
        self._running = True

        while not self._should_stop or self._flushing:
            try:
                payload, headers, routing_key, kwargs = self._queue.get(timeout=0.1)
            except Empty:
                self._flushing = False
                continue

            if not self._publish:
                self._publish = self._publisher_factory()
                if hasattr(self._publish, 'publish'):
                    self._publish = self._publish.publish
            try:
                self._publish(
                    payload, headers=headers, routing_key=routing_key, **kwargs
                )
            except Exception as e:
                logger.exception('Error while publishing: %s', e)

        self._running = False
        self._should_stop = False

    def publish(self, payload, headers=None, routing_key=None, **kwargs):
        headers = headers or {}
        self._queue.put((payload, headers, routing_key, kwargs))

    def stop(self):
        if self._running:
            self._should_stop = True

    def flush_and_stop(self):
        if self._running:
            self._should_stop = True
            self._flushing = True
