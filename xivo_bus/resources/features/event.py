# -*- coding: utf-8 -*-
# Copyright 2017-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class FeaturesApplicationmapEditedEvent(ServiceEvent):
    name = 'features_applicationmap_edited'
    routing_key_fmt = 'config.features_applicationmap.edited'

    def __init__(self):
        super(FeaturesApplicationmapEditedEvent, self).__init__()


class FeaturesFeaturemapEditedEvent(ServiceEvent):
    name = 'features_featuremap_edited'
    routing_key_fmt = 'config.features_featuremap.edited'

    def __init__(self):
        super(FeaturesFeaturemapEditedEvent, self).__init__()


class FeaturesGeneralEditedEvent(ServiceEvent):
    name = 'features_general_edited'
    routing_key_fmt = 'config.features_general.edited'

    def __init__(self):
        super(FeaturesGeneralEditedEvent, self).__init__()
