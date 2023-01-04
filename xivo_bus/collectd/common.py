# Copyright 2016-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import ABC, abstractmethod


class AbstractCollectdEvent(ABC):
    interval = 10
    time = 'N'
    values = ()

    @property
    @abstractmethod
    def plugin(self):
        pass

    @property
    @abstractmethod
    def plugin_instance(self):
        pass

    @property
    @abstractmethod
    def routing_key(self):
        pass

    @property
    @abstractmethod
    def type_(self):
        pass

    @property
    @abstractmethod
    def type_instance(self):
        pass

    def is_valid(self):
        return (
            self.plugin is not None
            and self.plugin_instance is not None
            and self.type_ is not None
            and self.type_instance is not None
            and (self.time == 'N' or isinstance(self.time, int))
            and len(self.values) > 0
        )

    def __str__(self):
        content = ', '.join(
            [
                f'plugin={self.plugin}',
                f'plugin_instance={self.plugin_instance}',
                f'type={self.type_}',
                f'type_instance={self.type_instance}',
                f'values={self.values}',
            ]
        )
        return f'<Collectd Event: {content}>'
