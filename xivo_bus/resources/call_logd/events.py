# -*- coding: utf-8 -*-
# Copyright 2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import BaseEvent


class RetentionUpdatedEvent(BaseEvent):

    name = 'call_logd_retention_updated'
    routing_key_fmt = 'call_logd.retention.updated'

    def __init__(self, retention):
        self._body = retention
        super(RetentionUpdatedEvent, self).__init__()
