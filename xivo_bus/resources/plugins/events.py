# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class PluginInstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_install_progress'
    routing_key_fmt = 'plugin.install.{uuid}.{status}'

    def __init__(self, plugin_uuid, status, errors=None):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)
        super(PluginInstallProgressEvent, self).__init__(content)


class PluginUninstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_uninstall_progress'
    routing_key_fmt = 'plugin.uninstall.{uuid}.{status}'

    def __init__(self, plugin_uuid, status, errors=None):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)
        super(PluginUninstallProgressEvent, self).__init__(content)
