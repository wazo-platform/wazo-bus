# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractEvent(metaclass=ABCMeta):
    __slots__ = ('content',)

    def __init__(self, content: dict | None = None):
        self.content = content or {}

    def __eq__(self, other: Any) -> bool:
        return (
            self.__class__ == other.__class__
            and self.content == other.content
            and vars(self) == vars(other)
        )

    def __ne__(self, other: Any) -> bool:
        return not self == other

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return '<Event: {} (headers: {}, content: {})>'.format(
            self.name,
            self.headers,
            self.content,
        )

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def routing_key_fmt(self) -> str:
        pass

    @property
    def routing_key(self) -> str:
        variables = dict(**self.content)
        variables.update(vars(self), name=self.name)
        return self.routing_key_fmt.format(**variables)

    @property
    def required_acl(self) -> str:
        """
        Deprecated, use required_access instead
        """
        if hasattr(self, 'required_acl_fmt'):
            variables = dict(**self.content)
            variables.update(vars(self), name=self.name)
            return self.required_acl_fmt.format(**variables)
        return f'events.{self.routing_key}'

    @property
    def required_access(self) -> str:
        return f'event.{self.name}'

    @property
    def headers(self) -> dict:
        headers = dict(vars(self))
        headers.update(name=self.name)
        return headers

    def marshal(self) -> dict:
        return self.content
