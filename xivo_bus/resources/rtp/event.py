# -*- coding: utf-8 -*-
# Copyright 2018-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class RTPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_general_edited'
    routing_key_fmt = 'config.rtp_general.edited'

    def __init__(self):
        super(RTPGeneralEditedEvent, self).__init__()


class RTPIceHostCandidatesEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_ice_host_candidates_edited'
    routing_key_fmt = 'config.rtp_ice_host_candidates.edited'

    def __init__(self):
        super(RTPIceHostCandidatesEditedEvent, self).__init__()
