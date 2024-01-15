# Copyright 2016-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from abc import abstractmethod

from ..resources.common.abstract import EventProtocol


class CollectdEvent(EventProtocol):
    '''
    Base Collectd Event

    subclasses must define the following attributes:
      * name
      * routing_key_fmt
      * plugin
      * type_
    '''

    routing_key_fmt: str
    interval: int = 10
    plugin_instance: str | None = None
    time: str | int = 'N'
    type_instance: str | None = None
    values: tuple[str, ...] = ()

    def __init__(self, content: dict | None = None):
        self.content = content or {}

    @property
    @abstractmethod
    def plugin(self) -> str:
        pass

    @property
    @abstractmethod
    def type_(self) -> str:
        pass

    def is_valid(self) -> bool:
        return (
            self.plugin is not None
            and self.plugin_instance is not None
            and self.type_ is not None
            and self.type_instance is not None
            and (self.time == 'N' or isinstance(self.time, int))
            and len(self.values) > 0
        )

    def __str__(self) -> str:
        content = ', '.join(
            [
                f'plugin=\'{self.plugin}\'',
                f'plugin_instance=\'{self.plugin_instance}\'',
                f'type=\'{self.type_}\'',
                f'type_instance=\'{self.type_instance}\'',
                f'values={self.values}',
            ]
        )
        return f'CollectdEvent({content})'
