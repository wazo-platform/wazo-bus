# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Avencall
#
# SPDX-License-Identifier: GPL-3.0+

import logging

logger = logging.getLogger(__name__)


def retry_message(exception, interval):
    logger.error('Error: %s', exception, exc_info=1)
    logger.info('Retry in %s seconds...', interval)
