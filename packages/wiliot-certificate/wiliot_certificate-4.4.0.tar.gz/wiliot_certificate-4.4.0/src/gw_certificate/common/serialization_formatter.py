
from enum import Enum
from google.protobuf.json_format import MessageToDict, Parse, ParseError, ParseDict
import base64

from gw_certificate.interface.mqtt import Serialization
from gw_certificate.interface.if_defines import LOCATION
from gw_certificate.common import wltPb_pb2
from gw_certificate.ag.ut_defines import GW_CONF, ADDITIONAL, VERSION, BLE_VERSION, WIFI_VERSION, LAT, LNG
from gw_certificate.common.debug import debug_print

# helper defines
ACL_MODE =                      "mode"
ACL_BRIDGE_IDS =                "bridgeIds"
ACL_DENY =                      "deny"
ACL_ALLOW =                     "allow"
ACL_DENY_VALUE =                 0
ACL_ALLOW_VALUE =                1


class Configurable(Enum):
    ACL = "accessControlList"

class SerializationFormatter():
    def __init__(self, serialization:Serialization):
        self.serialization = serialization
    
    def is_pb(self):
        return self.serialization == Serialization.PB

    def cfg_param_set(self, received_status_msg: dict, param: Configurable, value):
        '''
        Since configuration paramters change between partners, we must use a received_status_msg to keep every parameter as is.
        In the future we may use a validation schema file or default.
        '''

        def gatewaystatus_to_downlink(gw_status_dict: dict, param_to_set: Configurable, value_to_set) -> wltPb_pb2.DownlinkMessage:
            gw_status = ParseDict(gw_status_dict, wltPb_pb2.GatewayStatus())
            gw_cfg = wltPb_pb2.GatewayConfig()

            if gw_status.HasField(VERSION):
                gw_cfg.version = gw_status.version
            if gw_status.HasField('bleSwVersion'):
                gw_cfg.bleSwVersion = gw_status.bleSwVersion
            if gw_status.HasField('interfaceSwVersion'):
                gw_cfg.interfaceSwVersion = gw_status.interfaceSwVersion
            if gw_status.HasField(LOCATION):
                gw_cfg.location.lat = gw_status.location.lat
                gw_cfg.location.lng = gw_status.location.lng
            
            for key, val in gw_status.config.items():
                if key != param_to_set:
                    gw_cfg.config[key].CopyFrom(val)
                else:
                    pb_gcvalue = wltPb_pb2.GatewayConfigValue()
                    if isinstance(value_to_set, int):
                        pb_gcvalue.integerValue = value_to_set
                    elif isinstance(value_to_set, float):
                        pb_gcvalue.numberValue = value_to_set
                    elif isinstance(value_to_set, str):
                        pb_gcvalue.stringValue = value_to_set
                    elif isinstance(value_to_set, bool):
                        pb_gcvalue.boolValue = value_to_set
                    elif isinstance(value_to_set, dict) and key == Configurable.ACL.value:
                        pb_gcvalue.aclValue.mode_allow = ACL_ALLOW_VALUE if value_to_set.get(ACL_MODE) == ACL_ALLOW else ACL_DENY_VALUE
                        ids_bytes = [bytes.fromhex(id) for id in value_to_set.get(ACL_BRIDGE_IDS)]
                        pb_gcvalue.aclValue.ids.extend(ids_bytes)
                    else:
                        debug_print(f"Unsupported value type for key '{key}': {type(val)}, protobuf cfg may be invalid")

                    gw_cfg.config[key].CopyFrom(pb_gcvalue)

            return wltPb_pb2.DownlinkMessage(gatewayConfig=gw_cfg)
            
        cfg_msg = received_status_msg.copy()
        if self.serialization == Serialization.PB:
            # In protobuf, we must convert the GatewayStatus to a DownlinkMessage with oneof=GatewayConfig
            cfg_msg = gatewaystatus_to_downlink(cfg_msg, param, value)
            return cfg_msg
        else:
            # JSON
            cfg_msg.setdefault(GW_CONF, {}).setdefault(ADDITIONAL, {})[param] = value
            debug_print(cfg_msg)
            return cfg_msg
    
    def pb_status_acl_bytes_to_hex_string(self, msg: dict) -> dict:
        brg_ids_bytes = msg.get('config', {}).get('accessControlList', {}).get('aclValue', {}).get('ids', {})
        brg_ids_ascii = []
        for brg_id in brg_ids_bytes:
            brg_ids_ascii.append(base64.b64decode(brg_id).hex().upper())
        if len(brg_ids_ascii) > 0:
            msg['config']['accessControlList']['aclValue']['ids'] = brg_ids_ascii
        return msg