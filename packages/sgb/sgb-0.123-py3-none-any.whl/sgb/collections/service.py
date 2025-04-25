import isgb

from sgb.consts.hosts import HOSTS
from sgb.consts.service_commands import SERVICE_COMMAND
from sgb.collections import nstr, nint, nbool, strtuple, Host

from dataclasses import dataclass, field
from typing import Any
from enum import Enum


@dataclass
class ServiceDescriptionBase:
    name: nstr = None
    host: nstr = None
    port: nint = None
    service_path: nstr = None
    isolated: bool = False
    host_changeable: bool = True
    visible_for_admin: bool = True
    auto_start: bool = True
    auto_restart: bool = True
    run_from_system_account: bool = False
    python_executable_path: nstr = None
    version: nstr = None
    sgb_version: nstr = None
    parameters: Any = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, another):
        return (
            False
            if another is None
            else (
                self.name == another.name
                if isinstance(another, ServiceDescriptionBase)
                else self.name == another
            )
        )


@dataclass
class SubscribtionDescription:
    service_name: nstr = None
    service_command: SERVICE_COMMAND | str | None = None
    type: nint = None
    name: nstr = None


@dataclass
class Subscribtion(SubscribtionDescription):
    available: bool = False
    enabled: bool = False


@dataclass
class SubscribtionInformation(SubscribtionDescription):
    pass


@dataclass
class ServiceInformation(ServiceDescriptionBase):
    subscribtions: list[Subscribtion] = field(default_factory=list)
    pid: int = -1
    standalone: nbool = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, another: Any):
        return (
            False
            if another is None
            else (
                self.name == another.name
                if isinstance(another, ServiceDescriptionBase)
                else self.name == another
            )
        )


@dataclass
class ServiceDescription(ServiceDescriptionBase):
    description: nstr = None
    login: nstr = None
    password: nstr = None
    commands: tuple[SERVICE_COMMAND | str, ...] | None = None
    use_standalone: bool = False
    standalone_name: nstr = None
    support_servers: strtuple | None = None
    packages: strtuple | None = None

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, another):
        return (
            False
            if another is None
            else (
                self.name == another.name
                if isinstance(another, ServiceDescriptionBase)
                else self.name == another
            )
        )


@dataclass
class SubscriberInformation:
    type: nint = None
    name: nstr = None
    available: bool = True
    enabled: bool = True
    service_information: ServiceDescriptionBase | None = None


@dataclass
class SubscribtionResult:
    result: Any = None
    type: int = 0
    checker: bool = False


class ServiceRoleItem(Enum):

    @property
    def value(self) -> ServiceDescription:
        return super().value

    @property
    def host(self) -> str | None:
        return self.value.host

    @property
    def standalone_name(self) -> str | None:
        return self.value.standalone_name

    @host.setter
    def host(self, value: str | HOSTS | Host) -> None:
        if isinstance(value, str):
            self.value.host = value
        elif isinstance(value, (HOSTS, Host)):
            self.host = value.value

    @property
    def NAME(self) -> str | None:
        return self.value.name
