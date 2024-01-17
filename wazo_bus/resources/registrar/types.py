# Copyright 2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TypedDict


class RegistrarDict(TypedDict, total=False):
    id: str
    deletable: bool
    name: str
    main_host: str
    main_port: int
    backup_host: str
    backup_port: int
    proxy_main_host: str
    proxy_main_port: int
    proxy_backup_host: str
    proxy_backup_port: int
    outbound_proxy_host: str
    outbound_proxy_port: int
