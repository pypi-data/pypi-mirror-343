import isgb

from sgb.collections import ServerRoleItem
from enum import Enum

class SERVER_ROLE(Enum):

    DC: ServerRoleItem = ServerRoleItem("domain controller", "dc")
    TELEPHONY: ServerRoleItem = ServerRoleItem("asterisk", "pbx")