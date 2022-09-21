# Copyright 2022-2022 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import importlib
import inspect
import logging
import os
import re
import yaml

from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from glob import glob
from itertools import chain
from sys import stdout
from time import time

from xivo_bus.resources.common.abstract import AbstractEvent


logging.basicConfig(stream=stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

RESOURCES_DIR = os.path.join("resources", "**")


class Event:
    def __init__(self, class_):
        self.class_ = class_

        sig = inspect.signature(class_.__init__)
        self.__keys__ = sig.parameters.keys()

    def __getattr__(self, attr):
        return getattr(self.class_, attr)

    @staticmethod
    def is_event(class_):
        if not inspect.isclass(class_):
            return False

        if not issubclass(class_, AbstractEvent):
            return False

        if inspect.isabstract(class_):
            return False

        return True

    def __repr__(self):
        return f'<Event \'{self.name}\'>'

    @property
    def service(self):
        return getattr(self.class_, 'service', 'undefined')

    def generate_tag(self):
        return [{'name': self.service}]

    def generate_headers(self):
        headers = {
            'name': {
                'type': 'string',
                'const': self.name,
                'description': 'Name of the event (used for routing the message)',
            },
            'required_access': {
                'type': 'string',
                'const': f'event.{self.name}',
                'description': 'Necessary user access required to read this event',
            },
            'origin_uuid': {'$ref': '#/components/schemas/origin_uuid'},
            'timestamp': {'$ref': '#/components/schemas/timestamp'},
        }
        required = ['name', 'required_access', 'origin_uuid', 'timestamp']

        if 'tenant_uuid' in self.__keys__:
            headers['tenant_uuid'] = {'$ref': '#/components/schemas/tenant_uuid'}
            required.append('tenant_uuid')

        if 'user_uuid' in self.__keys__:
            headers['user_uuid:{uuid}'] = {
                '$ref': '#/components/schemas/user_uuid:{uuid}'
            }
            required.append('user_uuid:{uuid}')

        return {'type': 'object', 'properties': headers, 'required': required}

    def generate_payload(self):
        content = {}
        keys_ignore_list = ('tenant_uuid', 'user_uuid', 'self')
        content_keys = [key for key in self.__keys__ if key not in keys_ignore_list]

        for key in content_keys:
            if key.endswith('uuid'):
                content[key] = {'type': 'string', 'format': 'uuid'}
            elif key.endswith(('id', 'number')):
                content[key] = {'type': 'integer'}
            elif key.startswith('is_'):
                content[key] = {'type': 'boolean'}
            elif key.endswith('at'):
                content[key] = {'type': 'string', 'format': 'date-time'}
            elif key.endswith(('_data', '_info', '_schema')):
                content[key] = {'type': 'object', 'properties': {}}
            else:
                content[key] = {'type': 'string'}

        return {
            'type': 'object',
            'properties': {
                'data': {
                    'type': 'object',
                    'properties': content,
                }
            },
        }

    def generate_parameters(self):
        parameters = {}
        matches = re.search(r'\{(.*?)\}', self.name)
        if matches:
            for param in matches.groups() or []:
                parameters[param] = {
                    'description': '',
                    'schema': {
                        'type': 'string',
                    },
                }
        return parameters

    def generate_specification(self):
        message_name = '-'.join([self.name.replace('_', '-'), 'payload'])

        try:
            doc = yaml.safe_load(self.class_.__doc__)
        except AttributeError:
            doc = ''

        spec = {
            'subscribe': {
                'summary': doc or '',
                'tags': self.generate_tag(),
                'message': {
                    'name': message_name,
                    'payload': self.generate_payload(),
                    'headers': self.generate_headers(),
                },
            }
        }

        parameters = self.generate_parameters()
        if parameters:
            spec['parameters'] = parameters

        return {self.name: spec}


class EventSpecificationBuilder:
    def __init__(self, input_schema, *, overwrite_all=False, **kwargs):
        paths = sorted(glob(RESOURCES_DIR, recursive=False), reverse=False)

        with open(input_schema, 'r') as file:
            self.input_schema = yaml.safe_load(file)
        self.overwrite = overwrite_all
        self.paths = [path for path in paths if '__' not in path]

    def get_resource_events(self, path):
        events = []
        file_paths = glob(os.path.join(path, '*.py'), recursive=False)

        for file_path in file_paths:
            import_name = os.path.splitext(file_path)[0].replace('/', '.')
            try:
                module = importlib.import_module(import_name)
            except ModuleNotFoundError:
                raise

            events.extend(
                Event(cls) for _, cls in inspect.getmembers(module, Event.is_event)
            )

        return events

    def generate_specifications(self, events):
        print(f'generating AsyncAPI specifications ({len(events)} events)')
        specifications = {}
        for event in events:
            service = event.service
            if service not in specifications:
                specifications[service] = {}
            specifications[service].update(event.generate_specification())
            print('.', end='')
        print('\n')
        return specifications

    def write_specifications(self, specifications, output_dir, *, dry_run=False):
        def write(service):
            path = os.path.join(dirpath, f'{service}.yml')
            schema = deepcopy(self.input_schema)
            schema['info']['title'] = f'{service} events'
            schema['channels'] = specifications[service]

            if not dry_run:
                with open(path, 'w+') as file:
                    yaml.dump(schema, file, sort_keys=False)
            print(f'would write \'{path}\'' if dry_run else f'wrote \'{path}\'')

        dirpath = os.path.abspath(output_dir)
        try:
            os.makedirs(dirpath)
        except OSError:
            if not os.path.isdir(dirpath):
                raise

        with ThreadPoolExecutor() as executor:
            executor.map(write, specifications.keys())

    def run(self, output_dir='asyncapi', *, dry_run=False):
        start_time = time()
        if dry_run:
            print('[DRY RUN]')

        with ThreadPoolExecutor() as executor:
            results = executor.map(self.get_resource_events, self.paths)

        events = list(chain(*results))
        specifications = self.generate_specifications(events)

        self.write_specifications(specifications, output_dir, dry_run=dry_run)
        exec_time = time() - start_time
        print(f'(execution took \'{exec_time:.3f}\' seconds)')


def parse(template_file, output_dir, *, dry_run=False):
    builder = EventSpecificationBuilder(template_file)
    builder.run(output_dir, dry_run=dry_run)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract AsyncAPI specification for service\'s events'
    )

    parser.add_argument('-o', type=str, dest='output_dir', required=True)
    parser.add_argument(
        '-t', type=str, dest='template_file', default='asyncapi-template.yml'
    )
    parser.add_argument(
        '--dry', action='store_true', dest='dry_run', help='don\'t write files'
    )

    try:
        parsed = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)

    parse(parsed.template_file, parsed.output_dir, dry_run=parsed.dry_run)
