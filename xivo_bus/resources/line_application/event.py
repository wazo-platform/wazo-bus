# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseLineApplicationEvent(BaseEvent):

    def __init__(self, line, application):
        self._body = {'line': line, 'application': application}
        super(_BaseLineApplicationEvent, self).__init__()


class LineApplicationAssociatedEvent(_BaseLineApplicationEvent):

    name = 'line_application_associated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.updated'


class LineApplicationDissociatedEvent(_BaseLineApplicationEvent):

    name = 'line_application_dissociated'
    routing_key_fmt = 'config.lines.{line[id]}.applications.{application[uuid]}.deleted'
