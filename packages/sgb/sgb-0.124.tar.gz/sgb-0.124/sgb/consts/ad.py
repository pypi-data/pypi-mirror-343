import isgb

from sgb.tools import j, j_p
from sgb.collections import strtuple, strlist
from sgb.consts.names import ACTIVE_DIRECTORY_USER_PROPERTIES

from enum import Enum


class AD:

    SPLITTER: str = "."
    OU: str = "OU="
    SEARCH_ATTRIBUTES: strlist = [
        ACTIVE_DIRECTORY_USER_PROPERTIES.LOGIN,
        ACTIVE_DIRECTORY_USER_PROPERTIES.NAME,
    ]
    SEARCH_ATTRIBUTE_DEFAULT: str = SEARCH_ATTRIBUTES[0]
    SEARCH_ALL_PATTERN: str = "*"
    LOCATION_SPLITTER: str = ":"
    TEMPLATED_USER_SERACH_TEMPLATE: str = j(("_", SEARCH_ALL_PATTERN, "_"))

    USER_ACCOUNT_CONTROL: strlist = [
        "SCRIPT",
        "ACCOUNTDISABLE",
        "RESERVED",
        "HOMEDIR_REQUIRED",
        "LOCKOUT",
        "PASSWD_NOTREQD",
        "PASSWD_CANT_CHANGE",
        "ENCRYPTED_TEXT_PWD_ALLOWED",
        "TEMP_DUPLICATE_ACCOUNT",
        "NORMAL_ACCOUNT",
        "RESERVED",
        "INTERDOMAIN_TRUST_ACCOUNT",
        "WORKSTATION_TRUST_ACCOUNT",
        "SERVER_TRUST_ACCOUNT",
        "RESERVED",
        "RESERVED",
        "DONT_EXPIRE_PASSWORD",
        "MNS_LOGON_ACCOUNT",
        "SMARTCARD_REQUIRED",
        "TRUSTED_FOR_DELEGATION",
        "NOT_DELEGATED",
        "USE_DES_KEY_ONLY",
        "DONT_REQ_PREAUTH",
        "PASSWORD_EXPIRED",
        "TRUSTED_TO_AUTH_FOR_DELEGATION",
        "RESERVED",
        "PARTIAL_SECRETS_ACCOUNT",
    ]

    DOMAIN_NAME: str = "sgb"
    DOMAIN_SUFFIX: str = "lan"
    DOMAIN_DNS: str = j_p((DOMAIN_NAME, DOMAIN_SUFFIX))
    #DOMAIN: str = DOMAIN_DNS
    #PATH_ROOT: str = j(("//", DOMAIN))

    ROOT_CONTAINER_DN: str = f"DC={DOMAIN_NAME},DC={DOMAIN_SUFFIX}"
    WORKSTATIONS_CONTAINER_DN: str = f"{OU}Workstations,{ROOT_CONTAINER_DN}"
    SERVERS_CONTAINER_DN: str = f"{OU}Servers,{ROOT_CONTAINER_DN}"
    ADMINS_CONTAINER_DN: str = f"{OU}Admins,{ROOT_CONTAINER_DN}"
    USERS_CONTAINER_DN_SUFFIX: str = f"Holding,{ROOT_CONTAINER_DN}"
    OUTSOURCE_USERS_CONTAINER_DN_SUFFIX: str = f"Outsourcing,{ROOT_CONTAINER_DN}"
    ACTIVE_USERS_CONTAINER_DN: strtuple = f"{OU}{USERS_CONTAINER_DN_SUFFIX}"
    OUTSOURCE_USERS_CONTAINER_DN: str = f"{OU}{OUTSOURCE_USERS_CONTAINER_DN_SUFFIX}"
    ALL_ACTIVE_USERS_CONTAINER_DN: strtuple = (
        ACTIVE_USERS_CONTAINER_DN,
        OUTSOURCE_USERS_CONTAINER_DN,
        ADMINS_CONTAINER_DN,
    )
    INACTIVE_USERS_CONTAINER_DN: str = f"{OU}User,{OU}Disabled,{ROOT_CONTAINER_DN}"
    GROUP_CONTAINER_DN: str = f"{OU}Groups,{ROOT_CONTAINER_DN}"
    PROPERTY_ROOT_DN: str = f"{OU}Property,{GROUP_CONTAINER_DN}"
    # PROPERTY_COMPUTER_DN: str = f"{OU}Computer,{PROPERTY_ROOT_DN}"
    PROPERTY_USER_DN: str = f"{OU}User,{PROPERTY_ROOT_DN}"
    JOB_POSITION_CONTAINER_DN: str = f"{OU}Job positions,{GROUP_CONTAINER_DN}"

    class ComputerProperties(Enum):
        Watchable = 1
        Shutdownable = 2
        Rebootable = 4
        DiskReportable = 8
        DiskReportableViaZabbix = 16

    class UserProperies(Enum):
        Jokeless = 1
        DoctorVisitless = 2
        HasLunchBreak = 4
        TimeTrackingless = 8
