# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_bus.resources.common.event import ServiceEvent


class ExtensionFeatureEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'extension_feature_edited'
    routing_key_fmt = 'config.extension_feature.edited'

    def __init__(self, feature_extension_uuid: str):
        content = {'uuid': feature_extension_uuid}
        super().__init__(content)
