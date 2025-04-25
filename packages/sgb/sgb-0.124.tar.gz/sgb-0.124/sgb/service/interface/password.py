import isgb

from abc import ABC, abstractmethod

from sgb.tools import ResultTool
from sgb.service.interface import ClientBase, IClientBase
from sgb.service.consts import SERVICE_ROLE, SERVICE_COMMAND
from sgb.collections import Any, Result, Callable, UsernameAndPassword


class IActionPasswordClient(ABC, IClientBase):

    @abstractmethod
    def save_credentials(
        self, username_and_logon: UsernameAndPassword, service: str
    ) -> bool:
        pass

    @abstractmethod
    def save_passwword(self, value: str, service: str) -> bool:
        pass


class IResultPasswordClient(ABC, IClientBase):

    @abstractmethod
    def get_credentials(self, service: str) -> Result[UsernameAndPassword]:
        pass

    @abstractmethod
    def get_password(self, service: str) -> Result[str]:
        pass


SR = SERVICE_ROLE.PASSWORD


class PasswordClient(ClientBase):

    class RESULT(IResultPasswordClient, ClientBase):

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

        def get_credentials(self, service: str) -> Result[UsernameAndPassword]:
            return self.call_for_result(
                SERVICE_COMMAND.get_credentials, (service,), UsernameAndPassword
            )

        def get_password(self, service: str) -> Result[str]:
            return ResultTool.map(
                lambda value: value.password, self.get_credentials(service)
            )

    class ACTION(IActionPasswordClient, ClientBase):

        def call(
            self,
            command: str,
            parameters: tuple[
                Any,
                ...,
            ],
        ) -> bool:
            return super().call(SR, command, parameters)

        def save_credentials(
            self, user_and_password: UsernameAndPassword, service: str
        ) -> bool:
            return self.call(
                SERVICE_COMMAND.save_credentials,
                (user_and_password.username, user_and_password.password, service),
            )

        def save_passwword(self, value: str, service: str) -> bool:
            return self.save_credentials(UsernameAndPassword(password=value), service)
