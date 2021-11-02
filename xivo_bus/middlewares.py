# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from datetime import datetime


class EventPublisherMiddleware(object):
    def __init__(self, service_uuid):
        self.uuid = service_uuid

    def __call__(self, event, headers, payload):
        headers = self._inject_headers_metadata(event, headers)
        event_data = self._prepare_event(event, payload)
        payload = dict(data=event_data, **headers)
        return headers, payload

    def _prepare_event(self, event, payload):
        payload = payload or {}
        try:
            return dict(event.marshal(), **payload)
        except AttributeError as e:
            raise ValueError(
                'Event \'{event}\' has invalid format -> {msg}'.format(event=event, msg=e)
            )

    def _inject_headers_metadata(self, event, headers):
        headers.update(
            name=event.name, origin_uuid=self.uuid, timestamp=datetime.now().isoformat()
        )

        if hasattr(event, 'required_acl'):
            headers['required_acl'] = event.required_acl

        return headers


class EventConsumerMiddleware(object):
    def __call__(self, event, headers, payload):
        data = payload.pop('data', None)
        headers = headers or payload
        return headers, data


class EchoMiddleware(object):
    _logger = logging.getLogger('EchoMiddleware')

    def __init__(self, title=''):
        self.title = title

    def __call__(self, event, headers, payload):
        self._logger.info(
            '{title}\nEvent: {event}\nHeaders: {headers}\nPayload: {payload}'.format(
                title=self.title, event=event, headers=headers, payload=payload
            )
        )
        return headers, payload
