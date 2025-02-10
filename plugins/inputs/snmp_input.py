# plugins/inputs/snmp_input.py
from pysnmp.hlapi import *
from ..metric import Metric

class SNMPInputPlugin:
    def __init__(self, host: str, community: str, oids: list):
        self.host = host
        self.community = community
        self.oids = oids

    def gather(self) -> list[Metric]:
        metrics = []
        for oid in self.oids:
            error_indication, error_status, error_index, var_binds = next(
                getCmd(
                    SnmpEngine(),
                    CommunityData(self.community),
                    UdpTransportTarget((self.host, 161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid)),
                )
            )
            if error_indication:
                print(f"SNMP error: {error_indication}")
            else:
                for var_bind in var_binds:
                    metrics.append(
                        Metric(
                            name="snmp",
                            tags={"oid": str(var_bind[0])},
                            fields={"value": str(var_bind[1])},
                        )
                    )
        return metrics