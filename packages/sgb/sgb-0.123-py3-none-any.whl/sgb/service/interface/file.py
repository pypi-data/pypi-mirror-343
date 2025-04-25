import isgb

from abc import ABC, abstractmethod

from sgb.consts import CHARSETS
from sgb.collections import strlist, Host
from sgb.tools import n, nl, j_nl, PathTool, OSTool
from sgb.service.interface.ssh import IActionSSHClient


class IActionFile(ABC):

    @abstractmethod
    def copy_file(
        self,
        source_host: str | Host | None,
        source_file_path: str,
        target_host: str | Host,
        target_file_path: str,
    ) -> bool:
        pass

    @abstractmethod
    def write_content_for_host(
        self,
        file_path: str,
        host: str | Host,
        content: str | strlist,
        encoding: str = CHARSETS.UTF8,
    ) -> bool:
        pass


class File:

    class ACTION(IActionFile):

        def __init__(self, ssh_action_client: IActionSSHClient):
            self.ssh_client = ssh_action_client

        def write_content_for_host(
            self,
            file_path: str,
            host: str | Host,
            content: str | strlist,
            encoding: str = CHARSETS.UTF8,
        ) -> bool:
            if isinstance(content, (tuple, list)):
                content = nl(j_nl(content), reversed=True)
            try:
                with open(
                    PathTool.resolve(file_path, Host.name(host)), "a", encoding=encoding
                ) as file:
                    file.write(content)
            except Exception as error:
                return False
            return True

        def copy_file(
            self,
            source_host: str | Host | None,
            source_file_path: str,
            target_host: str | Host,
            target_file_path: str,
        ) -> bool:
            source_host = OSTool.host() if n(source_host) else Host.name(source_host) 
            target_host = Host.name(target_host)
            source_file_path = PathTool.resolve(source_file_path, source_host)
            return self.ssh_client.copy_file(
                source_host, target_host, source_file_path, target_file_path
            )
