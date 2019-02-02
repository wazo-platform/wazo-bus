# -*- coding: utf-8 -*-
# Copyright 2016-2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

from six.moves import queue

logger = logging.getLogger(__name__)


class PublishingQueue(object):

    def __init__(self, publisher_factory):
        self._publisher = None
        self._publisher_factory = publisher_factory
        self._queue = queue.Queue()
        self._running = False
        self._should_stop = False

    def run(self):
        self._running = True

        while not self._should_stop:
            try:
                message, headers = self._queue.get(timeout=0.1)
            except queue.Empty:
                continue

            try:
                if not self._publisher:
                    self._publisher = self._publisher_factory()
                self._publisher.publish(message, headers=headers)
            except Exception as e:
                logger.exception('Error while publishing: %s', e)

        self._running = False
        self._should_stop = False

    def publish(self, event, headers=None):
        headers = headers or {}
        self._queue.put((event, headers))

    def stop(self):
        if self._running:
            self._should_stop = True
