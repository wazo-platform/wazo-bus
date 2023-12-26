# Copyright 2018-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class RTPGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_general_edited'
    routing_key_fmt = 'config.rtp_general.edited'

    def __init__(self) -> None:
        super().__init__()


class RTPIceHostCandidatesEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'rtp_ice_host_candidates_edited'
    routing_key_fmt = 'config.rtp_ice_host_candidates.edited'

    def __init__(self) -> None:
        super().__init__()
