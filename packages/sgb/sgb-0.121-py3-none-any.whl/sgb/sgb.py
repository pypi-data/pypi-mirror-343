import isgb

from sgb.tools import OSTool, n, j_s, e, ne
import os, sys

class SYS(OSTool):

        use_virtual_environment: nbool = None

        @staticmethod
        def python_executable(host: nstr = None) -> nstr:
            return (
                sys.executable
                if SGB.SYS.host_is_local(host)
                else SGB.EXECUTOR.python_for_result(
                    ("import sys", "print(sys.executable)"),
                    host,
                    SGB.SYS.is_linux(host),
                )
            )

        @staticmethod
        def is_virtual_environment() -> bool:
            if n(SGB.SYS.use_virtual_environment):
                return sys.prefix != sys.base_prefix
            return SGB.SYS.use_virtual_environment



        @staticmethod
        @cache
        def host_is_local(value: nstr) -> nbool:
            try:
                return e(value) or SGB.SYS.hosts_are_equal(SGB.SYS.host(), value)
            except socket.gaierror as error:
                return None

        @staticmethod
        def hosts_are_equal(host1: str, host2: str) -> nbool:
            try:
                return socket.gethostbyname(host1) == socket.gethostbyname(host2)
            except socket.gaierror as error:
                return None

        @staticmethod
        def make_sudo(command: str, password: str) -> str:
            return j_s(("echo -e", password, "| sudo -S", command))

        @staticmethod
        @cache
        def python_version(host: nstr = None) -> nstr:
            return SGB.EXECUTOR.python_version(host)

        @staticmethod
        def python_exists(host: nstr = None) -> bool:
            return ne(SGB.SYS.python_version(host))

        @staticmethod
        @cache
        def name(host: nstr = None) -> nstr:
            if SGB.SYS.host_is_local(host):
                return platform.system()
            result: nstr = SGB.EXECUTOR.python_for_result(
                "import platform;print(platform.system())", host
            )
            return None if n(result) else result.strip()

        @staticmethod
        @cache
        def is_linux(host: nstr = None) -> bool:
            return SGB.SYS.name(host) == "Linux"

        @staticmethod
        def get_login() -> str:
            return os.getlogin()

        @staticmethod
        def pid() -> int:
            return OSTool.pid()

        @staticmethod
        def environment_variable(name: str) -> str:
            return os.getenv(name)

        @staticmethod
        def os_name() -> str:
            return SGB.SYS.environment_variable("OS")

        @staticmethod
        def domain_dns() -> str:
            return lw(SGB.SYS.environment_variable("USERDNSDOMAIN"))

        @staticmethod
        def domain() -> str:
            return lw(SGB.SYS.environment_variable("USERDOMAIN"))

        @staticmethod
        def kill_process(
            name_or_pid: str | int,
            via_standart_tools: bool = True,
            show_output: bool = False,
        ) -> bool:
            return SGB.EXECUTOR.kill_process(
                name_or_pid, None, via_standart_tools, show_output
            )

        @staticmethod
        def kill_process_by_port(
            value: int,
        ) -> nbool:
            return SGB.EXECUTOR.kill_process_by_port(value)