# -*- coding: utf-8 -*-
# Copyright (C) 2016 Avencall
# SPDX-License-Identifier: GPL-3.0+


class CollectdEvent(object):
    interval = 10
    plugin = None
    plugin_instance = None
    type_ = None
    type_instance = None
    values = ()
    time = 'N'

    def is_valid(self):
        return (self.plugin is not None and
                self.plugin_instance is not None and
                self.type_ is not None and
                self.type_instance is not None and
                (self.time == 'N' or isinstance(self.time, int)) and
                len(self.values) > 0)
