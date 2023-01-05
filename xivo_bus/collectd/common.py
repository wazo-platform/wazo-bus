# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


class CollectdEvent:
    interval = 10
    plugin = None
    plugin_instance = None
    type_ = None
    type_instance = None
    values = ()
    time = 'N'

    def is_valid(self):
        return (
            self.plugin is not None
            and self.plugin_instance is not None
            and self.type_ is not None
            and self.type_instance is not None
            and (self.time == 'N' or isinstance(self.time, int))
            and len(self.values) > 0
        )
