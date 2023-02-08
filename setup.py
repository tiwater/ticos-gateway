# -*- coding: utf-8 -*-

#     Copyright 2019. Ticos
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from setuptools import setup
from os import path

from ticos_gateway.gateway.constants import VERSION


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    version=VERSION,
    name="ticos-gateway",
    author="Ticos",
    author_email="info@ticos.io",
    license="Apache Software License (Apache Software License 2.0)",
    description="Ticos Gateway for IoT devices.",
    url="https://github.com/ticos/ticos-gateway",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.7",
    packages=['ticos_gateway', 'ticos_gateway.gateway', 'ticos_gateway.gateway.proto', 'ticos_gateway.gateway.grpc_service',
              'ticos_gateway.storage', 'ticos_gateway.storage.memory', 'ticos_gateway.gateway.shell',
              'ticos_gateway.storage.file', 'ticos_gateway.storage.sqlite',
              'ticos_gateway.connectors', 'ticos_gateway.connectors.ble', 'ticos_gateway.connectors.socket',
              'ticos_gateway.connectors.mqtt',  'ticos_gateway.connectors.opcua_asyncio', 'ticos_gateway.connectors.xmpp',
              'ticos_gateway.connectors.opcua', 'ticos_gateway.connectors.request', 'ticos_gateway.connectors.ocpp',
              'ticos_gateway.connectors.modbus', 'ticos_gateway.connectors.can', 'ticos_gateway.connectors.bacnet',
              'ticos_gateway.connectors.bacnet.bacnet_utilities', 'ticos_gateway.connectors.odbc',
              'ticos_gateway.connectors.rest', 'ticos_gateway.connectors.snmp', 'ticos_gateway.connectors.ftp',
              'ticos_gateway.ticos_utility', 'ticos_gateway.extensions',
              'ticos_gateway.extensions.mqtt', 'ticos_gateway.extensions.modbus', 'ticos_gateway.extensions.opcua',
              'ticos_gateway.extensions.opcua_asyncio', 'ticos_gateway.extensions.ocpp',
              'ticos_gateway.extensions.ble', 'ticos_gateway.extensions.serial', 'ticos_gateway.extensions.request',
              'ticos_gateway.extensions.can', 'ticos_gateway.extensions.bacnet', 'ticos_gateway.extensions.odbc',
              'ticos_gateway.extensions.rest',  'ticos_gateway.extensions.snmp', 'ticos_gateway.extensions.ftp',
              'ticos_gateway.extensions.socket', 'ticos_gateway.extensions.xmpp',
              ],
    install_requires=[
        'cryptography',
        'jsonpath-rw',
        'regex',
        'pip',
        'PyYAML',
        'simplejson',
        'requests',
        'PyInquirer',
        'pyfiglet',
        'termcolor',
        'grpcio<=1.43.0',
        'protobuf',
        'cachetools'
    ],
    download_url='https://github.com/ticos/ticos-gateway/archive/%s.tar.gz' % VERSION,
    entry_points={
        'console_scripts': [
            'ticos-gateway = ticos_gateway.ticos_gateway:daemon',
            'ticos-gateway-configurator = ticos_gateway.gateway.configuration_wizard:configure',
            'ticos-gateway-shell = ticos_gateway.gateway.shell:main'
        ]
    })
