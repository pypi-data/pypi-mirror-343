from dataclasses import dataclass
from typing import Literal

from gw_certificate.common.debug import debug_print
from gw_certificate.interface.mqtt import Serialization
from gw_certificate.ag.ut_defines import GW_CONF, GW_API_VERSION

@dataclass
class GWCapabilities:
    tagMetadataCouplingSupported: bool = False
    downlinkSupported: bool = False
    bridgeOtaUpgradeSupported: bool = False
    fwUpgradeSupported: bool = False
    geoLocationSupport: bool = False
    
    @staticmethod
    def get_capabilities():
        return list(GWCapabilities.__dataclass_fields__.keys())
    
    def set_capability(self, capability, value:bool):
        assert capability in GWCapabilities.get_capabilities(), f'{capability} is not a valid capability'
        setattr(self, capability, value)

class ConfigurationData():
    """
    Hold variables which values must be shared between different tests.
    """
    def __init__(self):
        self.status_msg = None
        self.api_version = None
    
    def status_msg_set(self, status_msg, ser: Serialization):
        if not isinstance(status_msg, dict):
            debug_print('Status message should be a dict!')
            return

        self.status_msg = status_msg
        if ser == Serialization.PB:
            self.api_version = status_msg.get(GW_API_VERSION)
        else:
            conf = status_msg.get(GW_CONF, {})
            self.api_version = conf.get(GW_API_VERSION)
            if isinstance(self.api_version, str):
                self.api_version = int(self.api_version)

    def status_msg_get(self):
        return self.status_msg
    
    def is_acl_supported(self):
        API_VERSION_SUPPORT_ACL = 205

        if self.api_version != None and self.api_version >= API_VERSION_SUPPORT_ACL:
            return True
        return False