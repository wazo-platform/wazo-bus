# -*- coding: utf-8 -*-
# Copyright 2016-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import six

from six.moves import queue

logger = logging.getLogger(__name__)


class PublishingQueue(object):

    def __init__(self, publisher_factory):
        self._publish = None
        self._publisher_factory = publisher_factory
        self._queue = queue.Queue()
        self._running = False
        self._should_stop = False
        self._flushing = False

    def run(self):
        self._running = True

        while not self._should_stop or self._flushing:
            try:
                message, headers, kwargs = self._queue.get(timeout=0.1)
            except queue.Empty:
                self._flushing = False
                continue

            if not self._publish:
                self._publish = self._publisher_factory()
                if not six.callable(self._publish):
                    self._publish = self._publish.publish
            try:
                self._publish(message, headers=headers, **kwargs)
            except Exception as e:
                logger.exception('Error while publishing: %s', e)

        self._running = False
        self._should_stop = False

    def publish(self, event, headers=None, **kwargs):
        headers = headers or {}
        self._queue.put((event, headers, kwargs))

    def stop(self):
        if self._running:
            self._should_stop = True

    def flush_and_stop(self):
        if self._running:
            self._should_stop = True
            self._flushing = True
