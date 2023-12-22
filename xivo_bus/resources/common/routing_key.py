# Copyright 2017-2023 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def escape(routing_key_part: str) -> str:
    return (
        routing_key_part.replace('.', '__DOT__')
        .replace('#', '__HASH__')
        .replace('*', '__STAR__')
    )
