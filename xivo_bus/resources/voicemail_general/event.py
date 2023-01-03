# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import unicode_literals
from xivo_bus.resources.common.event import ServiceEvent


class VoicemailGeneralEditedEvent(ServiceEvent):
    service = 'confd'
    name = 'voicemail_general_edited'
    routing_key_fmt = 'config.voicemail_general.edited'

    def __init__(self):
        super(VoicemailGeneralEditedEvent, self).__init__()
