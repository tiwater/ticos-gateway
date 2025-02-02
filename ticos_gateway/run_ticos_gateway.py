#     Copyright 2022. Ticos
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
import sys
from os import curdir, listdir, mkdir, path

from ticos_gateway.gateway.ticos_gateway_service import TicosGatewayService
from ticos_gateway.gateway.hot_reloader import HotReloader


def main():
    if "logs" not in listdir(curdir):
        mkdir("logs")

    try:
        hot_reload = bool(sys.argv[1])
    except IndexError:
        hot_reload = False

    if hot_reload:
        HotReloader(TicosGatewayService)
    else:
        TicosGatewayService(path.dirname(path.abspath(__file__)) + '/config/ticos_gateway.yaml'.replace('/', path.sep))


def daemon():
    TicosGatewayService("/etc/ticos-gateway/config/ticos_gateway.yaml".replace('/', path.sep))


if __name__ == '__main__':
    main()
