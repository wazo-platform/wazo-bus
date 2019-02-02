# -*- coding: utf-8 -*-
# Copyright 2018 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals


class _RTPConfigurationEvent(object):
    def marshal(self):
        return {}

    @classmethod
    def unmarshal(cls, msg):
        return cls()

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return not self == other


class EditRTPGeneralEvent(_RTPConfigurationEvent):
    name = 'rtp_general_edited'
    routing_key = 'config.rtp_general.edited'


class EditRTPIceHostCandidatesEvent(_RTPConfigurationEvent):
    name = 'rtp_ice_host_candidates_edited'
    routing_key = 'config.rtp_ice_host_candidates.edited'
