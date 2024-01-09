# Copyright 2022-2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import argparse
import importlib
import inspect
import logging
import os
import re
import sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from itertools import chain
from pathlib import Path
from time import time
from types import NoneType, UnionType
from typing import (
    Annotated,
    Any,
    Callable,
    Literal,
    TypedDict,
    Union,
    get_args,
    get_origin,
    get_type_hints,
    is_typeddict,
)

import yaml
from typing_extensions import TypeAlias, Unpack

PACKAGE_NAME = 'xivo_bus'
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AsyncAPIOptions(TypedDict, total=False):
    nullable: bool
    const: str
    enum: list


class AsyncAPITypes:
    @classmethod
    def _process_options(
        cls,
        content: dict,
        **options: Unpack[AsyncAPIOptions],
    ) -> dict:
        if 'nullable' in options:
            content['nullable'] = options.get('nullable', False)

        if 'const' in options:
            content['const'] = options['const']

        if 'enum' in options:
            content['enum'] = options['enum']

        return content

    @classmethod
    def array(cls, format: dict[str, str]) -> dict:
        return {'type': 'array', 'items': format}

    @classmethod
    def boolean(cls, *metadata: Any, **options: Unpack[AsyncAPIOptions]) -> dict:
        content = {'type': 'boolean'}
        return cls._process_options(content, **options)

    @classmethod
    def float_(cls, *metadata: Any, **options: Unpack[AsyncAPIOptions]) -> dict:
        content = {'type': 'float'}
        return cls._process_options(content, **options)

    @classmethod
    def integer(cls, *metadata: Any, **options: Unpack[AsyncAPIOptions]) -> dict:
        content = {'type': 'integer'}
        return cls._process_options(content, **options)

    @classmethod
    def object_(
        cls,
        content: dict | None = None,
        *metadata: Any,
        **options: Unpack[AsyncAPIOptions],
    ) -> dict:
        content = {'type': 'object', 'properties': content or {}}
        return cls._process_options(content, **options)

    @classmethod
    def string(cls, *metadata: Any, **options: Unpack[AsyncAPIOptions]) -> dict:
        content = {'type': 'string'}

        for obj in metadata:
            if hasattr(obj, 'format'):
                content['format'] = obj.format

        return cls._process_options(content, **options)


class Converter:
    _type_factories: dict[type | Any, Callable[..., dict]] = {
        Any: AsyncAPITypes.object_,
        bool: AsyncAPITypes.boolean,
        dict: AsyncAPITypes.object_,
        float: AsyncAPITypes.float_,
        int: AsyncAPITypes.integer,
        str: AsyncAPITypes.string,
    }

    @classmethod
    def _scan_hint(cls, hint: type) -> dict[str, str]:
        def recurse(
            type_: type, *metadata: Any, **options: Unpack[AsyncAPIOptions]
        ) -> dict:
            # Check if has a subtype i.e: type[subtype, ...]
            if origin_type := get_origin(type_):
                subtype, *args = get_args(type_)

                if origin_type is Annotated:
                    return recurse(subtype, *args, **options)

                elif origin_type is Literal:
                    if len(args) > 0:
                        return recurse(type(subtype), enum=[subtype, *args])
                    return recurse(type(subtype), const=subtype)

                # i.e: Union[X, Y] or X | Y
                # Note: we currently do not support multiple type in the API,
                #       other types will be omitted from the spec
                elif origin_type in (UnionType, Union):
                    nullable = any([item is NoneType for item in args])
                    return recurse(subtype, nullable=nullable)

                elif origin_type in (list, set, tuple):
                    if len(args) > 0:
                        raise TypeError('arrays cannot have multiple types')
                    return AsyncAPITypes.array(recurse(subtype, **options))

                elif origin_type is dict:
                    return AsyncAPITypes.object_(**options)

            elif is_typeddict(type_):
                content = {
                    name: recurse(subtype)
                    for name, subtype in get_type_hints(
                        type_, include_extras=True
                    ).items()
                }
                return AsyncAPITypes.object_(content, **options)

            # Standard types: bool, float, int, string, any...
            elif type_ in cls._type_factories.keys():
                factory = cls._type_factories[type_]
                return factory(*metadata, **options)

            raise TypeError(f'unhandled type: {type_}')

        return recurse(hint)

    @classmethod
    def from_init(cls, class_: type, *, ignore_keys: set[str] | None = None) -> dict:
        ignore_keys = ignore_keys or set()
        init_fn = getattr(class_, '__init__')

        hints: dict[str, type] = {
            param: type_
            for param, type_ in get_type_hints(init_fn, include_extras=True).items()
            if param not in ignore_keys
        }

        return {param: cls._scan_hint(hint) for param, hint in hints.items()}


