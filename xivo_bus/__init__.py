# Copyright 2013-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from warnings import warn

import wazo_bus

warn(
    f'{__name__} is deprecated and will be removed in the future, '
    'Please use `wazo_bus` instead.',
    DeprecationWarning,
    stacklevel=2,
)

# Note: Alias xivo_bus to wazo_bus
sys.modules['xivo_bus'] = wazo_bus
