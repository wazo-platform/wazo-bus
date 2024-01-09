# Copyright 2024 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

import json
import os
import subprocess
from tempfile import TemporaryDirectory
from unittest import TestCase

from wazo_test_helpers.asset_launching_test_case import (
    AbstractAssetLaunchingHelper,
    _run_cmd,
)


class DockerError(Exception):
    pass


class ValidationError(Exception):
    pass


class TestDocumentation(AbstractAssetLaunchingHelper, TestCase):
    asset = 'documentation'
    assets_root = os.path.join(os.path.dirname(__file__), '..', 'assets')
    service = 'spec-generator'
    validator = 'spec-validator'

    @classmethod
    def _generate_specfiles(
        cls, output_directory: os.PathLike
    ) -> subprocess.CompletedProcess:
        program: list[str] = ['docker-compose']
        options: list[str] = cls._docker_compose_options()
        args: list[str] = [
            'run',
            '-v',
            f'{output_directory}:/app/output',
            cls.service,
            '-p',
            'test-version',
        ]

        return _run_cmd(program + options + args)

    @classmethod
    def _validate_specfile(
        cls, name: str, path: os.PathLike
    ) -> subprocess.CompletedProcess:
        program: list[str] = ['docker-compose']
        options: list[str] = cls._docker_compose_options()
        args: list[str] = [
            'run',
            '--no-TTY',  # needed for docker-compose v2.2.3 (https://github.com/orgs/community/discussions/11011)
            '-v',
            f'{path}:/{name}.yml',
            cls.validator,
            'validate',
            '--diagnostics-format',
            'json',
            f'/{name}.yml',
        ]

        return _run_cmd(program + options + args)

    @classmethod
    def _parse_errors(cls, process: subprocess.CompletedProcess) -> list[str]:
        output = process.stdout.decode().split('\n')
        issues = json.loads(''.join(output[2:]))

        return [issue['message'] for issue in issues if issue['severity'] == 0]

    def test_documentation_is_valid(self):
        with TemporaryDirectory() as basepath:
            result = self._generate_specfiles(basepath)
            if result.returncode != 0:
                print(result.stdout.decode())
                raise DockerError(
                    "An error occured while generating specification files"
                )

            for filename in os.listdir(basepath):
                path = os.path.join(basepath, filename)
                name, extension = os.path.splitext(filename)
                if extension.endswith('yml'):
                    result = self._validate_specfile(name, path)

                    if result.returncode != 0:
                        print(result.stdout.decode())
                        raise DockerError('an error occured within the validator')

                    if errors := self._parse_errors(result):
                        for error in errors:
                            print(error)
                        raise ValidationError(
                            f'Validation failed for {name} specification file'
                        )
