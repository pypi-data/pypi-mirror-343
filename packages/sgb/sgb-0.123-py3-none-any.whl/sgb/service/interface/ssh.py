import isgb

from abc import ABC, abstractmethod

from sgb.consts import PYTHON
from sgb.service.consts import SERVICE_ROLE
from sgb.tools import j, j_s, escs, OSTool, EnumTool, PathTool
from sgb.service.interface import ClientBase, IClientBase
from sgb.collections import nstr, strlist, nbool, Any, Result, Callable, Host


class IActionSSHClient(ABC, IClientBase):

    @abstractmethod
    def mount_facade_for_linux_host(self, value: nstr = None) -> bool:
        pass

    @abstractmethod
    def copy_file(
        self,
        source_host: str | Host,
        target_host: str | Host,
        source_file_path: str,
        target_file_path: str,
        username: nstr = None,
        password: nstr = None,
    ) -> bool:
        pass


class IResultSSHClient(ABC, IClientBase):

    @abstractmethod
    def execute(
        self,
        command: str,
        host: str | Host,
        username: nstr = None,
        password: nstr = None,
        use_sudo: bool = False,
        in_background: bool = False,
    ) -> Result[strlist]:
        pass

    @abstractmethod
    def execute_python(
        self, command: tuple[str] | str, host: str, in_background: bool = False
    ) -> Result[strlist]:
        pass

    @abstractmethod
    def execute_python_file(
        self,
        value: str,
        host: str,
        in_background: bool = False,
        as_standalone: bool = False,
    ) -> Result[strlist]:
        pass

    @abstractmethod
    def get_certificate_information(
        self, host: str, username: nstr = None, password: nstr = None
    ) -> Result[nstr]:
        pass

    @abstractmethod
    def get_unix_free_space_information_by_drive_name(
        self,
        drive_name: str,
        host: str,
        username: nstr = None,
        password: nstr = None,
    ) -> Result[nstr]:
        pass


SR = SERVICE_ROLE.SSH


class SSHClient(ClientBase):

    class RESULT(IResultSSHClient, ClientBase):

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

        def execute(
            self,
            command: str,
            host: str | Host,
            username: nstr = None,
            password: nstr = None,
            use_sudo: bool = False,
            in_background: bool = False,
        ) -> Result[strlist]:
            return self.call_for_result(
                "execute",
                (
                    command,
                    host if isinstance(host, str) else EnumTool.get(host).name,
                    username,
                    password,
                    use_sudo,
                    in_background,
                ),
            )

        def execute_python(
            self, command: tuple[str] | str, host: str, in_background: bool = False
        ) -> Result[strlist]:
            return self.execute(
                j_s(
                    (
                        PYTHON.EXECUTOR,
                        PYTHON.COMMAND.FLAG,
                        escs(
                            j(command, ";") if isinstance(command, tuple) else command
                        ),
                    )
                ),
                host,
                in_background=in_background,
            )

        def execute_python_file(
            self,
            value: str,
            host: str,
            in_background: bool = False,
            as_standalone: bool = False,
        ) -> Result[strlist]:
            return self.execute(
                j_s(
                    (
                        None if as_standalone else PYTHON.EXECUTOR3,
                        value,
                    )
                ),
                host,
                in_background=in_background,
            )

        def get_certificate_information(
            self, host: str, username: nstr = None, password: nstr = None
        ) -> Result[nstr]:
            return self.call_for_result(
                "get_certificate_information",
                (host, username, password),
            )

        def get_unix_free_space_information_by_drive_name(
            self,
            drive_name: str,
            host: str,
            username: nstr = None,
            password: nstr = None,
        ) -> Result[nstr]:
            return self.call_for_result(
                "get_unix_free_space_information_by_drive_name",
                (drive_name, host, username, password),
            )

    class ACTION(IActionSSHClient, ClientBase):

        def call(
            self,
            command: str,
            parameters: tuple[
                Any,
                ...,
            ],
        ) -> bool:
            return super().call(SR, command, parameters)

        def mount_facade_for_linux_host(self, value: nstr = None) -> bool:
            return self.call(
                "mount_facade_for_linux_host",
                (value or OSTool.host(),),
            )

        def copy_file(
            self,
            source_host: str | Host,
            target_host: str | Host,
            source_file_path: str,
            target_file_path: str,
            username: nstr = None,
            password: nstr = None,
        ) -> bool:
            source_host = Host.name(source_host)
            target_host = Host.name(target_host)
            source_file_path = PathTool.resolve(source_file_path, source_host)
            return self.call(
                "copy_file",
                (target_host, source_file_path, target_file_path, username, password),
            )
