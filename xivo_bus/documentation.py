import importlib
import inspect
import os
import re
import yaml

from glob import glob
from concurrent.futures import ThreadPoolExecutor
from collections import ChainMap
from xivo_bus.resources.common.abstract import AbstractEvent

# from xivo_bus.resources.common.event import TenantEvent, UserEvent


RESOURCES_DIR = os.path.join("resources", "**", "event*.pyi")
KEYS_IGNORE_LIST = (
    'self',
    'tenant_uuid',
    'user_uuid',
)


def generate_format():
    spec = {
        'asyncapi': '2.0.0',
        'info': {
            'title': '',
            'version': '0.0.1',
        },
        'servers': {
            'production': {
                'url': 'amqp://guest:guest@localhost:5672/',
                'protocol': 'amqp',
                'protocolVersion': '0.9.1',
            }
        },
        'channels': {},
        'components': {
            'x-headers': {
                'origin_uuid': {
                    'type': 'string',
                    'format': 'uuid',
                    'description': 'Unique identifier of the WAZO service that published this '
                    'event',
                },
                'timestamp': {
                    'type': 'string',
                    'format': 'date-time',
                    'description': 'date and time this event was published',
                },
                'tenant_uuid': {
                    'type': 'string',
                    'format': 'uuid',
                    'description': 'Resource\'s associated tenant\'s UUID',
                },
                'user_uuid:{uuid}': {
                    'name': 'user_uuid',
                    'type': 'boolean',
                    'description': 'Targeted user\'s uuid.  The format user_uuid:<uuid> allows '
                    'multiple users to be the recipient of the event',
                    'parameters': {
                        'uuid': {
                            'description': 'Concerned user\'s unique identifier',
                            'schema': {
                                'type': 'string',
                                'format': 'uuid',
                            },
                        },
                    },
                },
            },
            'schemas': {},
        },
    }
    return spec


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
        'origin_uuid': {'$ref': '#/components/x-headers/origin_uuid'},
        'timestamp': {'$ref': '#/components/x-headers/timestamp'},
    }

    if 'tenant_uuid' in keys:
        headers['tenant_uuid'] = {'$ref': '#/components/x-headers/tenant_uuid'}
        required.append('tenant_uuid')
    if 'user_uuid' in keys:
        headers['user_uuid:{uuid}'] = {'$ref': '#/components/x-headers/user_uuid:{uuid}'}
        required.append('user_uuid:{uuid}')
    return headers, required


def generate_event_payload(cls, keys):
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
        else:
            content[key] = {'type': 'string'}

    return {
        'data': {
            'type': 'object',
            'properties': content,
        },
    }


def generate_event_parameters(cls):
    parameters = {}
    matches = re.search(r'\{(.*?)\}', cls.name)
    if matches is None:
        return {}

    for param in matches.groups() or []:
        parameters[param] = {
            'description': '',
            'schema': {
                'type': 'string',
            },
        }
    return {'parameters': parameters}


def generate_event_spec(cls):
    fn_sig = inspect.signature(cls.__init__)
    fn_args = fn_sig.parameters.keys()

    try:
        doc = yaml.safe_load(cls.__doc__)
    except AttributeError:
        doc = {}

    headers, required_headers = generate_event_headers(cls, fn_args)
    payload = generate_event_payload(cls, fn_args)

    event_spec = {
        'subscribe': {
            'summary': doc.get('summary', ''),
            'message': {
                'payload': {
                    'type': 'object',
                    'properties': payload,
                },
                'headers': {
                    'type': 'object',
                    'properties': headers,
                    'required': required_headers,
                },
            },
        }
    }

    parameters = generate_event_parameters(cls)
    parameters.update(event_spec)
    return parameters


def get_event_spec(path):
    module_name = os.path.splitext(path)[0].replace('/', '.')
    spec = {}

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

        spec[cls.name] = generate_event_spec(cls)
    return spec


def import_events(base_cls=None):
    resources_dir = os.path.join("resources", "**", "event*.py")

    paths = sorted(glob(resources_dir, recursive=False), reverse=True)
    spec = generate_format()

    with ThreadPoolExecutor() as executor:
        results = executor.map(get_event_spec, paths)

    spec['channels'] = dict(ChainMap(*[result for result in results]))

    try:
        with open('events_spec.yml', 'w') as file:
            yaml.dump(spec, file, sort_keys=False)
    except Exception:
        raise
