# -*- coding: utf-8 -*-
# Copyright 2013-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class LineStatusUpdatedEvent(BaseEvent):

    name = 'line_status_updated'
    routing_key_fmt = 'lines.{id}.status.updated'

    def __init__(self, status):
        self._body = status
        super(LineStatusUpdatedEvent, self).__init__()


class _BaseLineEvent(BaseEvent):

    def __init__(self, line):
        self._body = line
        super(_BaseLineEvent, self).__init__()


class EditLineEvent(_BaseLineEvent):
    name = 'line_edited'
    routing_key_fmt = 'config.line.edited'


class CreateLineEvent(_BaseLineEvent):
    name = 'line_created'
    routing_key_fmt = 'config.line.created'


class DeleteLineEvent(_BaseLineEvent):
    name = 'line_deleted'
    routing_key_fmt = 'config.line.deleted'
