# -*- coding: utf-8 -*-
# Copyright 2016-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseContextEvent(BaseEvent):

    def __init__(self, **context):
        self._body = context
        super(_BaseContextEvent, self).__init__()


class EditContextEvent(_BaseContextEvent):

    name = 'context_edited'
    routing_key_fmt = 'config.contexts.edited'


class CreateContextEvent(_BaseContextEvent):

    name = 'context_created'
    routing_key_fmt = 'config.contexts.created'


class DeleteContextEvent(_BaseContextEvent):

    name = 'context_deleted'
    routing_key_fmt = 'config.contexts.deleted'
