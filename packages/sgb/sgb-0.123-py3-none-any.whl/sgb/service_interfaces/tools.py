import isgb

from sgb.tools import n, DataTool
from contextlib import contextmanager
from sgb.consts.service import SERVICE_ROLE
from sgb.service.client import ServiceClient
from sgb.collections import Any, Result, Callable
from sgb.consts.errors import ServiceIsNotStartedError
from sgb.collections.service import ServiceDescriptionBase
from sgb.consts.service_commands import SERVICE_COMMAND as SC


class IClientBase:

    def set_service_client(self, value: ServiceClient) -> None:
        pass

    @contextmanager
    def with_service_client(self, value: ServiceClient):
        pass

    def call(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
    ) -> Result:
        pass

    def call_for_result(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
        class_type_holder: Any | Callable[[Any], Any] | None = None,
    ) -> Result:
        pass

    @property
    def active_service_client(self) -> ServiceClient:
        pass


class ClientBase(IClientBase):

    service_client: ServiceClient | None = None

    def __init__(self, service_client: ServiceClient | None = None):
        self.service_client = service_client

    def set_service_client(self, value: ServiceClient) -> None:
        self.service_client = value

    @contextmanager
    def with_service_client(self, value: ServiceClient):
        prev_client_service_client_static: ServiceClient = ClientBase.service_client
        prev_client_service_client: ServiceClient | None = self.service_client
        try:
            self.service_client = value
            yield True
        finally:
            self.service_client = prev_client_service_client

    def call_router(self, command: str, parameters: tuple[Any, ...]) -> Any:
        return DataTool.rpc_decode(
            self.internal_call(SERVICE_ROLE.ROUTER, command, parameters)
        )

    def call_router_for_result(
        self,
        command: str,
        parameters: tuple[Any, ...],
        class_type_holder: Any | Callable[[Any], Any] | None = None,
    ) -> Result:
        return DataTool.to_result(
            self.internal_call(SERVICE_ROLE.ROUTER, command, parameters),
            class_type_holder,
        )
    
    @property
    def active_service_client(self) -> ServiceClient:
        return self.service_client or ClientBase.service_client

    def internal_call(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
    ) -> str:
        try:
            return self.active_service_client.call_service(
                service_object, command, parameters
            )
        except ServiceIsNotStartedError:
            pass

    def call(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
    ) -> Any:
        return DataTool.rpc_decode(
            self.internal_call(service_object, command, parameters)
        )

    def call_for_result(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
        class_type_holder: Any | Callable[[Any], Any] | None = None,
    ) -> Result:
        return DataTool.to_result(
            self.internal_call(service_object, command, parameters),
            class_type_holder,
        )
