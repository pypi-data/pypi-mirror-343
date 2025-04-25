import isgb

from abc import ABC, abstractmethod

from sgb.collections import Any, Result, Callable
from sgb.service.interface import ClientBase, IClientBase
from sgb.service.consts import SERVICE_ROLE


class IActionDamewareClient(ABC, IClientBase):

    @abstractmethod
    def connect(self, host: str) -> bool:
        pass


SR = SERVICE_ROLE.DAMEWARE


class DamewareClient(ClientBase):

    class ACTION(IActionDamewareClient, ClientBase):

        def call(
            self,
            command: str,
            parameters: tuple[
                Any,
                ...,
            ],
        ) -> Result:
            return super().call(SR, command, parameters)

        def call_for_result(
            self,
            command: str,
            parameters: tuple[
                Any,
                ...,
            ],
            class_type_holder: Any | Callable[[Any], Any] | None = None,
        ) -> Result:
            return super().call_for_result(SR, command, parameters, class_type_holder)

        def connect(self, host: str) -> bool:
            return self.call("connect", (host,), bool)