class EventProxy:
    _DEFAULT_PAYLOAD_IGNORE_KEYS = {
        'self',
        'return',
        'tenant_uuid',
        'user_uuid',
        'user_uuids',
    }

    def __init__(self, class_: type):
        self.class_ = class_
        sig = inspect.signature(getattr(class_, '__init__'))
        self._parameters = sig.parameters
        self._keys = sig.parameters.keys()

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.class_, attr)

    def __lt__(self, other: TypeAlias) -> bool:
        return self.name < other.name

    @staticmethod
    def is_event(class_: type) -> bool:
        if not inspect.isclass(class_):
            return False

        if not all(
            hasattr(class_, attr) for attr in ('name', 'routing_key_fmt', 'content')
        ):
            return False

        if inspect.isabstract(class_):
            return False

        return True

    def __repr__(self) -> str:
        return f'<Event \'{self.name}\'>'

    @property
    def service(self) -> str:
        return getattr(self.class_, 'service', 'undefined')

    def generate_tag(self) -> list[dict]:
        return [{'name': self.service}]

    def generate_headers(self) -> dict:
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

        if 'tenant_uuid' in self._keys:
            headers['tenant_uuid'] = {'$ref': '#/components/schemas/tenant_uuid'}
            required.append('tenant_uuid')

        if any([key in self._keys for key in ('user_uuid', 'user_uuids')]):
            headers['user_uuid:{uuid}'] = {
                '$ref': '#/components/schemas/user_uuid:{uuid}'
            }
            required.append('user_uuid:{uuid}')

        return {'type': 'object', 'properties': headers, 'required': required}

    def generate_payload(self) -> dict:
        return Converter.from_init(
            self.class_, ignore_keys=self._DEFAULT_PAYLOAD_IGNORE_KEYS
        )

    def generate_parameters(self) -> dict:
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

    def generate_specification(self) -> dict:
        message_name = '-'.join([self.name.replace('_', '-'), 'payload'])
        doc = yaml.safe_load(self.class_.__doc__ or '')

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
    def __init__(self, input_schema: str, version: str):
        self.platform_version = str(version)
        self.base_path = self.get_package_path(PACKAGE_NAME)
        resource_dir = self.base_path.joinpath('resources')
        self.paths = [path for path in resource_dir.iterdir() if path.is_dir()]

        with open(input_schema) as file:
            self.input_schema = yaml.safe_load(file)

    @staticmethod
    def get_package_path(package_name: str) -> Path:
        module = importlib.import_module(package_name)
        entrypoint = inspect.getfile(module)
        return Path(os.path.dirname(entrypoint))

    def get_resource_events(self, resource_path: Path) -> list[EventProxy]:
        events: list[EventProxy] = []
        file_paths = sorted(resource_path.glob('*.py'))

        for path in file_paths:
            name = os.path.splitext(path.relative_to(self.base_path))[0]
            import_name = '.'.join([PACKAGE_NAME, name.replace('/', '.')])

            try:
                module = importlib.import_module(import_name)
            except ModuleNotFoundError as e:
                print(f'skipping {name}: {e}')
                continue

            events.extend(
                EventProxy(cls)
                for _, cls in inspect.getmembers(module, EventProxy.is_event)
            )

        return events

    def generate_specifications(self, events: list[EventProxy]) -> dict:
        failures: set[tuple[str, Exception]] = set()
        specifications: defaultdict[str, dict] = defaultdict(dict)

        print(
            f'generating AsyncAPI specifications for `{self.platform_version}` '
            f'({len(events)} events)'
        )

        for event in events:
            service = event.service
            try:
                event_spec = event.generate_specification()
            except Exception as e:
                print('F', end='')
                failures.add((event.name, e))
            else:
                print('.', end='')
                specifications[service].update(event_spec)
        print('\n')

        if failures:
            for event_name, error in failures:
                print(f'Failed to generate specification for {event_name}: {error}')
            raise RuntimeError('Failed to generate AsyncAPI specifications')

        return specifications

    def write_specifications(
        self, specifications: dict, output_dir: str, *, dry_run: bool = False
    ) -> None:
        def write(service: str) -> str:
            service_name = (
                '-'.join(['wazo', service]) if service != 'undefined' else service
            )
            path = Path(output_dir).joinpath(f'{service_name}.yml').resolve()
            schema = deepcopy(self.input_schema)
            schema['info']['title'] = f'{service_name} events'
            schema['info']['version'] = self.platform_version
            schema['channels'] = specifications[service]

            if dry_run:
                return f'would write \'{path}\''

            with open(path, 'w') as file:
                yaml.dump(schema, file, sort_keys=False)
            size = path.stat().st_size / 1024
            return f'wrote \'{path}\' ({size:.2f} KB)'

        with ThreadPoolExecutor() as executor:
            futs = [
                executor.submit(write, service) for service in specifications.keys()
            ]
        [print(fut.result()) for fut in futs]

    def run(self, output_dir: str = 'asyncapi', *, dry_run: bool = False) -> None:
        start_time = time()
        if dry_run:
            print('[DRY RUN]')

        with ThreadPoolExecutor() as executor:
            results = executor.map(self.get_resource_events, self.paths)

        events = sorted(chain(*results))
        specifications = self.generate_specifications(events)

        self.write_specifications(specifications, output_dir, dry_run=dry_run)
        exec_time = time() - start_time
        print(f'(execution took \'{exec_time:.3f}\' seconds)')


def generate_documentation(
    template_file: str, output_dir: str, version: str, *, dry_run: bool = False
) -> None:
    builder = EventSpecificationBuilder(template_file, version)
    try:
        builder.run(output_dir, dry_run=dry_run)
    except RuntimeError:
        print(flush=True)
        sys.exit('Error while generating AsyncAPI specifications, exiting...')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract AsyncAPI specification for service\'s events'
    )

    parser.add_argument('-o', type=str, dest='output_dir', required=True)
    parser.add_argument('-p', type=str, dest='platform_version', required=True)
    parser.add_argument(
        '-t', type=str, dest='template_file', default='asyncapi-template.yml'
    )
    parser.add_argument(
        '--dry', action='store_true', dest='dry_run', help='don\'t write files'
    )

    parsed = parser.parse_args()
    generate_documentation(
        parsed.template_file,
        parsed.output_dir,
        parsed.platform_version,
        dry_run=parsed.dry_run,
    )
