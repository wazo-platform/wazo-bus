# -*- coding: utf-8 -*-
# Copyright 2020 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class _BaseUserExternalAppEvent(BaseEvent):

    def __init__(self, app):
        self._body = app
        super(_BaseUserExternalAppEvent, self).__init__()


class EditUserExternalAppEvent(_BaseUserExternalAppEvent):
    name = 'user_external_app_edited'
    routing_key_fmt = 'config.user_external_apps.edited'


class CreateUserExternalAppEvent(_BaseUserExternalAppEvent):
    name = 'user_external_app_created'
    routing_key_fmt = 'config.user_external_apps.created'


class DeleteUserExternalAppEvent(_BaseUserExternalAppEvent):
    name = 'user_external_app_deleted'
    routing_key_fmt = 'config.user_external_apps.deleted'
