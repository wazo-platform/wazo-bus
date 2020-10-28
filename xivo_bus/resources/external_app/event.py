# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class _BaseExternalAppEvent(BaseEvent):

    def __init__(self, app):
        self._body = app
        super(_BaseExternalAppEvent, self).__init__()


class EditExternalAppEvent(_BaseExternalAppEvent):
    name = 'external_app_edited'
    routing_key_fmt = 'config.external_apps.edited'


class CreateExternalAppEvent(_BaseExternalAppEvent):
    name = 'external_app_created'
    routing_key_fmt = 'config.external_apps.created'


class DeleteExternalAppEvent(_BaseExternalAppEvent):
    name = 'external_app_deleted'
    routing_key_fmt = 'config.external_apps.deleted'
