# -*- coding: utf-8 -*-
# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class _HEPConfigurationEvent(object):
    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, msg):
        return cls()

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other


class EditHEPGeneralEvent(_HEPConfigurationEvent):
    name = 'hep_general_edited'
    routing_key = 'config.hep_general.edited'
