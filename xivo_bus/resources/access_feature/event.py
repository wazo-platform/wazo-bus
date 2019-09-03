# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from xivo_bus.resources.common.event import BaseEvent


class DeleteAccessFeatureEvent(BaseEvent):
    name = 'access_feature_deleted'
    routing_key_fmt = 'config.access_feature.deleted'

    def __init__(self, access_feature_info):
        self._body = access_feature_info
        super(DeleteAccessFeatureEvent, self).__init__()


class EditAccessFeatureEvent(BaseEvent):
    name = 'access_feature_edited'
    routing_key_fmt = 'config.access_feature.edited'

    def __init__(self, access_feature_info):
        self._body = access_feature_info
        super(EditAccessFeatureEvent, self).__init__()


class CreateAccessFeatureEvent(BaseEvent):
    name = 'access_feature_created'
    routing_key_fmt = 'config.access_feature.created'

    def __init__(self, access_feature_info):
        self._body = access_feature_info
        super(CreateAccessFeatureEvent, self).__init__()
