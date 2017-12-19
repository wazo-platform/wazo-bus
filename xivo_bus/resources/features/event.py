# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from __future__ import unicode_literals


class _FeaturesConfigurationEvent(object):
    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, msg):
        return cls()

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other


class EditFeaturesApplicationmapEvent(_FeaturesConfigurationEvent):
    name = 'features_applicationmap_edited'
    routing_key = 'config.features_applicationmap.edited'


class EditFeaturesFeaturemapEvent(_FeaturesConfigurationEvent):
    name = 'features_featuremap_edited'
    routing_key = 'config.features_featuremap.edited'


class EditFeaturesGeneralEvent(_FeaturesConfigurationEvent):
    name = 'features_general_edited'
    routing_key = 'config.features_general.edited'
