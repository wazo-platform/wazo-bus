# -*- coding: utf-8 -*-
# Copyright 2018-2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class _BaseApplicationEvent(BaseEvent):

    def __init__(self, application):
        self._body = application
        super(_BaseApplicationEvent, self).__init__()


class EditApplicationEvent(_BaseApplicationEvent):
    name = 'application_edited'
    routing_key_fmt = 'config.applications.edited'


class CreateApplicationEvent(_BaseApplicationEvent):
    name = 'application_created'
    routing_key_fmt = 'config.applications.created'


class DeleteApplicationEvent(_BaseApplicationEvent):
    name = 'application_deleted'
    routing_key_fmt = 'config.applications.deleted'
