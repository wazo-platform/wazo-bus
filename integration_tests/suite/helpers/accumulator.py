# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import defaultdict


class MessageAccumulator(object):
    def __init__(self):
        self._buffer = defaultdict(list)

    def create_handler(self, event):
        def handler(payload):
            self.add(event, payload)

        return handler

    def add(self, event, message):
        event = event if event else '__none__'
        self._buffer[event].append(message)

    def pop(self, event):
        event = event if event else '__none__'
        return self._buffer.pop(event, [])
