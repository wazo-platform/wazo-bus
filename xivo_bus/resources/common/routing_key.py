# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later


def escape(routing_key_part):
    return routing_key_part.replace('.', '__DOT__').replace('#', '__HASH__').replace('*', '__STAR__')
