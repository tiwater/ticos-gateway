#     Copyright 2020. Ticos
#
#     Licensed under the Apache License, Version 2.0 (the "License"];
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

import struct

from ticos_gateway.connectors.can.can_converter import CanConverter
from ticos_gateway.connectors.converter import log
from ticos_gateway.gateway.statistics_service import StatisticsService


class BytesCanUplinkConverter(CanConverter):
    @StatisticsService.CollectStatistics(start_stat_type='receivedBytesFromDevices',
                                         end_stat_type='convertedBytesFromDevice')
    def convert(self, configs, can_data):
        result = {"attributes": {},
                  "telemetry": {}}

        for config in configs:
            try:
                ticos_key = config["key"]
                ticos_item = "telemetry" if config["is_ts"] else "attributes"

                data_length = config["length"] if config["length"] != -1 else len(can_data) - config["start"]

                # The 'value' variable is used in eval
                if config["type"][0] == "b":
                    value = bool(can_data[config["start"]])
                elif config["type"][0] == "i" or config["type"][0] == "l":
                    value = int.from_bytes(can_data[config["start"]:config["start"] + data_length],
                                           config["byteorder"],
                                           signed=config["signed"])
                elif config["type"][0] == "f" or config["type"][0] == "d":
                    fmt = ">" + config["type"][0] if config["byteorder"][0] == "b" else "<" + config["type"][0]
                    value = struct.unpack_from(fmt,
                                               bytes(can_data[config["start"]:config["start"] + data_length]))[0]
                elif config["type"][0] == "s":
                    value = can_data[config["start"]:config["start"] + data_length].decode(config["encoding"])
                elif config["type"][0] == "r":
                    value = ""
                    for hex_byte in can_data[config["start"]:config["start"] + data_length]:
                        value += "%02x" % hex_byte
                else:
                    log.error("Failed to convert CAN data to Ticos %s '%s': unknown data type '%s'",
                              "time series key" if config["is_ts"] else "attribute", ticos_key, config["type"])
                    continue

                if config.get("expression", ""):
                    result[ticos_item][ticos_key] = eval(config["expression"],
                                                   {"__builtins__": {}} if config["strictEval"] else globals(),
                                                   {"value": value, "can_data": can_data})
                else:
                    result[ticos_item][ticos_key] = value
            except Exception as e:
                log.error("Failed to convert CAN data to Ticos %s '%s': %s",
                          "time series key" if config["is_ts"] else "attribute", ticos_key, str(e))
                continue
        return result
