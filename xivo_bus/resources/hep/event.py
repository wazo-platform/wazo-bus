# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals

from ..common.event import BaseEvent


class HEPGeneralUpdatedEvent(BaseEvent):

    name = 'hep_general_updated'
    routing_key_fmt = 'config.hep_general.updated'

    def __init__(self):
        self._body = {}
        super(HEPGeneralUpdatedEvent, self).__init__()
