# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from ..common.event import ServiceEvent


class VoicemailZoneMessagesEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'voicemail_zonemessages_edited'
    routing_key_fmt = 'config.voicemail_zonemessages.edited'

    def __init__(self) -> None:
        super().__init__()
