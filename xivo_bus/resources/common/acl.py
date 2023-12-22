# Copyright 2022-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def escape(acl_part: str) -> str:
    return (
        acl_part.replace('.', '__DOT__')
        .replace('#', '__HASH__')
        .replace('*', '__STAR__')
    )
