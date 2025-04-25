import isgb

from sgb.collections import nstr, nbool
from sgb.tools import j_s, escs, n

from dataclasses import dataclass

from typing import Any

import grpc


RPCError = grpc.RpcError


class NotImplemented(BaseException):
    pass


class OperationExit(BaseException):
    pass


class OperationCanceled(BaseException):
    pass


@dataclass
class Redirection(BaseException):
    arg: Any | None = None


class ZeroReached(BaseException):
    pass


class BarcodeNotFound(BaseException):

    def get_details(self) -> str:
        return "Штрих-код не распознан, попробуйте еще раз"


class NotFound(BaseException):

    def get_details(self) -> str:
        return self.args[0]

    def get_value(self) -> str:
        return self.args[1]


class IncorrectInputFile(BaseException):
    pass


class NotAccesable(BaseException):
    pass


@dataclass
class Error(BaseException):
    details: nstr = None
    code: tuple | None = None

class ServiceIsNotStartedError(Error):
    pass

class ERROR:

    class USER:

        @staticmethod
        def create_not_found_error(title: str, active: nbool, value: str) -> NotFound:
            start: nstr = None
            if n(active):
                start = "Пользователь"
            elif active:
                start = "Активный пользователь"
            else:
                start = "Неактивный пользователь"
            return NotFound(j_s((start, "с", title, escs(value), "не найден!")), value)

    class WORKSTATION:

        @staticmethod
        def create_not_found_error(title: str, value: str) -> NotFound:
            return NotFound(
                j_s(("Компьютер", "с", title, escs(value), "не найден!")), value
            )
