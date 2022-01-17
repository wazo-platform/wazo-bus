# Copyright 2020-2021 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
from abc import ABCMeta, abstractmethod
from datetime import datetime
from six import add_metaclass, raise_from


class MiddlewareError(Exception):
    def __init__(self, middleware):
        self.message = 'Error during middleware \'{}\' execution'.format(
            middleware
        )


@add_metaclass(ABCMeta)
class Middleware(object):
    '''
    Abstract class used to define a bus serializer/deserializer

    Must implement functions:
        marshal(self, event, headers, payload) -> headers, payload
            Hook to perform action on data being sent on the wire

        unmarshal(self, event, headers, payload) -> headers, payload
            Hook to perform action on data being received
    '''

    @abstractmethod
    def marshal(self, event, headers, payload):
        '''
        Transformations to apply on data before sending it on the bus

        Parameters:
            event (object, str): Event
            headers (dict): Message headers
            payload (dict): Message body

        returns:
            headers (dict): Modified headers
            payload (dict): Modified payload
        '''
        return headers, payload

    @abstractmethod
    def unmarshal(self, event, headers, payload):
        '''
        Transformations to apply on data before application receives it

        Parameters:
            event (object, str): Event
            headers (dict): Message headers
            payload (dict): Message body

        returns:
            headers (dict): Modified headers
            payload (dict): Modified payload
        '''
        return headers, payload


class EventMarshaller(Middleware):
    def __init__(self, service_uuid=None, copy_headers_in_payload=True):
        self.service_uuid = service_uuid
        self.copy_headers = copy_headers_in_payload

    def marshal(self, event, headers, payload):
        headers = self._inject_metadata(event, headers)
        payload = dict(data=self._serialize_event(event, payload))
        if self.copy_headers:
            payload.update(**headers)
        return headers, payload

    def unmarshal(self, event, headers, payload):
        data = payload.pop('data')
        headers = headers or payload
        return headers, data

    def _serialize_event(self, event, payload):
        payload = payload or {}
        try:
            return dict(event.marshal(), **payload)
        except AttributeError as exc:
            raise_from(
                ValueError('Event \'{}\' has an invalid format'.format(event)), exc
            )

    def _inject_metadata(self, event, headers):
        headers = headers or {}
        headers.update(
            name=event.name,
            origin_uuid=self.service_uuid,
            timestamp=datetime.now().isoformat(),
        )

        if hasattr(event, 'required_acl'):
            headers['required_acl'] = event.required_acl
        return headers


class EventLogger(Middleware):
    logger = logging.getLogger(__name__)

    def marshal(self, event, headers, payload):
        self.logger.info(
            'Transmitting:\n\tEvent: %s\n\tHeaders: %s\n\tPayload: %s',
            event,
            headers,
            payload,
        )
        return headers, payload

    def unmarshal(self, event, headers, payload):
        self.logger.info(
            'Receiving:\n\tEvent: %s\n\tHeaders: %s\n\tPayload: %s',
            event,
            headers,
            payload,
        )
        return headers, payload
