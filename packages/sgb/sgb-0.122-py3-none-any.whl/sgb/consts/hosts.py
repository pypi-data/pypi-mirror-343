import isgb

from enum import Enum
from sgb.collections import Host
from sgb.tools import StringTool, DataTool, first
from sgb.consts.community import COMMUNITY
from sgb.consts.server_role import SERVER_ROLE


class HOSTS(Enum):

    @property
    def NAME(self) -> str:
        return self.value.name

    @property
    def IP(self) -> str | None:
        return self.value.ip

    @property
    def ALIAS(self) -> str:
        return self.value.alias

    @staticmethod
    def get_by(host_name: str) -> Host | None:
        return first(
            DataTool.filter(
                lambda data: StringTool.contains(data.name, host_name, True),
                HOSTS,
            )
        )

    SPHERA_DC1 = Host("vld-np-dc1", "dc1")

    AD = SPHERA_DC1

    SPHERE_DC2 = Host("vld-np-dc2", "dc2")

    DEVELOPER = Host("vld-np-sgb-46")

    SKYPE = Host("vld-np-skype")

    SPHERE_PBX = Host("vld-np-pbx")

    HAPK_PBX = Host("krb-nv-pbx")

    PK_PBX = Host("vld-al-pbx")

    GAS_PBX = Host("trc-ml-pbx")

    AGMZ_PBX = Host("art-kr-pbx")

    MKUS_PBX = Host("us-mir-pbx")

    DAME_WARE = DEVELOPER

    EXECUTOR = DEVELOPER

    PASSWORD = DEVELOPER

    ROUTER = DEVELOPER

    SSH = DEVELOPER


class HOST_MAP:

    values: dict[HOSTS, tuple[SERVER_ROLE, COMMUNITY | tuple[COMMUNITY, ...]]] = {
        HOSTS.AGMZ_PBX: (SERVER_ROLE.TELEPHONY, (COMMUNITY.AGMZ, COMMUNITY.TD)),
        HOSTS.SPHERE_PBX: (SERVER_ROLE.TELEPHONY, COMMUNITY.SPHERE),
        HOSTS.HAPK_PBX: (SERVER_ROLE.TELEPHONY, COMMUNITY.HAPK),
        HOSTS.GAS_PBX: (SERVER_ROLE.TELEPHONY, COMMUNITY.GAS),
        HOSTS.PK_PBX: (SERVER_ROLE.TELEPHONY, COMMUNITY.PK),
        HOSTS.MKUS_PBX: (SERVER_ROLE.TELEPHONY, COMMUNITY.MKUS),
    }

    @staticmethod
    def by(server_role: SERVER_ROLE, community: COMMUNITY) -> Host | None:
        for host in HOST_MAP.values:
            value: tuple[SERVER_ROLE, COMMUNITY | tuple[COMMUNITY, ...]] = (
                HOST_MAP.values[host]
            )
            if (
                value[0] == server_role and community in value[1]
                if isinstance(value[1], tuple)
                else community == value[1]
            ):
                return host.value
        return None
