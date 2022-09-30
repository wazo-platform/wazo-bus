# -*- coding: utf-8 -*-
# Copyright 2019-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ServiceEvent


class AccessFeatureCreatedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_created'
    routing_key_fmt = 'config.access_feature.created'

    def __init__(self, access_feature_info):
        super(AccessFeatureCreatedEvent, self).__init__(content=access_feature_info)


class AccessFeatureDeletedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_deleted'
    routing_key_fmt = 'config.access_feature.deleted'

    def __init__(self, access_feature_info):
        super(AccessFeatureDeletedEvent, self).__init__(content=access_feature_info)


class AccessFeatureEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'access_feature_edited'
    routing_key_fmt = 'config.access_feature.edited'

    def __init__(self, access_feature_info):
        super(AccessFeatureEditedEvent, self).__init__(content=access_feature_info)
