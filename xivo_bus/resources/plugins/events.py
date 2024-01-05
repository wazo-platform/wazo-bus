# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from ..common.event import ServiceEvent
from .types import PluginErrorDict


class PluginInstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_install_progress'
    routing_key_fmt = 'plugin.install.{uuid}.{status}'

    def __init__(
        self, plugin_uuid: str, status: str, errors: PluginErrorDict | None = None
    ):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)


class PluginUninstallProgressEvent(ServiceEvent):
    service = 'plugind'
    name = 'plugin_uninstall_progress'
    routing_key_fmt = 'plugin.uninstall.{uuid}.{status}'

    def __init__(
        self, plugin_uuid: str, status: str, errors: PluginErrorDict | None = None
    ):
        content = {'uuid': plugin_uuid, 'status': status}
        if errors:
            content.update(errors=errors)  # type: ignore[call-overload]
        super().__init__(content)
