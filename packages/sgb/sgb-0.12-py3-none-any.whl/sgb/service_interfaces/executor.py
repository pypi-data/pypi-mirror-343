import isgb

from abc import ABC, abstractmethod

from sgb.consts.errors import ServiceIsNotStartedError
from sgb.collections import Any, Result, Callable, nstr, strtuple
from sgb.consts.service import SERVICE_ROLE, SERVICE_COMMAND as SC
from sgb.service.interface import ServiceClient, ClientBase, IClientBase

from subprocess import CompletedProcess
from contextlib import contextmanager

SR = SERVICE_ROLE.EXECUTOR


class IResultExecutorClient(IClientBase, ABC):

    call_with_service: bool = False

    @abstractmethod
    def execute(
        self,
        command: strtuple | str,
        show_output: bool = False,
        capture_output: bool = False,
        command_as_text: bool = True,
        as_shell: bool = False,
        encoding: nstr = None,
    ) -> Result[CompletedProcess]:
        pass

    @abstractmethod
    @contextmanager
    def make_call_with_service(self, error_on_inaccessibility: bool = False):
        pass


class ExecutorClient(ClientBase):

    class RESULT(IResultExecutorClient, ClientBase):

        def __init__(self, service_client: ServiceClient | None = None):
            super().__init__(service_client)
            self.call_with_service = False

        def call_for_result(
            self,
            command: SC | str,
            parameters: tuple[
                Any,
                ...,
            ],
            class_type_holder: Any | Callable[[Any], Any] | None = None,
        ) -> Result:
            return super().call_for_result(SR, command, parameters, class_type_holder)

        @contextmanager
        def make_call_with_service(self, error_on_inaccessibility: bool = False):
            try:
                if self.active_service_client.check_on_availability(SR):
                    self.call_with_service = True
                else:
                    if error_on_inaccessibility:
                        ServiceIsNotStartedError()
                yield
            finally:
                self.call_with_service = False


        def execute(
            self,
            command: strtuple | str,
            show_output: bool = False,
            capture_output: bool = False,
            command_as_text: bool = True,
            as_shell: bool = False,
            encoding: nstr = None,
        ) -> Result[CompletedProcess]:
            return self.call_for_result(
                "execute",
                (
                    command,
                    show_output,
                    capture_output,
                    command_as_text,
                    as_shell,
                    encoding,
                ),
                lambda data: CompletedProcess(*data.values()),
            )
