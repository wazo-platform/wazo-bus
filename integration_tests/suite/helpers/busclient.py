# Copyright 2021-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import requests
from inspect import ismethod


class BusApiClient(object):
    def __init__(self, host='localhost', port=6444):
        self._base_url = 'http://{host}:{port}'.format(host=host, port=port)

    def _make_url(self, *part):
        return '/'.join([self._base_url, *part])

    def _serialize_event(self, event):
        obj = {}
        attrs = list(filter(lambda a: not a.startswith('__'), dir(event)))

        for attr in attrs:
            value = getattr(event, attr, None)
            if not ismethod(value):
                obj[attr] = value
        return obj

    def bind(self, event, headers=None, headers_match_all=True, routing_key=None):
        url = self._make_url('bus', event, 'subscribe')
        payload = {
            'headers': headers,
            'headers_match_all': headers_match_all,
            'routing_key': routing_key,
        }
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def unbind(self, event, headers=None, headers_match_all=True, routing_key=None):
        url = self._make_url('bus', event, 'unsubscribe')
        payload = {
            'headers': headers,
            'headers_match_all': headers_match_all,
            'routing_key': routing_key,
        }
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def publish(self, event, message, headers=None, routing_key=None):
        url = self._make_url('bus', event, 'publish')
        payload = {'headers': headers, 'routing_key': routing_key, 'payload': message}
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def publish_event(self, event, headers=None, routing_key=None):
        url = self._make_url('bus', event.name, 'publish')
        headers = headers or {}
        payload = {
            'headers': {'x-event-object': True, **headers},
            'routing_key': routing_key,
            'payload': self._serialize_event(event),
        }
        resp = requests.post(url, json=payload)
        return resp.status_code == 200

    def get_messages(self, event):
        url = self._make_url('bus', event, 'messages')
        return requests.get(url).json()

    def add_middleware(self, bus_type, middleware, *args, **kwargs):
        url = self._make_url('bus', 'middlewares', middleware)
        payload = {'type': bus_type, 'args': args, 'kwargs': kwargs}
        resp = requests.put(url, json=payload)
        return resp.status_code == 200

    def remove_middleware(self, bus_type, middleware):
        url = self._make_url('bus', 'middlewares', middleware)
        payload = {'type': bus_type}
        resp = requests.delete(url, json=payload)
        return resp.status_code == 200
