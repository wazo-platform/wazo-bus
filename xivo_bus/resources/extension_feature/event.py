# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals

from xivo_bus.resources.common.event import ResourceConfigEvent


class EditExtensionFeatureEvent(ResourceConfigEvent):
    name = 'extension_feature_edited'
    routing_key = 'config.extension_feature.edited'
