# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import importlib
import inspect
import os
import re
import yaml

from collections import ChainMap
from concurrent.futures import ThreadPoolExecutor
from glob import glob
from threading import Lock
from xivo_bus.resources.common.abstract import AbstractEvent


RESOURCES_DIR = os.path.join("resources", "**", "*.py")
KEYS_IGNORE_LIST = (
    'self',
    'tenant_uuid',
    'user_uuid',
)


class SpecBuilder:
    def __init__(self, schema_filename: str):
        self._lock = Lock()
        with open(schema_filename, 'r') as file:
            self.schema: dict = yaml.safe_load(file)

    def write(self, spec):
        with self._lock:
            self.schema['channels'].update(spec)

    def render(self, filename=None):
        if filename:
            try:
                with open(filename, 'w') as file:
                    yaml.dump(self.schema, file, sort_keys=False)
                return
            except Exception:
                raise
        print(json.dumps(self.schema, indent=4))


def camel_to_snake(str):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', str)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def generate_event_headers(cls, keys):
    required = ['name', 'required_access', 'origin_uuid', 'timestamp']
    headers = {
        'name': {
            'type': 'string',
            'const': cls.name,
            'description': 'Name of the event (used for routing the message)',
        },
        'required_access': {
            'type': 'string',
            'const': f'event.{cls.name}',
            'description': 'Necessary user access required to read this event',
        },
        'origin_uuid': {'$ref': '#/components/schemas/origin_uuid'},
        'timestamp': {'$ref': '#/components/schemas/timestamp'},
    }

    if 'tenant_uuid' in keys:
        headers['tenant_uuid'] = {'$ref': '#/components/schemas/tenant_uuid'}
        required.append('tenant_uuid')
    if 'user_uuid' in keys:
        headers['user_uuid:{uuid}'] = {'$ref': '#/components/schemas/user_uuid:{uuid}'}
        required.append('user_uuid:{uuid}')
    return headers, required


def generate_message(cls, keys):
    def contains(key, *parts):
        return any(part in key for part in parts)

    keys = [key for key in keys if key not in ('tenant_uuid', 'user_uuid', 'self')]
    content = {}

    for key in keys:
        if contains(key, 'uuid'):
            content[key] = {'type': 'string', 'format': 'uuid'}
        elif contains(key, 'id', 'number'):
            content[key] = {'type': 'integer'}
        elif key.endswith('_at'):
            content[key] = {'type': 'string', 'format': 'date-time'}
        elif key.endswith(('_data', '_info', '_schema')):
            content[key] = {'type': 'object'}
        else:
            content[key] = {'type': 'string'}

    name = '-'.join([*camel_to_snake(cls.name).split('_'), 'payload'])
    headers, required_headers = generate_event_headers(cls, keys)

    payload = {'type': 'null'}
    if content:
        payload['type'] = 'object'
        payload['properties'] = content

    return {
        'name': name,
        'payload': payload,
        'headers': {
            'type': 'object',
            'properties': headers,
            'required': required_headers,
        },
    }


def generate_base(cls, message):
    try:
        doc = yaml.safe_load(cls.__doc__)
    except AttributeError:
        doc = ''

    base = {
        'subscribe': {
            'summary': doc or '',
            'message': message,
        }
    }

    matches = re.search(r'\{(.*?)\}', cls.name)

    if matches:
        parameters = {}
        for param in matches.groups() or []:
            parameters[param] = {
                'description': '',
                'schema': {
                    'type': 'string',
                },
            }
        base['parameters'] = parameters

    return {cls.name: base}


def generate_event_spec(cls):
    fn_sig = inspect.signature(cls.__init__)
    fn_args = fn_sig.parameters.keys()

    message = generate_message(cls, fn_args)
    event_spec = generate_base(cls, message)

    return event_spec


def get_module_event_specs(path):
    module_name = os.path.splitext(path)[0].replace('/', '.')
    specs = {}

    try:
        module = importlib.import_module(module_name)
    except ModuleNotFoundError:
        return {}

    for item in dir(module):
        if item.startswith('__'):
            continue

        cls = getattr(module, item)
        if not isinstance(cls, type) or inspect.isabstract(cls):
            continue

        if not issubclass(cls, AbstractEvent):
            continue

        specs.update(generate_event_spec(cls))
    return specs


def import_events(base_cls=None):
    resources_dir = os.path.join("resources", "**", "event*.py")

    builder = SpecBuilder('base_spec.yml')
    paths = sorted(glob(resources_dir, recursive=False), reverse=True)

    with ThreadPoolExecutor() as executor:
        results = executor.map(get_module_event_specs, paths)

    builder.write(dict(ChainMap(*[result for result in results])))

    builder.render(filename='asyncapi.yml')
