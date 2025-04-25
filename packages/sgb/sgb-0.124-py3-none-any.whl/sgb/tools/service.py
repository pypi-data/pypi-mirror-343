import isgb

from sgb.consts import CONST
from sgb.collections import nstr
from sgb.tools import (
    j,
    e,
    n,
    ne,
    OSTool,
    DataTool,
    NetworkTool,
    ParameterList,
)
from sgb.service.consts import (
    SERVICE_ROLE,
    SUPPORT_NAME_PREFIX,
    EVENT_LISTENER_NAME_PREFIX,
)


from sgb.service.collections import (
    Subscribtion,
    ServiceInformation,
    ServiceDescription,
    SubscribtionResult,
    ServiceDescriptionBase,
)

from sgb.service.consts import SERVICE_COMMAND as SC


import grpc
from enum import Enum
from abc import ABC, abstractmethod


class IRootSupporter(ABC):

    @abstractmethod
    def add_isolated_arg(self) -> bool:
        pass

    @abstractmethod
    def error_handler(
        self,
        description: ServiceDescriptionBase,
        exception: grpc.RpcError,
        code: tuple,
        details: str,
        command: str,
    ) -> None:
        pass

    @abstractmethod
    def isolated_arg(self) -> nstr:
        pass

    @abstractmethod
    def service_header(self, information: ServiceInformation) -> None:
        pass

    @abstractmethod
    def description_by_service_command(self, value: SC) -> ServiceDescription | None:
        pass

    @abstractmethod
    def error_detect_handler(
        exception: BaseException,
        host: nstr = None,
        argument_list: list[str] | None = None,
    ) -> None:
        pass

    @abstractmethod
    def service_was_not_started(
        self, service_information: ServiceInformation, error: str
    ) -> None:
        pass


class IServiceCollection(ABC):

    @abstractmethod
    def request(self, client) -> None:
        pass

    @abstractmethod
    def remove_service(self, value: ServiceDescriptionBase) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass

    @abstractmethod
    def get(
        self,
        key_description: ServiceDescription | None = None,
    ) -> dict[ServiceDescriptionBase, ServiceInformation] | ServiceInformation | None:
        pass

    @abstractmethod
    def update(
        self,
        value: ServiceDescriptionBase | list[ServiceDescriptionBase],
        add: bool = True,
        overwrite: bool = False,
    ) -> None:
        pass


class ServiceTool:

    @staticmethod
    def create_port(
        service_role_or_description: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> int:
        return (
            ServiceRoleTool.service_description(service_role_or_description).port
            or NetworkTool.next_free_port()
        )

    @staticmethod
    def create_host(
        service_role_or_description: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> str:
        description: ServiceDescription = ServiceRoleTool.service_description(
            service_role_or_description
        )
        return (
            OSTool.host()
            if description.isolated or e(description.host)
            else description.host
        )

    @staticmethod
    def extract_parameter_list(value: ParameterList) -> ParameterList:
        return (
            ParameterList(value.get())
            if ServiceTool.has_subscribtion_result(value)
            else value
        )

    @staticmethod
    def create_event_listener_service_description(
        host: str, port: int
    ) -> ServiceDescription:
        return ServiceDescription(
            name=j(
                (EVENT_LISTENER_NAME_PREFIX, host, port),
                CONST.SPLITTER,
            ),
            description="Subscriber",
            host=host,
            port=port,
            auto_start=False,
            auto_restart=False,
        )

    @staticmethod
    def extract_service_information(
        value: dict | ServiceInformation,
    ) -> ServiceInformation:
        service_information: ServiceInformation = (
            DataTool.fill_data_from_source(ServiceInformation(), value)
            if isinstance(value, dict)
            else value
        )
        if ne(service_information.subscribtions):
            service_information.subscribtions = DataTool.fill_data_from_list_source(
                Subscribtion, service_information.subscribtions
            )
        return service_information

    @staticmethod
    def has_subscribtion_result(pl: ParameterList) -> bool:
        return (
            len(pl.values) == 2
            and DataTool.fill_data_from_source(
                SubscribtionResult(), pl.values[-1]
            ).checker
        )

    @staticmethod
    def is_service_as_listener(description: ServiceDescriptionBase) -> bool:
        return description.name.find(EVENT_LISTENER_NAME_PREFIX) == 0

    @staticmethod
    def is_service_as_support(description: ServiceDescriptionBase) -> bool:
        return description.name.find(SUPPORT_NAME_PREFIX) == 0


class ServiceRoleTool:

    @staticmethod
    def get(
        value: ServiceDescription | ServiceInformation | SERVICE_ROLE,
    ) -> SERVICE_ROLE | None:
        if isinstance(value, SERVICE_ROLE):
            return value
        for service_role in SERVICE_ROLE:
            if service_role.NAME.lower().replace("_", "") == value.name.lower():
                return service_role

    @staticmethod
    def service_description(
        value: Enum | str | ServiceDescriptionBase, get_source_description: bool = False
    ) -> ServiceDescriptionBase | None:
        def isolated_name(
            value: ServiceDescriptionBase | None,
        ) -> ServiceDescriptionBase | None:
            if n(value):
                return None
            value.name = (
                j((CONST.ISOLATED_ARG_NAME, value.name), CONST.SPLITTER)
                if value.isolated and value.name.find(CONST.ISOLATED_ARG_NAME) == -1
                else value.name
            )
            return value

        if isinstance(value, str):
            for service_role in SERVICE_ROLE:
                if ServiceRoleTool.service_description(service_role).name == value:
                    return isolated_name(service_role.value)
            return None
        if isinstance(value, ServiceDescriptionBase):
            return isolated_name(
                ServiceRoleTool.service_description(value.name)
                if get_source_description
                else value
            )
        return isolated_name(value.value)
