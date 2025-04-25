from subprocess import DEVNULL, STDOUT, CompletedProcess
from contextlib import contextmanager, redirect_stdout
from pkg_resources import parse_version, working_set
from datetime import datetime, timedelta, date
from requests import ConnectTimeout, Response
from urllib.parse import unquote, quote_plus
from inspect import signature, Signature
from colorama import Back, Style, Fore
from collections import defaultdict
from prettytable import PrettyTable
from colorama.ansi import CSI
from transliterate import translit
from typing import Any, Callable
from concurrent import futures
from random import randrange
from threading import Thread
from string import Formatter
from grpc import StatusCode
from getpass import getpass
from io import StringIO
from json import dumps
from time import sleep
import importlib.util
from enum import Enum
import dataclasses
import subprocess
import traceback
import platform
import calendar
import colorama
import requests
import pathlib
import locale
import base64
import json
import uuid
import sys
import re
import os

import isgb

from sgb.service.collections import (
    ServiceDescription,
    ServiceInformation,
    SubscribtionResult,
    SubscriberInformation,
    ServiceDescriptionBase,
)
from sgb.service.client import IService
from sgb.service.consts import SERVICE_ROLE
from sgb.tools.service import (
    ServiceTool,
    IRootSupporter,
    ServiceRoleTool,
    IServiceCollection,
)
from sgb.service.interface.executor import IResultExecutorClient, ExecutorClient


from sgb.tools import *
from sgb.consts import *
from sgb.consts.ad import *
from sgb.collections import *
from sgb.consts.file import *
from sgb.consts.paths import *
from sgb.consts.hosts import *
from sgb.consts.names import *
from sgb.consts.style import *
from sgb.consts.errors import *
from sgb.consts.community import *
from sgb.consts.password import *
from sgb.consts.argument import *
from sgb.consts.python import PYTHON
from sgb.consts.events import Events
from sgb.consts.settings import SETTINGS
from sgb.consts.rpc import RPC as CONST_RPC
from sgb.consts.telephone import TELEPHONE_POOL
from sgb.service.consts import SUPPORT_NAME_PREFIX, SERVICE_COMMAND

from sgb.tools.service import ServiceTool
from sgb.service.interface import ClientBase
from sgb.service.client import ServiceClient
from sgb.service.interface.ad import (
    UserClient,
    ComputerClient,
    ICheckUserClient,
    IActionUserClient,
    WorkstationClient,
    IResultUserClient,
    IResultComputerClient,
    IResultWorkstationClient,
)
from sgb.service.interface.file import IActionFile, File
from sgb.service.interface.ssh import IResultSSHClient, IActionSSHClient, SSHClient
from sgb.service.interface.skype import IResultSkypeBusinessClient, SkypeBusinessClient
from sgb.service.interface.password import IActionPasswordClient, IResultPasswordClient, PasswordClient


BM = BitMask


class ActionWorkstationClientExtended(WorkstationClient.ACTION):

    def connect(
        self,
        source_login: str,
        source_password: str,
        source_host_name_or_ip: str,
        target_host_name_or_ip: nstr = None,
    ) -> bool:
        result: list[bool] | None = self.call_router(
            "connect",
            (
                source_login,
                source_password,
                source_host_name_or_ip,
                target_host_name_or_ip,
            ),
        )
        return DataTool.if_not_empty(result, lambda data: first(data), False)


class ServiceListener(IClosable):

    def __init__(self):
        self.service: IService | None = None
        self.service_command_list: strlist | None = None
        self.host: str = OSTool.host()
        self.port: int = NetworkTool.next_free_port()

    def listen_for(
        self,
        service_command_list: strlist,
        handler: Callable[[str, ParameterList, IClosable], Any],
    ) -> None:
        self.service_command_list = service_command_list

        def service_starts_handler(service: IService) -> None:
            self.service = service
            for service_command in service_command_list:
                service.subscribe_on(service_command)

        SGB.SERVICE.serve(
            ServiceTool.create_event_listener_service_description(self.host, self.port),
            lambda command_name, pl: handler(command_name, pl, self),
            service_starts_handler,
            show_output=True,
        )

    def close(self) -> None:
        service: IService = nnt(self.service)
        service.unsubscribe(self.service_command_list)
        SGB.SERVICE.stop(service.description, False)


class RootSuppport(IRootSupporter):

    def add_isolated_arg(self) -> bool:
        return SGB.session.add_isolated_arg()

    def isolated_arg(self) -> nstr:
        return SGB.session.isolated_arg()

    def service_header(self, information: ServiceInformation) -> None:
        SGB.output.service_header(information)
        SGB.output.good("Service was started!")

    def description_by_service_command(
        self, value: SERVICE_COMMAND
    ) -> ServiceDescription | None:
        return SGB.SERVICE.description_by_service_command(value)

    def error_detect_handler(
        exception: BaseException,
        host: nstr = None,
        argument_list: strlist | None = None,
    ) -> None:
        SGB.ERROR.global_except_hook(exception, host, argument_list)

    def error_handler(
        self,
        description: ServiceDescriptionBase,
        exception: grpc.RpcError,
        code: tuple,
        details: str,
        command: SERVICE_COMMAND | str,
    ) -> None:
        if code == StatusCode.UNAVAILABLE:
            if SGB.ERROR.notify_about_error:
                SGB.output.error("Error:")
                with SGB.output.make_indent(1):
                    for item in details.splitlines():
                        parts: strlist = item.split(": ")
                        if len(parts) > 1:
                            SGB.output.value(
                                parts[0],
                                SGB.output.red_str(j(parts[1:], "; ")),
                            )
                        else:
                            SGB.output.write_line(parts[0])
            return
        elif (
            code == StatusCode.DEADLINE_EXCEEDED
            or details.lower().find("stream removed") != -1
        ):
            return
        else:
            if SGB.ERROR.notify_about_error:
                SGB.EVENT.send(
                    Events.ERROR,
                    (
                        SGB.SYS.host(),
                        SGB.ERROR.create_header(exception.details),
                        str(exception),
                        details,
                    ),
                )
            raise Error(exception.details(), code) from None

    def service_was_not_started(
        self, service_information: ServiceInformation, error: str
    ) -> None:
        SGB.EVENT.service_was_not_started(service_information, error)


class SGBThread(Thread):

    autostart: bool = True

    def __init__(
        self,
        target: Callable,
        auto_start: bool = autostart,
        group=None,
        name=None,
        args=(),
        kwargs=None,
        *,
        daemon=None,
    ):
        def local_target(*args) -> None:
            with SGB.ERROR.detect():
                target(*args)

        super().__init__(
            group=group,
            target=local_target,
            name=name,
            args=args,
            kwargs=kwargs,
            daemon=daemon,
        )
        if auto_start:
            self.start()


class OutputStubAbstract:

    def b(self, value: str) -> str:
        raise NotImplemented()

    def i(self, value: str) -> str:
        raise NotImplemented()


class OutputStub(OutputStubAbstract):

    def b(self, value: Any) -> str:
        return str(value)

    def i(self, value: Any) -> str:
        return str(value)

    def set_to(self, value: OutputStubAbstract) -> None:
        value.b = self.b
        value.i = self.i


class OutputAbstract:

    @contextmanager
    def make_indent(self, value: int, additional: bool = False):
        raise NotImplemented()

    def set_indent(self, count: int = 1) -> None:
        raise NotImplemented()

    def bold(self, value: str) -> str:
        raise NotImplemented()

    def paragraph(self, caption: str) -> None:
        raise NotImplemented()

    def reset_indent(self) -> None:
        raise NotImplemented()

    def restore_indent(self) -> None:
        raise NotImplemented()

    def init(self) -> None:
        raise NotImplemented()

    def text_color_str(self, color: int, text: str) -> str:
        raise NotImplemented()

    def text_black_str(self, text: str) -> str:
        raise NotImplemented()

    def set_title(self, value: str) -> None:
        raise NotImplemented()

    def color_str(
        self,
        color: int,
        text: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> str:
        raise NotImplemented()

    def color(
        self,
        color: int,
        text: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> None:
        raise NotImplemented()

    def write_line(self, text: str) -> None:
        raise NotImplemented()

    def index(
        self,
        text: str,
        min_value: nint = None,
        max_value: nint = None,
    ) -> None:
        raise NotImplemented()

    def indexed_item(
        self,
        index: int,
        text: str,
        min_value: nint = None,
        max_value: nint = None,
    ) -> None:
        raise NotImplemented()

    def indexed_item_str(
        self,
        index: nint,
        text: str,
        min_value: nint = None,
        max_value: nint = None,
    ) -> str:
        raise NotImplemented()

    def index_str(
        self,
        caption: str,
        min_value: int,
        max_value: int,
    ) -> str:
        raise NotImplemented()

    def input(self, caption: str) -> None:
        raise NotImplemented()

    def input_str(
        self,
        caption: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> str:
        raise NotImplemented()

    def value(self, caption: str, value: str, text_before: nstr = None) -> None:
        raise NotImplemented()

    def get_action_value(
        self, caption: str, value: str, show: bool = True
    ) -> ActionValue:
        raise NotImplemented()

    def head(self, caption: str) -> None:
        raise NotImplemented()

    def head1(self, caption: str) -> None:
        raise NotImplemented()

    def head2(self, caption: str) -> None:
        raise NotImplemented()

    def new_line(self) -> None:
        raise NotImplemented()

    def separated_line(self) -> None:
        self.new_line()

    def error_str(self, caption: str) -> str:
        raise NotImplemented()

    def error(self, caption: str) -> None:
        raise NotImplemented()

    def notify_str(self, caption: str) -> str:
        raise NotImplemented()

    def notify(self, caption: str) -> None:
        raise NotImplemented()

    def good_str(self, caption: str) -> str:
        raise NotImplemented()

    def good(self, caption: str) -> None:
        raise NotImplemented()

    def green_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def green(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def yellow_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def yellow(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def black_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def black(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def white_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def white(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def draw_line(
        self, color: str = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80
    ) -> None:
        raise NotImplemented()

    def line(self) -> None:
        raise NotImplemented()

    def magenta_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def magenta(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def cyan(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def cyan_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def red(self, text: str, text_before: nstr = None, text_after: nstr = None) -> None:
        raise NotImplemented()

    def red_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def blue(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def blue_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def bright(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        raise NotImplemented()

    def bright_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        raise NotImplemented()

    def get_number(self, value: int) -> str:
        raise NotImplemented()

    @contextmanager
    def make_separated_lines(self):
        yield True

    def write_result(
        self,
        result: Result[T],
        use_index: bool = True,
        item_separator: str = nl(),
        empty_result_text: str = "Не найдено",
        separated_result_item: bool = True,
        label_function: Callable[[Any, int], str] | None = None,
        data_label_function: (
            Callable[[int, FieldItem, Result[T], Any], tuple[bool, str]] | None
        ) = None,
        title: nstr = None,
    ) -> None:
        raise NotImplemented()

    @contextmanager
    def make_send_to_group(self, group: CONST.MESSAGE.WHATSAPP.GROUP):
        raise NotImplemented()


class UserOutputAbstract:
    def result(
        self,
        result: Result[list[User]],
        caption: nstr = None,
        use_index: bool = False,
        root_location: str = AD.ALL_ACTIVE_USERS_CONTAINER_DN,
    ) -> None:
        raise NotImplemented()

    def get_formatted_given_name(self, value: nstr = None) -> str:
        return value


class WorkstationOutputAbstract:

    def label_function(self, workstation: Workstation, index: int) -> str:
        return NotImplemented()


class OutputExtendedAbstract:

    def sgb_title(self) -> None:
        raise NotImplemented()

    def service_header(self, description: ServiceDescription) -> None:
        raise NotImplemented()

    def containers_for_result(self, result: Result, use_index: bool = False) -> None:
        raise NotImplemented()

    def table_with_caption_first_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable | None = None,
    ) -> None:
        raise NotImplemented()

    def table_with_caption_last_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable | None = None,
    ) -> None:
        raise NotImplemented()

    def table_with_caption(
        self,
        result: Any,
        caption: nstr = None,
        use_index: bool = False,
        modify_table_function: Callable | None = None,
        label_function: Callable | None = None,
    ) -> None:
        raise NotImplemented()

    @contextmanager
    def make_loading(self, loading_timeout: float = 1, text: nstr = None) -> None:
        raise NotImplemented()

    def template_users_for_result(self, data: dict, use_index: bool = False) -> None:
        raise NotImplemented()

    def clear_screen(self) -> None:
        raise NotImplemented()

    def write_video(self, caption: str, video_content: str) -> None:
        raise NotImplemented()

    def write_image(self, caption: str, image_content: str) -> bool:
        pass


class UserOutputBase(UserOutputAbstract):
    def __init__(self):
        self.parent: Output


class WorkstationOutputBase(WorkstationOutputAbstract):
    def __init__(self):
        self.parent: Output


class WorkstationOutput(WorkstationOutputBase):

    def label_function(self, workstation: Workstation, index: int) -> str:
        return (
            "Все"
            if n(workstation)
            else j(
                (
                    b(workstation.name),
                    ": ",
                    workstation.description,
                    (
                        None
                        if n(workstation.login)
                        else j((" ", s_b(workstation.login)))
                    ),
                )
            )
        )


class UserOutput(UserOutputBase):
    def result(
        self,
        result: Result[list[User]],
        caption: nstr = None,
        use_index: bool = False,
        root_location: str = AD.ALL_ACTIVE_USERS_CONTAINER_DN,
    ) -> None:
        data: list = DataTool.as_list(result.data)
        fields: FieldItemList = result.fields
        base_location_list: strlist = SGB.DATA.FORMAT.location_list(
            root_location, False
        )
        root_database_location: strlist = base_location_list[0:2]
        root_database_location.reverse()
        base_location = j(
            (
                j(root_database_location, "."),
                j(base_location_list[2:], AD.LOCATION_SPLITTER),
            ),
            AD.LOCATION_SPLITTER,
        )
        location_field = fields.get_item_by_name(FIELD_NAME_COLLECTION.DN)
        pevious_caption: str = location_field.caption
        location_field.caption = f"{location_field.caption} ({base_location})"

        def modify_data(field: FieldItem, user: User) -> str:
            if field.name == ACTIVE_DIRECTORY_USER_PROPERTIES.DN:
                return j(
                    DataTool.filter(
                        lambda x: x not in base_location_list,
                        SGB.DATA.FORMAT.location_list(user.distinguishedName),
                    ),
                    AD.LOCATION_SPLITTER,
                )
            if field.name == ACTIVE_DIRECTORY_USER_PROPERTIES.USER_ACCOUNT_CONTROL:
                return j_nl(
                    SGB.DATA.FORMAT.get_user_account_control_values(
                        user.userAccountControl
                    )
                )
            if field.name == ACTIVE_DIRECTORY_USER_PROPERTIES.DESCRIPTION:
                return user.description
            if field.name == ACTIVE_DIRECTORY_USER_PROPERTIES.NAME:
                return j_nl(user.name.split(" "))
            return None

        self.parent.table_with_caption(
            result,
            "Пользватели:" if len(data) > 1 else "Пользватель:",
            False,
            None,
            modify_data,
        )
        location_field.caption = pevious_caption


class InputAbstract:

    def input(
        self,
        caption: nstr = None,
        new_line: bool = True,
        check_function: Callable[[str], str] | None = None,
    ) -> str:
        raise NotImplemented()

    def polibase_person_card_registry_folder(
        self, value: nstr = None, title: nstr = None
    ) -> str:
        raise NotImplemented()

    def polibase_persons_by_any(
        self, value: nstr = None, title: nstr = None, select_all: bool = False
    ) -> list[PolibasePerson]:
        raise NotImplemented()

    def telephone_number(
        self, format: bool = True, telephone_prefix: str = CONST.TELEPHONE_NUMBER_PREFIX
    ) -> str:
        raise NotImplemented()

    def email(self) -> str:
        raise NotImplemented()

    def message(self, caption: nstr = None, prefix: nstr = None) -> str:
        raise NotImplemented()

    def description(self) -> str:
        raise NotImplemented()

    def login(self, check_on_exists: bool = False) -> str:
        raise NotImplemented()

    def indexed_list(
        self,
        caption: str,
        name_list: list[Any],
        caption_list: strlist,
        by_index: bool = False,
    ) -> str:
        raise NotImplemented()

    def indexed_field_list(self, caption: str, list: FieldItemList) -> str:
        raise NotImplemented()

    def date_period(
        self, start_date_value: nstr = None, end_date_value: nstr = None
    ) -> tuple[datetime, datetime]:
        raise NotImplemented()

    def index(
        self,
        caption: str,
        data: list[Any],
        label_function: Callable[[Any, int], str] | None = None,
    ) -> int:
        raise NotImplemented()

    def item_by_index(
        self,
        caption: str,
        data: list[Any],
        label_function: Callable[[Any, int], str] | None = None,
        filter_function: Callable[[Any, str], bool] | None = None,
    ) -> Any:
        raise NotImplemented()

    def tab_number(self, check: bool = True) -> str:
        raise NotImplemented()

    def password(
        self,
        secret: bool = True,
        check: bool = False,
        settings: PasswordSettings | None = None,
        is_new: bool = True,
    ) -> str:
        raise NotImplemented()

    def same_if_empty(self, caption: str, src_value: str) -> str:
        raise NotImplemented()

    def name(self) -> str:
        raise NotImplemented()

    def full_name(self, one_line: bool = False) -> FullName:
        raise NotImplemented()

    def confirm(
        self,
        text: str = " ",
        enter_for_yes: bool = False,
        yes_label: nstr = None,
        no_label: nstr = None,
        yes_checker: Callable[[str], bool] | None = None,
    ) -> bool:
        raise NotImplemented()

    def message_for_user_by_login(self, login: str) -> str:
        raise NotImplemented()

    def polibase_person_any(self, title: nstr = None) -> str:
        raise NotImplemented()

    def datetime(self, value: str) -> datetime:
        raise NotImplemented()

    def choose_file(
        self, use_search_request: nbool = None, force_fetch: nbool = None
    ) -> File:
        raise NotImplemented()


class WorkstationInputAbstract:

    def title_any(self, title: nstr = None) -> str:
        raise NotImplemented()

    def select(
        self,
        result: Result[list[Workstation]] | None = None,
        title: nstr = None,
        label_function: Callable[[Workstation, int], str] | None = None,
        sort_function: Callable[[Workstation], str] | None = None,
        filter_function: Callable[[Workstation, str], bool] | None = None,
        show_select_all: nbool = False,
    ) -> Result[list[Workstation]]:
        pass


class UserInputAbstract:
    def container(self) -> ADContainer:
        raise NotImplemented()

    def by_name(self) -> Result[User]:
        raise NotImplemented()

    def title_any(self, title: nstr = None) -> str:
        raise NotImplemented()

    def by_any(
        self,
        value: nstr = None,
        active: nbool = None,
        title: nstr = None,
        select_all: nbool = None,
    ) -> Result[list[User]]:
        raise NotImplemented()

    def telephone_number(
        self,
        value: nstr = None,
        active: nbool = None,
        title: nstr = None,
    ) -> User:
        raise NotImplemented()

    def template(self) -> User:
        raise NotImplemented()

    def search_attribute(self) -> str:
        raise NotImplemented()

    def search_value(self, search_attribute: str) -> str:
        raise NotImplemented()

    def generate_login(
        self,
        full_name: FullName,
        ask_for_remove_inactive_user_if_login_is_exists: bool = True,
        ask_for_use: bool = True,
    ) -> str:
        raise NotImplemented()

    def generate_password(
        self, once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT
    ) -> str:
        raise NotImplemented()


class UserInputBase(UserInputAbstract):
    def __init__(self):
        self.parent: InputBase = None


class WorkstationInputBase(WorkstationInputAbstract):

    def __init__(self):
        self.parent: InputBase = None


class InputBase(InputAbstract):
    def __init__(self):
        self.output: OutputBase
        self.user: UserInputBase
        self.workstation: WorkstationInputBase
        self.type: int = INPUT_TYPE.NO


class OutputBase(OutputAbstract, OutputExtendedAbstract):
    def __init__(
        self,
        user_output: UserOutputBase | None = None,
        workstation_output: WorkstationOutputBase | None = None,
    ):
        self.text_before: str = ""
        self.text_after: str = ""
        self.indent_symbol: str = " "
        self.indent_value: int = 0
        self.user: UserOutputBase | None = user_output
        if nn(user_output):
            self.user.parent = self
        self.workstation: WorkstationOutputBase | None = workstation_output
        if nn(workstation_output):
            self.workstation.parent = self
        self.personalize = False


class SessionAbstract:
    def run_forever_untill_enter_not_pressed(self) -> None:
        raise NotImplemented()

    def exit(self, timeout: float | None = None, message: nstr = None) -> None:
        raise NotImplemented()

    def get_login(self) -> str:
        raise NotImplemented()

    def get_user(self) -> User:
        raise NotImplemented()

    def user_given_name(self) -> str:
        raise NotImplemented()

    def start(self, login: str, notify: bool = True) -> None:
        raise NotImplemented()

    def hello(self, greeting: bool = True, fill_groups: bool = False) -> None:
        raise NotImplemented()

    @property
    def argv(self) -> strlist:
        raise NotImplemented()

    def arg(self, index: int = None, default_value: nstr = None) -> str:
        raise NotImplemented()

    @property
    def file_path(self) -> str:
        raise NotImplemented()

    @property
    def file_name(self) -> str:
        raise NotImplemented()

    def authenticate(self, exit_on_fail: bool = True) -> bool:
        raise NotImplemented()


class SessionBase(SessionAbstract):
    def __init__(
        self,
        input: InputBase | None = None,
        output: OutputBase | None = None,
        name: nstr = None,
        flags: int = 0,
    ):
        self.login: nstr = None
        self.ip: nstr = None
        self.user: User | None = None
        self.input: InputBase | None = input
        self.output: OutputBase | None = output
        self.name: nstr = name
        self.flags: int = flags

    @property
    def is_mobile(self) -> bool:
        return self.name == SESSION_TYPE.MOBILE

    @property
    def is_outside(self) -> bool:
        return self.name == SESSION_TYPE.OUTSIDE

    @property
    def is_web(self) -> bool:
        return self.name == SESSION_TYPE.WEB


class Session(SessionBase, ArgumentParserTool):

    def __init__(
        self, input: InputBase | None = None, output: OutputBase | None = None
    ):
        ArgumentParserTool.__init__(self)
        SessionBase.__init__(self, input, output)
        self.ip = SGB.SYS.host_ip()
        self.authenticated: bool = False

    @property
    def life_time(self) -> timedelta:
        return SGB.SERVICE.client.session_information.life_time

    def run_forever_untill_enter_not_pressed(self) -> None:
        try:
            self.output.green("Нажмите Ввод для выхода...")
            input()
        except KeyboardInterrupt:
            pass

    def exit(self, timeout: float | None = None, message: nstr = None) -> None:
        if nn(message):
            self.output.error(message)
        sleep(timeout or 5)
        exit()

    def get_login(self) -> str:
        if n(self.login):
            self.start(SGB.SYS.get_login())
        return self.login

    def get_user(self) -> User:
        if n(self.user):
            self.user = first(SGB.RESULT.USER.by_login(self.get_login()))
        return self.user

    @property
    def user_given_name(self) -> str:
        return FullNameTool.to_given_name(self.get_user().name)

    def start(self, login: str, notify: bool = True) -> None:
        if n(self.login):
            self.login = login
            if notify:
                SGB.EVENT.start_session()

    def hello(self, greeting: bool = True, fill_access_groups: bool = False) -> None:
        user: User = self.get_user()
        if n(user):
            self.output.error("Ты кто такой? Давай, до свидания...")
            self.exit()
            return
        if greeting:
            self.output.good(j_s(("Добро пожаловать,", user.name)))
            self.output.new_line()
        if fill_access_groups:
            self.fill_access_groups()

    def fill_access_groups(self) -> None:
        SGB.CHECK.ACCESS.action_for_all_groups(self, False, False, False, True)

    @property
    def file_path(self) -> str:
        return sys.argv[0]

    @property
    def argv(self) -> strlist:
        return sys.argv

    @property
    def is_executable(self) -> bool:
        return self.file_path.endswith(FILE.EXTENSION.EXE)

    @property
    def file_name(self) -> str:
        return PathTool.get_file_name(self.file_path)

    def authenticate(self, exit_on_fail: bool = True, once: bool = True) -> bool:
        try:
            if once and self.authenticated:
                return True
            self.output.green("Инициализация...")
            self.output.clear_screen()
            self.output.sgb_title()
            if SGB.SERVICE.check_on_availabllity(SERVICE_ROLE.AD):
                login: str = SGB.SYS.get_login()
                self.output.head1(
                    j(
                        (
                            FullNameTool.to_given_name(
                                SGB.RESULT.USER.by_login(login, cached=False).data.name
                            ),
                            " пожалуйста, пройдите аутентификацию...",
                        )
                    )
                )
                self.output.new_line()
                if not self.input.confirm(
                    j_s(("Использовать логин", escs(login))), True
                ):
                    login = SGB.input.login()
                password: str = SGB.input.password(is_new=False)
                if DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_ROLE.AD, "authenticate", (login, password)
                    )
                ):
                    self.authenticated = True
                    self.start(login, False)
                    self.fill_access_groups()
                    SGB.EVENT.login()
                    self.output.good(
                        self.output.text_black_str(
                            f"Добро пожаловать, {self.get_user().name}..."
                        )
                    )
                    return True
                else:
                    if exit_on_fail:
                        self.exit(5, "Неверный пароль или логин. До свидания...")
                    else:
                        return False
            else:
                self.output.error("Сервис аутентификации недоступен. До свидания...")
        except KeyboardInterrupt:
            self.exit(0, "Выход")


class Stdin:
    def __init__(self):
        self.data: nstr = None
        self.wait_for_data_input: bool = False
        self.interrupt_type: int = 0

    def is_empty(self) -> bool:
        return e(self.data)

    def set_default_state(self) -> None:
        self.interrupt_type = 0
        self.wait_for_data_input = False
        self.data = None


class Output(OutputBase, OutputStub):

    @contextmanager
    def make_indent(self, value: int, additional: bool = False):
        indent: int = self.indent
        try:
            self.set_indent([0, indent][additional] + value)
            yield True
        finally:
            self.set_indent(indent)

    def set_indent(self, value: int) -> None:
        self.indent_value = value
        self.text_before = self.indent_symbol * value

    def bold(self, value: str) -> str:
        return j((CSI, "1m", value, CSI, "22m"))

    def italics(self, value: str) -> str:
        return value

    def reset_indent(self) -> None:
        self.indent_value = 0
        self.text_before = ""

    @property
    def indent(self) -> int:
        return self.indent_value

    def restore_indent(self) -> None:
        self.set_indent(self.indent_value)

    def init(self) -> None:
        colorama.init()

    def text_color_str(self, color: str, text: str) -> str:
        return j((color, text, Fore.RESET))

    def text_black_str(self, text: str) -> str:
        return self.text_color_str(Fore.BLACK, text)

    def text_white_str(self, text: str) -> str:
        return self.text_color_str(Fore.WHITE, text)

    def color_str(
        self,
        color: int,
        text: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> str:
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        return j((text_before, color, " ", text, " ", Back.RESET, text_after))

    def color(
        self,
        color: int,
        text: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> None:
        self.write_line(self.color_str(color, text, text_before, text_after))

    def write_line(self, text: str) -> None:
        text = SGB.DATA.FORMAT.console_message(text)
        print(
            j_nl(
                DataTool.map(
                    lambda item: j((self.text_before, item)), text.splitlines()
                )
            )
        )

    @contextmanager
    def personalized(self):
        pass

    def indexed_item_str(
        self,
        index: nint,
        text: str,
        min_value: nint = None,
        max_value: nint = None,
    ) -> str:
        indent: str = ""
        if nn(max_value):
            indent = " " * (len(str(max_value)) - len(str(index)))
        return j((indent, text)) if n(index) else j((index, ". ", indent, text))

    def indexed_item(
        self,
        index: int,
        text: str,
        min_value: nint = None,
        max_value: nint = None,
    ) -> None:
        self.write_line(self.indexed_item_str(index, text, min_value, max_value))

    def index(
        self,
        caption: str,
        min_value: int,
        max_value: int,
    ) -> None:
        self.write_line(self.index_str(caption, min_value, max_value))

    def index_str(
        self,
        text: str,
        min_value: int,
        max_value: int,
    ) -> str:
        return j_s(
            (j((text, ", отправив число")), "(от", min_value, "до", j((max_value, ")")))
        )

    def input(self, caption: str) -> None:
        self.write_line(
            self.input_str(caption, self.text_before, text_after=CONST.SPLITTER)
        )

    def input_str(
        self,
        caption: str,
        text_before: nstr = None,
        text_after: nstr = None,
    ) -> str:
        return self.white_str(
            j((Fore.BLACK, caption, Fore.RESET)), text_before, text_after
        )

    def value(self, caption: str, value: str, text_before: nstr = None) -> None:
        text_before = text_before or self.text_before
        self.cyan(caption, text_before, j((": ", value)))

    def get_action_value(
        self, caption: str, value: str, show: bool = True
    ) -> ActionValue:
        if show:
            self.value(caption, value)
        return ActionValue(caption, value)

    def head(self, caption: str) -> None:
        self.cyan(self.text_black_str(caption))

    def head1(self, caption: str) -> None:
        self.magenta(caption)

    def head2(self, caption: str) -> None:
        self.yellow(self.text_color_str(Fore.BLACK, caption))

    def new_line(self) -> None:
        print()

    def separated_line(self) -> None:
        self.new_line()

    def error_str(self, caption: str) -> str:
        return self.red_str(caption)

    def error(self, caption: str) -> None:
        self.write_line(self.error_str(caption))

    def notify_str(self, caption: str) -> str:
        return self.yellow_str(caption)

    def notify(self, caption: str) -> None:
        self.write_line(self.notify_str(caption))

    def good_str(self, caption: str) -> str:
        return self.green_str(self.text_white_str(caption))

    def good(self, caption: str) -> str:
        self.write_line(self.good_str(caption))

    def green_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.GREEN, text, text_before, text_after)

    def green(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.green_str(text, text_before, text_after))

    def yellow_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.YELLOW, text, text_before, text_after)

    def yellow(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        text_before = text_before or self.text_before
        text_after = text_after or self.text_after
        self.write_line(self.yellow_str(text, text_before, text_after))

    def black_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.BLACK, text, text_before, text_after)

    def black(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.black_str(text, text_before, text_after))

    def white_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.WHITE, text, text_before, text_after)

    def white(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.white_str(text, text_before, text_after))

    def draw_line(
        self, color: int = Back.LIGHTBLUE_EX, char: str = " ", width: int = 80
    ) -> None:
        self.write_line("") if color is None else self.color(color, char * width)

    def line(self) -> None:
        self.new_line()
        self.draw_line(
            Back.WHITE, self.text_color_str(Fore.BLACK, CONST.NAME_SPLITTER), width=128
        )
        self.new_line()

    def magenta_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.LIGHTMAGENTA_EX, text, text_before, text_after)

    def magenta(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.magenta_str(text, text_before, text_after))

    def cyan(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.cyan_str(text, text_before, text_after))

    def cyan_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.CYAN, text, text_before, text_after)

    def red(self, text: str, text_before: nstr = None, text_after: nstr = None) -> None:
        self.write_line(self.red_str(text, text_before, text_after))

    def red_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.LIGHTRED_EX, text, text_before, text_after)

    def blue(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.blue_str(text, text_before, text_after))

    def blue_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Back.BLUE, text, text_before, text_after)

    def bright(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> None:
        self.write_line(self.bright_str(text, text_before, text_after))

    def bright_str(
        self, text: str, text_before: nstr = None, text_after: nstr = None
    ) -> str:
        return self.color_str(Style.BRIGHT, text, text_before, text_after)

    @staticmethod
    def get_number(value: int) -> str:
        return CONST.VISUAL.NUMBER_SYMBOLS[value]

    def paragraph(self, caption: str) -> None:
        self.head2(caption)

    @contextmanager
    def make_separated_lines(self):
        yield True

    @contextmanager
    def make_loading(self, show_delay: float = 1.0, text: nstr = None):
        thread: SGBThread | None = None
        try:

            def show_loading() -> None:
                sleep(show_delay)
                if nn(thread):
                    self.write_line(
                        j_s(
                            ("", CONST.VISUAL.WAIT, j((text or "Идёт загрузка", "...")))
                        )
                    )

            thread = SGBThread(show_loading)
            self.locked = True
            yield True
        finally:
            self.locked = False
            thread = None

    def write_result(
        self,
        result: Result[T],
        use_index: bool = True,
        item_separator: str = nl(),
        empty_result_text: str = "Не найдено",
        separated_result_item: bool = True,
        label_function: Callable[[Any, int], str | strlist] | None = None,
        data_label_function: (
            Callable[[int, FieldItem, T, Any], tuple[bool, str]] | None
        ) = None,
        title: nstr = None,
        separated_all: bool = False,
    ) -> None:
        data: list = DataTool.as_list(result.data)
        result_string_list: strlist | None = None
        if e(data):
            self.new_line()
            self.write_line(empty_result_text)
        else:
            if ne(title):
                self.write_line(b(title))
            with self.make_indent(2, True):
                for index, data_item in enumerate(data):
                    result_string_list = []
                    if use_index and len(data) > 1:
                        result_string_list.append(j((self.text_before, index + 1, ":")))
                    if n(label_function):
                        field: FieldItem
                        for field in result.fields.list:
                            if not field.visible:
                                continue
                            item_data_value: nstr = None
                            if isinstance(data_item, dict):
                                item_data_value = data_item[field.name]
                            elif dataclasses.is_dataclass(data_item):
                                item_data_value = data_item.__getattribute__(field.name)
                            item_data_value = (
                                item_data_value
                                if e(item_data_value)
                                else SGB.DATA.FORMAT.by_formatter_name(
                                    field.data_formatter, item_data_value
                                )
                                or field.data_formatter.format(data=item_data_value)
                            )
                            if e(item_data_value):
                                if data_label_function is None:
                                    continue
                            default_value_label_function: Callable[
                                [int, FieldItem, Result[T], Any], tuple[bool, str]
                            ] = lambda _, field, __, data_value: (
                                True,
                                j((b(field.caption), ": ", data_value)),
                            )
                            result_data_label_function: Callable[
                                [int, FieldItem, T, Any], tuple[bool, str]
                            ] = (data_label_function or default_value_label_function)
                            label_value_result: tuple[bool, nstr] = (
                                result_data_label_function(
                                    index, field, data_item, item_data_value
                                )
                            )
                            label_value: nstr = None
                            if nn(label_value_result[0]):
                                if label_value_result[0] == True:
                                    label_value = label_value_result[1]
                                    if n(label_value) and nn(field.default_value):
                                        label_value = field.default_value
                                else:
                                    label_value = default_value_label_function(
                                        None, field, None, item_data_value
                                    )[1]
                            if ne(label_value):
                                result_string_list.append(label_value)
                    else:
                        result_string_list += DataTool.as_list(
                            label_function(data_item, index)
                        )
                    if separated_result_item:
                        self.separated_line()
                    if separated_all:
                        with self.make_separated_lines():
                            for line in result_string_list:
                                self.write_line(line)
                    else:
                        self.write_line(j(result_string_list, item_separator))

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def sgb_title(self) -> None:
        self.cyan(self.text_white_str("░██████╗░██████╗░██████╗░"))
        self.cyan(self.text_white_str("██╔════╝██╔════╝░██╔══██╗"))
        self.cyan(self.text_white_str("╚█████╗░██║░░██╗░██████╦╝"))
        self.cyan(self.text_white_str("░╚═══██╗██║░░╚██╗██╔══██╗"))
        self.cyan(self.text_white_str("██████╔╝╚██████╔╝██████╦╝"))
        self.cyan(
            j(
                (
                    self.text_white_str("╚═════╝░░╚═════╝░╚═════╝░"),
                    self.text_black_str(j((" ", SGB.VERSION.value))),
                )
            )
        )
        self.new_line()

    """
    def rpc_service_header(self, host: str, port: int, description: str) -> None:
        self.blue("SGB service")
        self.blue(f"Version: {SGB.VERSION.value}")
        self.green(f"Service host: {host}")
        self.green(f"Service port: {port}")
        self.green(f"Service name: {description}")'
    """

    def service_header(self, information: ServiceInformation) -> None:
        self.clear_screen()
        self.new_line()
        self.sgb_title()
        self.blue("Service starting...")
        self.new_line()
        self.green(f"Service name: {information.name}")
        with self.make_indent(1):
            if information.standalone:
                self.magenta("Standalone")
            if information.isolated:
                self.blue("Isolated")
            self.value("Version", information.version)
            self.value("Host", SGB.DATA.FORMAT.domain(information.host))
            self.value("Port", information.port)
            self.value("PID process", information.pid)

    def containers_for_result(self, result: Result, use_index: bool = False) -> None:
        self.table_with_caption(result, "Подразделение:", use_index)

    def table_with_caption_first_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable = None,
    ) -> None:
        def modify_table(table: PrettyTable, caption_list: strlist):
            table.align[caption_list[int(use_index)]] = "c"

        self.table_with_caption(
            result, caption, use_index, modify_table, label_function
        )

    def table_with_caption_last_title_is_centered(
        self,
        result: Result,
        caption: str,
        use_index: bool = False,
        label_function: Callable = None,
    ) -> None:
        def modify_table(table: PrettyTable, caption_list: strlist):
            table.align[caption_list[-1]] = "c"

        self.table_with_caption(
            result, caption, use_index, modify_table, label_function
        )

    def table_with_caption(
        self,
        result: Any,
        caption: nstr = None,
        use_index: bool = False,
        modify_table_function: Callable | None = None,
        label_function: Callable | None = None,
    ) -> None:
        if caption is not None:
            self.cyan(caption)
        is_result_type: bool = isinstance(result, Result)
        field_list = (
            result.fields if is_result_type else ResultTool.unpack_fields(result)
        )
        data: Any = result.data if is_result_type else ResultTool.unpack_data(result)
        if e(data):
            self.error("Не найдено!")
        else:
            if not isinstance(data, list):
                data = [data]
            if len(data) == 1:
                use_index = False
            if use_index:
                field_list.list.insert(0, FIELD_COLLECTION.INDEX)
            caption_list: list = field_list.get_caption_list()

            def create_table(caption_list: strlist) -> PrettyTable:
                from prettytable.colortable import ColorTable, Themes

                table: ColorTable = ColorTable(caption_list, theme=Themes.OCEAN)
                table.align = "l"
                if use_index:
                    table.align[caption_list[0]] = "c"
                return table

            table: PrettyTable = create_table(caption_list)
            if modify_table_function is not None:
                modify_table_function(table, caption_list)
            for index, item in enumerate(data):
                row_data: list = []
                for field_item_obj in field_list.get_list():
                    field_item: FieldItem = field_item_obj
                    if field_item.visible:
                        if field_item.name == FIELD_COLLECTION.INDEX.name:
                            row_data.append(str(index + 1))
                        elif not isinstance(item, dict):
                            if label_function is not None:
                                modified_item_data = label_function(field_item, item)
                                if modified_item_data is None:
                                    modified_item_data = getattr(item, field_item.name)
                                row_data.append(
                                    DataTool.check(
                                        modified_item_data,
                                        lambda: modified_item_data,
                                        "",
                                    )
                                    if modified_item_data is None
                                    else modified_item_data
                                )
                            else:
                                item_data = getattr(item, field_item.name)
                                row_data.append(
                                    DataTool.check(item_data, lambda: item_data, "")
                                )
                        elif field_item.name in item:
                            item_data = item[field_item.name]
                            if label_function is not None:
                                modified_item_data = label_function(field_item, item)
                                row_data.append(
                                    item_data
                                    if modified_item_data is None
                                    else modified_item_data
                                )
                            else:
                                row_data.append(item_data)
                table.add_row(row_data)
            print(table)
            table.clear()

    def template_users_for_result(self, data: dict, use_index: bool = False) -> None:
        def data_handler(field_item: FieldItem, item: User) -> Any:
            filed_name = field_item.name
            if filed_name == FIELD_NAME_COLLECTION.DESCRIPTION:
                return item.description
            return None

        self.table_with_caption(
            data,
            "Шаблоны для создания аккаунта пользователя:",
            use_index,
            None,
            data_handler,
        )


class Input(InputBase):
    def __init__(
        self,
        user_input: UserInputBase,
        workstation_input: WorkstationInputBase,
        output: OutputBase,
    ):
        self.output: OutputBase = output
        self.answer: nstr = None
        if nn(user_input):
            self.user: UserInputBase = user_input
            self.user.parent = self
        if nn(workstation_input):
            self.workstation: WorkstationInputBase = workstation_input
            self.workstation.parent = self

    def input(
        self,
        caption: nstr = None,
        new_line: bool = True,
        check_function: Callable[[str], str] | None = None,
    ) -> str:
        try:
            while True:
                if new_line and nn(caption):
                    with self.output.make_indent(0):
                        self.output.input(caption)
                value: str = (
                    input(self.output.text_before)
                    if new_line
                    else input(j_s((self.output.text_before + caption)))
                )
                if nn(check_function):
                    value_after: str = check_function(value)
                    if nn(value_after):
                        return value_after
                else:
                    return value
        except KeyboardInterrupt as _:
            raise KeyboardInterrupt()

    def date_period(
        self, start_date_string: nstr = None, end_date_string: nstr = None
    ) -> tuple[date, date]:
        today_date: date = SGB.DATA.today()

        def get_date_format(value: str) -> str:
            value = value.strip()
            return (
                CONST.YEARLESS_DATE_FORMAT
                if value.count(CONST.DATE_PART_DELIMITER) == 1 or value.count(" ") == 1
                else CONST.DATE_FORMAT
            )

        value: nstr = start_date_string
        format: nstr = None if e(value) else get_date_format(nns(value))
        start_date: date | None = SGB.DATA.EXTRACT.date(value, nns(format))
        if ne(start_date):
            if format == CONST.YEARLESS_DATE_FORMAT:
                start_date = nnt(start_date).replace(today_date.year)
        value = end_date_string
        format = None if e(value) else get_date_format(value)
        end_date: date | None = SGB.DATA.EXTRACT.date(value, nns(format))
        if ne(end_date):
            if format == CONST.YEARLESS_DATE_FORMAT:
                end_date = end_date.replace(today_date.year)
        while True:
            if e(start_date):
                value = self.input(
                    j(
                        (
                            "Введите начало периода, в формате ",
                            b("ДЕНЬ.МЕСЯЦ"),
                            ", например ",
                            SGB.DATA.today_string(CONST.YEARLESS_DATE_FORMAT),
                        )
                    )
                )
                value = SGB.DATA.FORMAT.to_date(value)
                format = get_date_format(value)
                if format == CONST.YEARLESS_DATE_FORMAT:
                    value = j_p((value, today_date.year))
                start_date = SGB.DATA.EXTRACT.date(value, CONST.DATE_FORMAT)
                if e(start_date) or nnt(start_date) > nnt(today_date):
                    continue
            if e(end_date) or nnt(start_date) > nnt(end_date):
                if not self.confirm(
                    "Использовать сегодняшнюю дату",
                    no_label=j(
                        (
                            "Введите окончание периода, в формате ",
                            b("ДЕНЬ.МЕСЯЦ"),
                            ", например ",
                            SGB.DATA.today_string(CONST.YEARLESS_DATE_FORMAT),
                        )
                    ),
                ):
                    value = SGB.DATA.FORMAT.to_date(self.answer)
                    format = get_date_format(value)
                    if format == CONST.YEARLESS_DATE_FORMAT:
                        value = j_p((value, today_date.year))
                    end_date = SGB.DATA.EXTRACT.date(value, CONST.DATE_FORMAT)
                    if e(end_date):
                        continue
                else:
                    end_date = SGB.DATA.today(as_datetime=True)
            if not (e(start_date) or e(end_date)):
                break

        return (start_date, end_date)

    def polibase_persons_by_any(
        self, value: nstr = None, title: nstr = None, select_all: bool = False
    ) -> list[PolibasePerson]:
        result: Result[list[PolibasePerson]] = SGB.RESULT.POLIBASE.persons_by_any(
            value or self.polibase_person_any(title)
        )
        label_function: Callable[[Any, int], str] | None = (
            (lambda item, _: "Все" if n(item) else item.FullName)
            if len(result.data) > 1
            else None
        )
        if select_all and len(result.data) > 1:
            result.data.append(None)
        polibase_person: PolibasePerson = self.item_by_index(
            "Выберите пользователя, введя индекс", result.data, label_function
        )
        return result.data if n(polibase_person) else [polibase_person]

    def telephone_number(
        self, format: bool = True, prefix: nstr = CONST.TELEPHONE_NUMBER_PREFIX
    ) -> str:
        while True:
            self.output.input("Введите номер телефона")
            use_telephone_prefix: bool = nn(prefix)
            telephone_number: str = self.input(prefix, False)
            if use_telephone_prefix:
                if not telephone_number.startswith(prefix):
                    telephone_number = j((prefix, telephone_number))
            check: nbool = None
            if format:
                telehone_number_after_fix = SGB.DATA.FORMAT.telephone_number(
                    telephone_number, prefix
                )
                check = SGB.CHECK.telephone_number(telehone_number_after_fix)
                if check and telehone_number_after_fix != telephone_number:
                    telephone_number = telehone_number_after_fix
                    self.output.value("Телефон отформатирован", telephone_number)
            if check or SGB.CHECK.telephone_number(telephone_number):
                return telephone_number
            else:
                self.output.error("Неверный формат номера телефона!")

    def email(self, title: nstr = None) -> str:
        email: nstr = None
        while True:
            email = self.input(title or "Адресс электронная почта")
            if SGB.CHECK.email(email):
                return email
            else:
                self.output.error("Неверный формат адресса электронной почты!")

    def polibase_person_card_registry_folder(
        self, value: nstr = None, title: nstr = None
    ) -> str:
        while True:
            value = value or self.input(
                title or "Введите название папки с картами пациентов"
            )
            if SGB.CHECK.POLIBASE.person_card_registry_folder(value):
                return SGB.DATA.FORMAT.polibase_person_card_registry_folder(value)
            else:
                self.output.error("Неверный формат названия папки с картами пациентов!")
                value = None

    def message(self, caption: nstr = None, prefix: nstr = None) -> str:
        caption = caption or "Введите сообщение"
        self.output.input(caption)
        return (prefix or "") + self.input(prefix, False)

    def description(self) -> str:
        self.output.input("Введите описание")
        return self.input()

    def login(self, check_on_exists: bool = False) -> str:
        login: nstr = None
        while True:
            login = self.input("Введите логин")
            if SGB.CHECK.login(login):
                if check_on_exists and SGB.CHECK.USER.exists_by_login(login):
                    self.output.error("Логин занят!")
                else:
                    return login
            else:
                self.output.error("Неверный формат логина!")

    def indexed_list(
        self,
        caption: str,
        name_list: list[Any],
        caption_list: strlist,
        by_index: bool = False,
    ) -> str:
        return self.item_by_index(
            caption,
            name_list,
            lambda item, index: caption_list[index if by_index else item],
        )

    def indexed_field_list(self, caption: str, list: FieldItemList) -> str:
        name_list = list.get_name_list()
        return self.item_by_index(
            caption, name_list, lambda item, _: list.get_item_by_name(item).caption
        )

    def index(
        self,
        caption: str,
        data: list[Any],
        label_function: Callable[[Any, int], str] | None = None,
    ) -> nint | str:
        length: int = len(data)
        if length == 0:
            return None
        if length == 1:
            return 0
        value: nstr = None
        selected_index: nint = None
        label_function = label_function or (lambda item, index: item)
        index_min_value: int = 1
        index_max_value: int = length
        data_label_list: strlist = []
        for index, item in enumerate(data):
            data_label: str = label_function(item, index)
            self.output.indexed_item(
                (index + 1 if length > 1 else None),
                data_label,
                index_min_value,
                index_max_value,
            )
            data_label_list.append(data_label)
        selected_index = SGB.DATA.EXTRACT.decimal(
            value := self.input(
                j(
                    (
                        self.output.index_str(
                            caption,
                            index_min_value,
                            index_max_value,
                        ),
                    )
                )
            ),
            simple=True,
        )
        if n(selected_index):
            return value
        selected_index = int(selected_index) - index_min_value
        if selected_index >= 0 and selected_index < length:
            return selected_index
        return None

    def enum_item_by_index(
        self,
        caption: str,
        enum_class: Enum,
        allow_choose_all: bool = False,
    ) -> Enum | list[Enum]:
        enum_list: list[Enum] = list(enum_class)
        index: int = self.index(
            caption,
            enum_list,
            lambda enum_item, index: enum_item.value,
        )
        return enum_list[1:] if allow_choose_all and index == 0 else enum_list[index]

    def community(
        self,
        exclude: (
            COMMUNITY_SETTING_ITEM
            | list[COMMUNITY_SETTING_ITEM]
            | tuple[COMMUNITY_SETTING_ITEM, ...]
            | None
        ) = None,
    ) -> COMMUNITY:
        community_list: list[COMMUNITY] = list(COMMUNITY)
        if nn(exclude):
            for community_item in community_list:
                if ne(COMMUNITY_SETTINGS[community_item]) and BM.has(
                    COMMUNITY_SETTINGS[community_item], exclude
                ):
                    community_list.remove(community_item)
        return self.enum_item_by_index("Выберите общество", community_list)

    def item_by_index(
        self,
        caption: str,
        data: list[Any],
        label_function: Callable[[Any, int], str] | None = None,
        filter_function: Callable[[Any, str], bool] | None = None,
    ) -> Any | list[Any]:
        while True:
            index: nint | str = self.index(caption, data, label_function)
            if n(index):
                continue
            if isinstance(index, int):
                return data[index]
            data_filtered: list[Any] = SGB.DATA.FILTER.by_string(
                index,
                data,
                label_function if n(filter_function) else None,
                filter_function,
            )
            if e(data_filtered):
                return None
            data = data_filtered

    def password(
        self,
        secret: bool = True,
        check: bool = False,
        settings: PasswordSettings | None = None,
        is_new: bool = True,
    ) -> str:
        self.output.input("Введите новый пароль" if is_new else "Введите пароль")
        while True:
            value = getpass("") if secret else self.input()
            if not check or (nn(settings) and SGB.CHECK.password(value, settings)):
                return value
            else:
                self.output.error("Пароль не соответствует требованием безопасности")

    def same_if_empty(self, caption: str, src_value: str) -> str:
        value = self.input(caption)
        if value == "":
            value = src_value
        return value

    def name(self) -> str:
        return self.input("Введите часть имени")

    def full_name(self, one_line: bool = False) -> FullName:
        if one_line:
            while True:
                value: str = self.input("Введите полное имя")
                if SGB.CHECK.full_name(value):
                    return FullNameTool.fullname_from_string(
                        SGB.DATA.FORMAT.name(value)
                    )
                else:
                    pass
        else:

            def full_name_part(caption: str) -> str:
                while True:
                    value: str = self.input(caption)
                    value = value.strip()
                    if SGB.CHECK.name(value):
                        return SGB.DATA.FORMAT.name(value)
                    else:
                        pass

            return FullName(
                full_name_part("Введите фамилию"),
                full_name_part("Введите имя"),
                full_name_part("Введите отчество"),
            )

    def confirm(
        self,
        text: str = " ",
        enter_for_yes: bool = False,
        yes_label: nstr = None,
        no_label: nstr = None,
        yes_checker: Callable[[str], bool] | None = None,
    ) -> bool:
        text = self.output.blue_str(self.output.text_color_str(Fore.WHITE, text))
        if nn(no_label):
            no_label = j((no_label, " "))
        self.output.write_line(
            f"{text}? \n{self.output.green_str(self.output.text_black_str('Да (1 или Ввод)'))} / {self.output.red_str(no_label or self.output.text_black_str('Нет (Остальное)'), '')}"
            if enter_for_yes
            else f"{text}? \n{self.output.red_str('Да (1)')} / {self.output.green_str(no_label or self.output.text_black_str('Нет (Остальное или Ввод)'), '')}"
        )
        answer: str = self.input()
        answer = answer.lower()
        self.answer = answer
        return (
            answer == "y"
            or answer == "yes"
            or answer == "1"
            or (answer == "" and enter_for_yes)
        )

    def message_for_user_by_login(self, login: str) -> str:
        user: User = SGB.RESULT.USER.by_login(login).data
        if user is not None:
            head_string = j_s(
                ("Здравствуйте, ", FullNameTool.to_given_name(user.name), ", ")
            )
            self.output.green(head_string)
            message = self.input("Введите сообщениеt: ")
            return j((head_string, message))
        else:
            pass

    def polibase_person_any(self, title: nstr = None) -> str:
        return self.input(
            title or "Введите персональный номер или часть имени пациента"
        )

    def datetime(
        self,
        use_date: nbool = True,
        use_time: nbool = True,
        ask_time_input: bool = True,
    ) -> datetime:
        result: datetime = DateTimeTool.now(second=0)
        temp_datetime: datetime = result
        if n(use_date):
            use_date = not self.confirm(
                j_s(
                    (
                        "Использовать текущую дату",
                        b(DateTimeTool.datetime_to_string(result, CONST.DATE_FORMAT)),
                    )
                )
            )
        while use_date and True:
            date_value: nstr = self.input(
                j_s(("Введите дату в формате", b("День.Месяц.Год")))
            ).lower()
            date_value = date_value.replace("ю", ".")
            dot_list: int = date_value.split(".")
            dot_count: int = len(dot_list)
            for _ in range(dot_count):
                dot_list = ListTool.not_empty_items(
                    DataTool.map(
                        lambda item: str(SGB.DATA.EXTRACT.decimal(item)), dot_list
                    )
                )
            if dot_count == len(dot_list):
                date_value = j(dot_list, ".")
                temp_datetime = SGB.DATA.EXTRACT.datetime(
                    date_value,
                    [CONST.DAY_FORMAT, CONST.YEARLESS_DATE_FORMAT, CONST.DATE_FORMAT][
                        dot_count - 1
                    ],
                )
                if nn(temp_datetime):
                    if dot_count >= 1:
                        result = result.replace(day=temp_datetime.day)
                    if dot_count >= 2:
                        result = result.replace(month=temp_datetime.month)
                    if dot_count >= 3:
                        result = result.replace(year=temp_datetime.year)
                    break
        if ask_time_input and self.confirm(j_s("Ввести время")):
            if n(use_time):
                use_time = not self.confirm(
                    j_s(
                        (
                            "Использовать текущее время",
                            b(
                                DateTimeTool.datetime_to_string(
                                    result, CONST.SECONDLESS_TIME_FORMAT
                                )
                            ),
                        )
                    )
                )
            while use_time and True:
                time_value: nstr = self.input(
                    j_s(("Введите время в формате", b("Час:Минуты")))
                )
                dot_list: int = time_value.split(":")
                dot_count: int = len(dot_list)
                for i in range(dot_count):
                    dot_list = ListTool.not_empty_items(
                        DataTool.map(
                            lambda item: str(SGB.DATA.EXTRACT.decimal(item)), dot_list
                        )
                    )
                if dot_count == len(dot_list):
                    time_value = j(dot_list, ":")
                    temp_datetime = SGB.DATA.EXTRACT.datetime(
                        time_value,
                        [CONST.HOUR_TIME_FORMAT, CONST.SECONDLESS_TIME_FORMAT][
                            dot_count - 1
                        ],
                    )
                    if nn(temp_datetime):
                        if dot_count >= 1:
                            result = result.replace(hour=temp_datetime.hour)
                        if dot_count >= 2:
                            result = result.replace(minute=temp_datetime.minute)
                        break
        else:
            result = result.replace(minute=0, hour=0)
        return result

    def choose_file(
        self,
        use_search_request: bool | nstr = None,
        allow_choose_all: bool = False,
    ) -> File | list[File]:
        if n(use_search_request):
            use_search_request = self.confirm("Использовать поиск", enter_for_yes=True)
        file_list: list[File] | None = None

        search_request: nstr = None
        if isinstance(use_search_request, str):
            search_request = use_search_request
        elif use_search_request:
            search_request = self.input("Введите поисковый запрос")
        with self.output.make_loading(1, "Идет загрузка файлов. Ожидайте"):
            file_list = SGB.RESULT.FILES.find(
                value=(search_request if use_search_request else None)
            ).data
        if e(file_list):
            self.output.error(
                j_s(
                    (
                        "Файл с именем",
                        esc(search_request),
                        "не найден",
                    )
                )
            )
            file_list = SGB.RESULT.FILES.all().data

        def label_function(file: File, _) -> str:
            title_list: strlist = file.title.split(CONST.SPLITTER)
            if len(title_list) == 3:
                return j(
                    (
                        b(title_list[0].upper()),
                        ": ",
                        title_list[-1],
                        " (",
                        title_list[-2],
                        ")",
                    )
                )
            return b(title_list[1])

        return self.item_by_index(
            "Выберите файл",
            file_list,
            label_function,
            allow_choose_all=allow_choose_all,
        )

    def choose_note(
        self,
        use_search_request: bool | nstr = None,
        allow_choose_all: bool = False,
    ) -> Note:
        if n(use_search_request):
            use_search_request = self.confirm("Использовать поиск", enter_for_yes=True)
        note_list: list[Note] | None = None
        search_request: nstr = None
        if isinstance(use_search_request, str):
            search_request = use_search_request
        elif use_search_request:
            search_request = self.input("Введите поисковый запрос")
        with self.output.make_loading(1, "Идет загрузка заметок. Ожидайте"):
            note_list = SGB.RESULT.NOTES.find(
                search_request if use_search_request else None
            ).data
        if e(note_list):
            self.output.error(
                j_s(
                    (
                        "Файл с именем",
                        esc(search_request),
                        "не найден",
                    )
                )
            )
            note_list = SGB.RESULT.NOTES.all().data

        def label_function(note: Note, _) -> str:
            return b(note.title)

        return self.item_by_index(
            "Выберите файл",
            note_list,
            label_function,
            allow_choose_all=allow_choose_all,
        )


class WorkstationInput(WorkstationInputBase):

    def __init__(self, input: Input | None = None):
        self.parent = input

    def title_any(self, title: nstr = None) -> str:
        return self.parent.input(
            title or "Введите название, логин, часть имени или телефон пользователя"
        )

    def select(
        self,
        result: Result[list[Workstation]] | None = None,
        title: nstr = None,
        label_function: Callable[[Workstation, int], str] | None = None,
        sort_function: Callable[[Workstation], str] | None = None,
        filter_function: Callable[[Workstation, str], bool] | None = None,
        show_select_all: nbool = False,
    ) -> Result[list[Workstation]]:
        if n(result):
            value: str = self.title_any(title)
        with self.parent.output.make_loading(text="Поиск"):
            result = SGB.RESULT.WORKSTATION.any(value)
        if n(show_select_all):
            return result
        if show_select_all and len(result) > 1:
            result.data.append(None)
        if nn(sort_function):
            result.sort(key=sort_function)

        result.data = DataTool.as_list(
            self.parent.item_by_index(
                "Выберите компьютер, введя индекс",
                result.data,
                label_function or self.parent.output.workstation.label_function,
                filter_function=filter_function,
            )
        )
        return result


class UserInput(UserInputBase):

    def __init__(self, input: Input | None = None):
        self.parent = input

    def container(self) -> ADContainer:
        result: Result[list[ADContainer]] = SGB.RESULT.USER.containers()
        self.parent.output.containers_for_result(result, True)
        return self.parent.item_by_index(
            "Выберите контейнер пользователя, введя индекс", result.data
        )

    def by_name(self) -> User:
        result: Result[list[User]] = SGB.RESULT.USER.by_name(self.parent.name())
        result.fields = FIELD_COLLECTION.AD.USER_NAME
        self.parent.output.table_with_caption(result, "Список пользователей", True)
        return self.parent.item_by_index(
            "Выберите пользователя, введя индекс", result.data
        )

    def title_any(self, title: nstr = None) -> str:
        return self.parent.input(
            title or "Введите логин, часть имени или другой поисковый запрос"
        )

    def by_any(
        self,
        value: nstr = None,
        active: nbool = None,
        title: nstr = None,
        select_all: nbool = None,
    ) -> Result[list[User]]:
        result: Result[list[User]] = SGB.RESULT.USER.by_any(
            value or self.title_any(title), active
        )
        if select_all and len(result.data) > 1:
            result.data.append(None)
        result_data: User | None = self.parent.item_by_index(
            "Выберите пользователя, введя индекс",
            result.data,
            (
                (
                    lambda item, _: (
                        "Все" if n(item) else j((item.name, " (", item.login, ")"))
                    )
                )
                if len(result.data) > 1
                else None
            ),
        )
        result.data = result_data
        return result

    def telephone_number(
        self,
        value: nstr = None,
        active: nbool = None,
        title: nstr = None,
    ) -> User | None:
        try:
            return self.by_any(value, active, title)
        except NotFound as _:
            return None

    def template(self) -> User:
        result: Result[list[User]] = SGB.RESULT.USER.template_list()
        self.parent.output.template_users_for_result(result, True)
        return self.parent.item_by_index(
            "Выберите шаблон пользователя, введя индекс", result.data
        )

    def search_attribute(self) -> str:
        return self.parent.indexed_field_list(
            "Выберите по какому критерию искать, введя индекс",
            FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE,
        )

    def search_value(self, search_attribute: str) -> str:
        field_item = FIELD_COLLECTION.AD.SEARCH_ATTRIBUTE.get_item_by_name(
            search_attribute
        )
        return self.parent.input(j_s(("Введите", lw(field_item.caption))))

    def generate_password(
        self, once: bool = False, settings: PasswordSettings = PASSWORD.SETTINGS.DEFAULT
    ) -> str:
        def internal_generate_password(settings: PasswordSettings | None = None) -> str:
            return PasswordTools.generate_random_password(
                settings.length,
                settings.special_characters,
                settings.order_list,
                settings.special_characters_count,
                settings.alphabets_lowercase_count,
                settings.alphabets_uppercase_count,
                settings.digits_count,
                settings.shuffled,
            )

        while True:
            password = internal_generate_password(settings)
            if once or self.parent.confirm(
                j_s(("Использовать пароль", password)), True
            ):
                return password
            else:
                pass

    def generate_login(
        self,
        full_name: FullName,
        ask_for_remove_inactive_user_if_login_is_exists: bool = True,
        ask_for_use: bool = True,
    ) -> str:
        login_list: strlist = []
        inactive_user_list: list[User] = []
        login_is_exists: bool = False

        def show_user_which_login_is_exists_and_return_user_if_it_inactive(
            login_string: str,
        ) -> User:
            user: User = SGB.RESULT.USER.by_login(login_string).data
            is_active: bool = SGB.CHECK.USER.active(user)
            self.parent.output.error(
                f"Логин '{login_string}' занят {'активным' if is_active else 'неактивным'} пользователем: {user.name}"
            )
            self.parent.output.new_line()
            return user if not is_active else None

        login: FullName = NamePolicy.convert_to_login(full_name)
        login_string: str = FullNameTool.fullname_to_string(login, "")
        login_list.append(login_string)
        need_enter_login: bool = False

        def remove_inactive_user_action():
            login_string: nstr = None
            need_enter_login: bool = False
            if self.parent.confirm(
                "Удалить неактивных пользователей, чтобы освободить логин", True
            ):
                user_for_remove: User = self.parent.item_by_index(
                    "Выберите пользователя для удаления, выбрав индекс",
                    inactive_user_list,
                    lambda user, _: f"{user.name} ({user.login})",
                )
                self.parent.output.new_line()
                self.parent.output.value(
                    "Пользователь для удаления", user_for_remove.name
                )
                if self.parent.confirm("Удалить неактивного пользователя", True):
                    if SGB.ACTION.USER.remove(user_for_remove):
                        self.parent.output.good("Удален")
                        login_string = user_for_remove.login
                        inactive_user_list.remove(user_for_remove)
                    else:
                        self.parent.output.error("Ошибка")
                else:
                    need_enter_login = True
            else:
                need_enter_login = True
            return need_enter_login, login_string

        if SGB.CHECK.USER.exists_by_login(login_string):
            user: User = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                login_string
            )
            if user is not None:
                inactive_user_list.append(user)
            login_alt: FullName = NamePolicy.convert_to_alternative_login(login)
            login_string = FullNameTool.fullname_to_string(login_alt, "")
            login_is_exists = login_string in login_list
            if not login_is_exists:
                login_list.append(login_string)
            if login_is_exists or SGB.CHECK.USER.exists_by_login(login_string):
                if not login_is_exists:
                    user = (
                        show_user_which_login_is_exists_and_return_user_if_it_inactive(
                            login_string
                        )
                    )
                    if user is not None:
                        inactive_user_list.append(user)
                login_reversed: FullName = NamePolicy.convert_to_reverse_login(login)
                login_is_exists = login_string in login_list
                login_string = FullNameTool.fullname_to_string(login_reversed, "")
                if not login_is_exists:
                    login_list.append(login_string)
                if login_is_exists or SGB.CHECK.USER.exists_by_login(login_string):
                    login_last: FullName = NamePolicy.convert_to_last_login(login)
                    login_string = FullNameTool.fullname_to_string(login_last, "")
                    if not login_is_exists:
                        user = show_user_which_login_is_exists_and_return_user_if_it_inactive(
                            login_string
                        )
                        if user is not None:
                            inactive_user_list.append(user)
                    if (
                        ask_for_remove_inactive_user_if_login_is_exists
                        and len(inactive_user_list) > 0
                    ):
                        need_enter_login, login_string = remove_inactive_user_action()
                    if need_enter_login:
                        while True:
                            login_string = self.parent.login()
                            if SGB.CHECK.USER.exists_by_login(login_string):
                                show_user_which_login_is_exists_and_return_user_if_it_inactive(
                                    login_string
                                )
                            else:
                                break
        if (
            not need_enter_login
            and ask_for_remove_inactive_user_if_login_is_exists
            and len(inactive_user_list) > 0
        ):
            need_enter_login, login_string = remove_inactive_user_action()
            if need_enter_login:
                return self.generate_login(full_name, False)
        else:
            if ask_for_use and not self.parent.confirm(
                f"Использовать логин '{login_string}' для аккаунта пользователя", True
            ):
                login_string = self.parent.login(True)

        return login_string


class NamePolicy:
    @staticmethod
    def get_first_letter(name: str) -> str:
        letter = name[0]
        if letter.lower() == "ю":
            return "yu"
        return translit(letter, "ru", reversed=True).lower()

    @staticmethod
    def convert_to_login(full_name: FullName) -> FullName:
        return FullName(
            NamePolicy.get_first_letter(full_name.last_name),
            NamePolicy.get_first_letter(full_name.first_name),
            NamePolicy.get_first_letter(full_name.middle_name),
        )

    @staticmethod
    def convert_to_alternative_login(login_list: FullName) -> FullName:
        return FullName(
            login_list.first_name, login_list.middle_name, login_list.last_name
        )

    @staticmethod
    def convert_to_last_login(login_list: FullName) -> FullName:
        return FullName(
            login_list.first_name, login_list.last_name, login_list.middle_name
        )

    @staticmethod
    def convert_to_reverse_login(login_list: FullName) -> FullName:
        return FullName(
            login_list.middle_name, login_list.first_name, login_list.last_name
        )


class SGB:

    NAME: str = "sgb"

    def __init__(
        self,
        input: InputBase | None = None,
        output: OutputBase | None = None,
        session: SessionBase | None = None,
    ):
        ErrorableThreadPoolExecutor.error_wrapper = SGB.ERROR.wrap
        if n(output):
            output = Output(UserOutput(), WorkstationOutput())
            SGB.output: Output = output
        else:
            self.output: Output = output
        if n(input):
            input = Input(UserInput(), WorkstationInput(), SGB.output)
            SGB.input: Input = input
        else:
            self.input: Input = input
        if n(session):
            SGB.session: Session = Session(input, output)
        else:
            self.session: Session = session
        SGB.output.init()

    class VERSION:
        value: str = VERSION

        @staticmethod
        def need_update() -> bool:
            return False
            # return importlib.util.find_spec(SGB.NAME) is not None and SGB.VERSION.value < SGB.VERSION.remote()

    class INPUT_WAIT:
        NAME: str = "RecipientWaitingForInput"

        @staticmethod
        def _get_name(group_name: str, recipient: str) -> str:
            return j((group_name, recipient), CONST.SPLITTER)

        @staticmethod
        def add(group_name: str, recipient: str, timeout: int) -> bool:
            return SGB.ACTION.DATA_STORAGE.value(
                RecipientWaitingForInput(
                    group_name, timeout, recipient, SGB.DATA.now()
                ),
                SGB.INPUT_WAIT._get_name(group_name, recipient),
                SGB.INPUT_WAIT.NAME,
            )

        @staticmethod
        def remove(group_name: str, recipient: str) -> bool:
            return SGB.ACTION.DATA_STORAGE.value(
                None,
                SGB.INPUT_WAIT._get_name(group_name, recipient),
                SGB.INPUT_WAIT.NAME,
            )

        @staticmethod
        def has(group_name: str, recipient: str) -> bool:
            def extractor(data: Any) -> RecipientWaitingForInput | None:
                if n(data):
                    return None
                result: RecipientWaitingForInput = DataTool.fill_data_from_source(
                    RecipientWaitingForInput(), data
                )
                result.timestamp = DateTimeTool.datetime_from_string(result.timestamp)
                return result

            result: RecipientWaitingForInput | None = SGB.RESULT.DATA_STORAGE.value(
                SGB.INPUT_WAIT._get_name(group_name, recipient),
                extractor,
                SGB.INPUT_WAIT.NAME,
            ).data
            return nn(result) and (
                n(result.timeout)
                or (DateTimeTool.now() - result.timestamp).total_seconds()
                < result.timeout
            )

    class CACHE:

        class TYPE:
            MEMORY: int = 0
            LOCAL: int = 1
            REMOTE: int = 2

        cache_type: int = TYPE.MEMORY

        memory_cache: dict[str, dict[str, bool]] = defaultdict(lambda: defaultdict(str))

        @staticmethod
        def get(section: str, name: str) -> nbool:
            if SGB.CACHE.cache_type == SGB.CACHE.TYPE.MEMORY:
                return (
                    SGB.CACHE.memory_cache[section][name]
                    if name in SGB.CACHE.memory_cache[section]
                    else None
                )
            if SGB.CACHE.cache_type == SGB.CACHE.TYPE.REMOTE:
                return SGB.DATA.VARIABLE.value(name, section=section)

        @staticmethod
        def set(section: str, name: str, value: bool) -> None:
            if SGB.CACHE.cache_type == SGB.CACHE.TYPE.MEMORY:
                SGB.CACHE.memory_cache[section][name] = value
            if SGB.CACHE.cache_type == SGB.CACHE.TYPE.REMOTE:
                SGB.DATA.VARIABLE.set(name, value, section=section)

    class ERROR:

        notify_about_error: bool = True

        USER = ERROR.USER

        @staticmethod
        def rpc(
            context: grpc.RpcContext | None = None,
            message: str = "",
            code: Any = None,
        ) -> Any:
            return SGB.SERVICE.client.create_error(
                context or ServiceClient.context, message, code
            )

        @staticmethod
        def service_host_is_unchangeable(value: str) -> None:
            SGB.output.error(
                j(
                    (
                        "Sorry, but service can't be start, cause service host is unchangeble.\n You are trying to start service on ",
                        SGB.DATA.FORMAT.domain(SGB.SYS.host()).lower(),
                        ", but service must be started on ",
                        SGB.DATA.FORMAT.domain(value).lower(),
                    )
                )
            )

        @staticmethod
        def create_header(details: str) -> str:
            return j(
                (
                    nl(),
                    "Версия: ",
                    SGB.VERSION.value,
                    nl(),
                    "Пользователь: ",
                    SGB.SYS.get_login(),
                    nl(),
                    "Хост: ",
                    SGB.SYS.host(),
                    nl(),
                    details,
                )
            )

        @staticmethod
        @contextmanager
        def detect(final_action: Callable[[], None] | None = None):
            try:
                yield True
            except Exception as error:
                SGB.ERROR.global_except_hook(error)
            finally:
                if nn(final_action):
                    final_action()

        @staticmethod
        @contextmanager
        def detect_suppressing(final_action: Callable[[], None] | None = None):
            try:
                yield True
            except BaseException:
                pass
            finally:
                if nn(final_action):
                    final_action()

        @staticmethod
        def wrap(action: Callable[[Any], Any]) -> Callable[[Any], Any]:
            def internal_action(*args, **kwargs) -> Any:
                with SGB.ERROR.detect():
                    return action(*args, **kwargs)

            return internal_action

        @staticmethod
        @contextmanager
        def detect_interruption(message: nstr = None):
            try:
                yield True
            except KeyboardInterrupt as _:
                DataTool.check_not_none(message, lambda: SGB.output.error(message))

        @staticmethod
        def rpc_error_handler(
            description: ServiceDescriptionBase,
            exception: grpc.RpcError,
            code: tuple,
            details: str,
            command: SERVICE_COMMAND,
        ) -> None:
            SGB._service_output(description, exception, code, details, command)

        @staticmethod
        def global_except_hook(
            exception: BaseException,
            host: nstr = None,
            argument_list: strlist | None = None,
        ) -> None:
            exception_type, traceback_value = type(exception), exception.__traceback__
            argument_list = (argument_list or []) + DataTool.filter(
                lambda item: isinstance(item, str), exception.args
            )
            traceback_value_string: str = j_nl(traceback.format_exception(exception))
            if SGB.ERROR.notify_about_error:
                SGB.EVENT.send(
                    Events.ERROR,
                    (
                        SGB.ERROR.create_header(traceback_value_string),
                        host or SGB.SYS.host(),
                        str(exception_type),
                        argument_list,
                    ),
                )
            sys.__excepthook__(exception_type, exception, traceback_value)

        sys.excepthook = lambda exception_type, exception, traceback_value: SGB.ERROR.global_except_hook(
            exception
        )

        class POLIBASE:

            @staticmethod
            def create_not_found_error(
                title: nstr, value: str, start: str = "Пациент"
            ) -> NotFound:
                title = title or "поисковым запросом"
                return NotFound(
                    j_s((start, "с", title, escs(value), "не найден!")), value
                )

    class UPDATER:

        @staticmethod
        @cache
        def versions(package_name: str) -> strlist:
            url: str = j(("https://pypi.org/pypi/", package_name, "/json"))
            return sorted(
                requests.get(url, timeout=5).json()["releases"],
                key=parse_version,
                reverse=True,
            )

        @staticmethod
        def for_service(
            service_object: SERVICE_ROLE | ServiceDescription,
            additional_packages: strtuple | None = None,
            as_standalone: bool = False,
            show_output: bool = True,
        ) -> bool:
            if SGB.session.is_executable:
                return True
            service_description: ServiceDescription = (
                ServiceRoleTool.service_description(service_object)
            )
            packages: strtuple = (additional_packages or ()) + (
                service_description.packages or ()
            )
            if as_standalone:
                if e(additional_packages):
                    return True
            else:
                package_list: strlist = []
                for package in packages:
                    if not package.startswith(SGB.NAME):
                        package_list.append(package)
                packages = tuple(package_list)
            return SGB.UPDATER.packages(packages, show_output)

        @staticmethod
        def packages(value: strtuple | None, show_output: bool = True) -> bool:
            result: bool = True
            if ne(value):
                installed_package_list: strlist = {
                    lw(package.key) for package in working_set
                }
                for package_name in lw(value):
                    if package_name not in installed_package_list:
                        result = result and SGB.UPDATER.package_operation(
                            name=package_name, show_output=show_output
                        )
                        if result:
                            working_set.add_entry(package_name)
                        else:
                            break
            return result

        @staticmethod
        def command_for_package_operation(
            package_name_or_path: str,
            version: nstr = None,
            host_is_local: bool = True,
            virtual_environment: bool = False,
            use_local_package: bool = False,
            install_operation: bool = True,
        ) -> strtuple:
            executor_path: nstr = None
            if virtual_environment and install_operation:
                executor_path = sys.executable
            else:
                executor_path = (
                    PYTHON.EXECUTOR if host_is_local else PYTHON.EXECUTOR_ALIAS
                )
            return (
                executor_path,
                "-m",
                PYTHON.PIP,
                [PYTHON.COMMAND.UNINSTALL, PYTHON.COMMAND.INSTALL][install_operation],
            ) + (
                (package_name_or_path, "-y")
                if not install_operation
                else (
                    (package_name_or_path,)
                    if use_local_package
                    else (
                        (package_name_or_path, "-U")
                        if n(version)
                        else (j((package_name_or_path, "==", version)),)
                    )
                )
            )

        @staticmethod
        def _cache_name(
            virtual_environment: bool,
            host: nstr,
            name: str,
            version: nstr = None,
        ) -> str:
            return j(
                (
                    "package",
                    [None, "venv"][virtual_environment],
                    host,
                    name,
                    version,
                ),
                CONST.SPLITTER,
            )

        @staticmethod
        def package_exists(value: str | strlist | strtuple) -> bool:
            if isinstance(value, (list, tuple)):
                for item in value:
                    if not SGB.UPDATER.package_exists(item):
                        return False
                    return True
            is_virtual_environment: bool = SGB.SYS.is_virtual_environment()
            cache_name: str = SGB.UPDATER._cache_name(
                is_virtual_environment, SGB.SYS.host(), value
            )
            cache_value: nbool = SGB.CACHE.get(SGB.UPDATER.__name__, cache_name)
            if nn(cache_value):
                return cache_value
            result: bool = nn(importlib.util.find_spec(value))
            SGB.CACHE.set(SGB.UPDATER.__name__, cache_name, result)
            return result

        @staticmethod
        def localy(version: nstr = None, show_output: bool = False) -> bool:
            return SGB.UPDATER.package_operation(
                name=SGB.NAME, version=version, show_output=show_output
            )

        @staticmethod
        def install_service(
            value: SERVICE_ROLE | ServiceDescriptionBase,
            version: nstr = None,
            host: nstr = None,
            use_local_package: bool = False,
            show_output: bool = False,
        ) -> nbool:
            service_description: ServiceDescription = (
                ServiceRoleTool.service_description(value)
            )
            if not service_description.use_standalone:
                return None
            return SGB.UPDATER.install_package(
                service_description.standalone_name,
                version,
                host,
                use_local_package,
                show_output,
            )

        @staticmethod
        def install_package(
            name: str,
            version: nstr = None,
            host: nstr = None,
            use_local_package: bool = False,
            show_output: bool = False,
        ) -> nbool:
            return SGB.UPDATER.package_operation(
                name, version, host, use_local_package, show_output, True
            )

        @staticmethod
        def uninstall_package(
            name: str,
            version: nstr = None,
            host: nstr = None,
            use_local_package: bool = False,
            show_output: bool = False,
        ) -> nbool:
            return SGB.UPDATER.package_operation(
                name, version, host, use_local_package, show_output, False
            )

        @staticmethod
        def package_operation(
            name: str,
            version: nstr = None,
            host: nstr = None,
            use_local_package: bool = False,
            show_output: bool = False,
            install_operation: bool = True,
        ) -> nbool:
            result: nbool = False
            is_sgb_package: bool = name.startswith(SGB.NAME)
            host_is_linux: nbool = None
            if use_local_package:
                if nn(version):
                    package_path: str = PathTool.path(
                        PATHS.FACADE.DITRIBUTIVE.PACKAGE(name, version)
                    )
                    if PathTool.exists(package_path):
                        name = package_path
                    else:
                        version = None
                if n(version):
                    name = PathTool.path(
                        nns(
                            first(
                                DataTool.filter(
                                    lambda item: PathTool.get_extension(item)
                                    == PYTHON.PACKAGE_EXTENSION,
                                    PathTool.get_file_list(
                                        PATHS.FACADE.DITRIBUTIVE.PACKAGE_FOLDER(name)
                                    ),
                                )
                            )
                        )
                    )

            virtual_environment: bool = (
                SGB.SYS.is_virtual_environment() and SGB.SYS.host_is_local(host)
            )
            if virtual_environment and install_operation:
                if is_sgb_package:
                    return None
                # Use VSCode for Windows
                host_is_linux = False
            else:
                if n(host_is_linux):
                    host_is_linux = SGB.SYS.is_linux(host)
            cache_name: str = SGB.UPDATER._cache_name(
                virtual_environment, host, name, version
            )
            if n(SGB.CACHE.get(SGB.UPDATER.__name__, cache_name)):
                host_is_local: bool = e(host) or SGB.SYS.host_is_local(host)
                command_list: strtuple = SGB.UPDATER.command_for_package_operation(
                    name,
                    version,
                    host_is_local,
                    virtual_environment,
                    use_local_package,
                    install_operation,
                )
                if host_is_linux:
                    command_list = (PYTHON.EXECUTOR3,) + command_list[1:]
                    result = (
                        str(SGB.RESULT.SSH.execute(j_s(command_list), host).data).find(
                            j_s(("Successfully installed", name))
                        )
                        != -1
                    )
                else:
                    complete_process: CompletedProcess = SGB.EXECUTOR.execute(
                        (
                            command_list
                            if host_is_local
                            else SGB.EXECUTOR.create_command_for_psexec(
                                command_list, host, interactive=True
                            )
                        ),
                        show_output,
                    )
                    result = SGB.DATA.CHECK.returncode(complete_process)
                SGB.CACHE.set(SGB.UPDATER.__name__, cache_name, result)
            return result

    class SETTINGS:

        NAME: str = "settings"

        @staticmethod
        def to_datetime(value: SETTINGS) -> datetime:
            return SGB.DATA.CONVERT.settings_to_datetime(value)

        @staticmethod
        def to_datetime_list(value: SETTINGS) -> list[datetime]:
            return SGB.DATA.CONVERT.settings_to_datetime_list(value)

        @staticmethod
        def set(settings_item: SETTINGS | str, value: Any) -> bool:
            return SGB.ACTION.SETTINGS.set(settings_item, value)

        @staticmethod
        def set_default(settings_item: SETTINGS) -> bool:
            return SGB.ACTION.SETTINGS.set_default(settings_item)

        @staticmethod
        def get(settings_item: SETTINGS | StorageVariableHolder | str) -> Any:
            if isinstance(settings_item, str):
                return SGB.RESULT.SETTINGS.get_by_name(settings_item).data
            return SGB.RESULT.SETTINGS.get(settings_item).data

        @staticmethod
        def all() -> list[strdict]:
            return SGB.RESULT.SETTINGS.get_by_name(None).data

        @staticmethod
        def init() -> None:
            for setting_item in SETTINGS:
                if setting_item.value.auto_init:
                    SGB.SETTINGS.set_default(setting_item)

        @staticmethod
        def find(value: nstr) -> list[SETTINGS]:
            result: list[SETTINGS] = []
            for item in SETTINGS:
                if (
                    n(value)
                    or StringTool.contains(item.name, value)
                    or StringTool.contains(item.value.key_name, value)
                    or StringTool.contains(item.value.description, value)
                ):
                    result.append(item)
            return result

        class WORKSTATION:
            @staticmethod
            def shutdown_time() -> datetime:
                return SGB.DATA.CONVERT.settings_to_datetime(
                    SETTINGS.WORKSTATION_SHUTDOWN_TIME
                )

            @staticmethod
            def reboot_time() -> datetime:
                return SGB.DATA.CONVERT.settings_to_datetime(
                    SETTINGS.WORKSTATION_REBOOT_TIME
                )

        class USER:

            @staticmethod
            def use_cache() -> bool:
                return True
                return SGB.SETTINGS.get(SETTINGS.USER_USE_CACHE)

            @staticmethod
            def _get_section_name(login_holder: User | str) -> str:
                return j(
                    (
                        (
                            login_holder.login
                            if isinstance(login_holder, User)
                            else login_holder
                        ),
                        SGB.SETTINGS.NAME,
                    ),
                    CONST.NAME_SPLITTER,
                )

            @staticmethod
            def set(login_holder: User | str, name: str, value: Any) -> bool:
                return SGB.ACTION.DATA_STORAGE.value(
                    value, name, SGB.SETTINGS.USER._get_section_name(login_holder)
                )

            @staticmethod
            def get(
                login_holder: User | str,
                name: str,
                class_type_holder: Any | Callable[[Any], Any] | None = None,
            ) -> Any:
                return SGB.RESULT.DATA_STORAGE.value(
                    name,
                    class_type_holder,
                    SGB.SETTINGS.USER._get_section_name(login_holder),
                ).data

        class INDICATION:
            @staticmethod
            def ct_notification_start_time() -> list[datetime]:
                return SGB.DATA.CONVERT.settings_to_datetime(
                    SETTINGS.INDICATION_CT_NOTIFICATION_START_TIME
                )

        class RESOURCE:
            @staticmethod
            def site_check_certificate_start_time() -> datetime:
                return SGB.DATA.CONVERT.settings_to_datetime(
                    SETTINGS.RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME
                )

            @staticmethod
            def site_check_free_space_perion_in_minutes() -> int:
                return SGB.SETTINGS.get(
                    SETTINGS.RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES
                )

    class EXECUTOR:

        @staticmethod
        def kill_process_by_port(value: int) -> nbool:
            pid: str = (
                str(
                    SGB.EXECUTOR.execute(
                        j(
                            (
                                r'netstat -aon | findstr /rc:"\<0.0.0.0:',
                                value,
                                r'\>" | findstr "LISTENING"',
                            )
                        ),
                        show_output=True,
                        capture_output=True,
                        command_as_text=True,
                        as_shell=True,
                    ).stdout
                )
                .strip()
                .split(" ")[-1]
            )

            if e(pid):
                return None
            return SGB.EXECUTOR.kill_process(
                int(pid),
                via_standart_tools=False,
                show_output=True,
            )

        @staticmethod
        def psping(
            address_or_ip: str,
            host: nstr = None,
            count: nint = None,
            check_all: bool = True,
        ) -> nbool:
            count = count or 4
            ping_command: strtuple = (
                SGB.EXECUTOR.get_executor_path(PSTOOLS.PS_PING),
                PSTOOLS.ACCEPTEULA,
                "-4",
                "-n",
                str(count),
                address_or_ip,
            )
            complete_process: CompletedProcess = SGB.EXECUTOR.execute(
                DataTool.check_not_none(
                    host,
                    lambda: SGB.EXECUTOR.create_command_for_psexec(
                        ping_command,
                        host,
                        SGB.DATA.VARIABLE.ENVIRONMENT.value(
                            LINK.ADMINISTRATOR_LOGIN, False
                        ),
                        SGB.DATA.VARIABLE.ENVIRONMENT.value(
                            LINK.ADMINISTRATOR_PASSWORD
                        ),
                        True,
                    ),
                    ping_command,
                ),
                True,
                True,
            )

            if SGB.DATA.EXTRACT.returncode(complete_process):
                error: str = complete_process.stderr
                if StringTool.contains(error, "Host not found"):
                    return None
                result: str = complete_process.stdout
                lost_marker: str = "Lost = "
                index: int = result.find(lost_marker)
                if index != -1:
                    lost_count: int = int(
                        result[index + len(lost_marker) : result.find(" (", index)]
                    )
                    if check_all:
                        return lost_count == 0
                    return lost_count < count
            return False

        @staticmethod
        @cache
        def python_version(host: nstr = None) -> nstr:
            def parse_version(value: str) -> str:
                return j(value.strip().split(" ")[1:])

            if SGB.SYS.host_is_local(host):
                return sys.version.split(" ")[0]
            result: nstr = None
            host_is_linux: bool = SGB.SYS.is_linux(host)
            if host_is_linux:
                result = first(
                    SGB.RESULT.SSH.execute(
                        j_s((PYTHON.EXECUTOR3, PYTHON.COMMAND.VERSION)), host
                    ).data
                )
            else:
                # result_list: list[nstr] = []
                for executor_name in (
                    PYTHON.EXECUTOR_ALIAS,
                    PYTHON.EXECUTOR,
                ):
                    command: strtuple = (
                        executor_name,
                        PYTHON.COMMAND.VERSION,
                    )
                    complete_process: CompletedProcess = SGB.EXECUTOR.execute(
                        SGB.EXECUTOR.create_command_for_psexec(
                            command, host, interactive=True
                        ),
                        True,
                        True,
                    )
                    stderr: str = complete_process.stderr
                    if ne(stderr):
                        if stderr.find(j_s(("could not start", executor_name))) != -1:
                            continue
                    result = str(complete_process.stdout)
            if nn(result):
                return parse_version(result)
            return None

        @staticmethod
        def get_disk_statistics_list(host: str) -> list[DiskStatistics]:
            output: str = SGB.EXECUTOR.execute(
                j_s(
                    (
                        CONST.POWERSHELL.NAME,
                        "Get-WmiObject -Class win32_logicalDisk -ComputerName",
                        host,
                    )
                ),
                True,
                True,
                as_shell=True,
            ).stdout
            result: list[DiskStatistics] = []
            delimiter: str = ": "
            delimiter_length: int = len(delimiter)
            disk_statistics: DiskStatistics | None = None
            for line in ListTool.not_empty_items(output.splitlines()):
                line: str = line
                if line.startswith("DeviceID"):
                    disk_statistics = DiskStatistics(
                        line[line.find(delimiter) + delimiter_length : -1]
                    )
                    result.append(disk_statistics)
                if line.startswith("FreeSpace"):
                    disk_statistics.free_space = DataTool.if_not_empty(
                        line[line.find(delimiter) + delimiter_length :],
                        lambda item: int(item),
                        0,
                    )
                if line.startswith("Size"):
                    disk_statistics.size = DataTool.if_not_empty(
                        line[line.find(delimiter) + delimiter_length :],
                        lambda item: int(item),
                        0,
                    )
            return result

        @staticmethod
        def get_logged_user(name_or_ip: str) -> nstr:
            return DataTool.get_first_item(
                SGB.EXECUTOR.get_user_session_for_host(name_or_ip)
            )

        @staticmethod
        def get_user_session_id_for_host(name_or_ip: str) -> nint:
            return DataTool.get_last_item(
                SGB.EXECUTOR.get_user_session_for_host(name_or_ip)
            )

        @staticmethod
        def get_user_session_for_host(name_or_ip: str) -> tuple[str, int] | None:
            def get_login_and_session_id(result: nstr) -> tuple[str, int] | None:
                if nn(result):
                    for line in lw(result.splitlines()[1:]):
                        if line.find("активно") != -1 or line.find("active") != -1:
                            data: strlist = ListTool.not_empty_items(line.split(" "))
                            return (data[1], int(data[2]))
                return None

            login_and_session_id: tuple[str, int] | None = get_login_and_session_id(
                SGB.EXECUTOR.execute_for_result(
                    ("qwinsta", "/server", name_or_ip),
                    encoding=WINDOWS.CHARSETS.ALTERNATIVE,
                )
            )
            if n(login_and_session_id):
                login_and_session_id = SGB.EXECUTOR.execute_for_result(
                    SGB.EXECUTOR.create_command_for_powershell(
                        (
                            j_s(
                                (
                                    "Get-WmiObject -ComputerName",
                                    name_or_ip,
                                    "-Class Win32_ComputerSystem | Select-Object UserName",
                                )
                            ),
                        )
                    ),
                )
                if nn(login_and_session_id):
                    login: nstr = login_and_session_id[0]
                    if login.find("\\") != -1:
                        login = login.split("\\")[1]
                    elif login.find(CONST.DOMAIN_SPLITTER) != -1:
                        login = login.split(CONST.DOMAIN_SPLITTER)[0]
                    else:
                        login_and_session_id = None
            if n(login_and_session_id):
                login_and_session_id = get_login_and_session_id(
                    SGB.EXECUTOR.execute_for_result(
                        ("query", "user", j(("/server:", name_or_ip))),
                        False,
                        encoding=WINDOWS.CHARSETS.ALTERNATIVE,
                    )
                )

            return login_and_session_id

        @staticmethod
        def ping(
            address_or_ip: str,
            host: nstr = None,
            count: int = 1,
            timeout: nint = None,
        ):
            timeout = timeout or 100
            command_list: strtuple = (
                "ping",
                "-4",
                address_or_ip,
                "-n",
                str(count),
                "-w",
                str(timeout),
            )
            result: CompletedProcess = SGB.EXECUTOR.execute(
                (
                    command_list
                    if n(host)
                    else SGB.EXECUTOR.create_command_for_psexec(
                        command_list, host, interactive=None
                    )
                ),
                True,
                True,
                encoding=CHARSETS.WINDOWS_ALTERNATIVE,
            )
            output: str = result.stdout
            return SGB.DATA.CHECK.returncode(result) and (
                output.count("(TTL)") < count or output.count("TTL=") < count
            )

        @staticmethod
        def get_executor_path(executor_name: str) -> str:
            return SGB.PATH.for_windows(
                SGB.PATH.join(PATHS.FACADE.TOOLS(), PSTOOLS.NAME, executor_name)
            )

        @staticmethod
        def create_command_for_executor(
            executor_name: str,
            command: strtuple | str,
            login: nstr = None,
            password: nstr = None,
            use_raw_login: bool = False,
        ) -> strtuple:
            if not isinstance(command, tuple):
                command = (command,)
            login = if_else(
                e(login),
                None,
                lambda: (
                    login
                    if use_raw_login
                    else SGB.DATA.FORMAT.login(AD.DOMAIN_DNS, login)
                ),
            )
            return (
                tuple(
                    [
                        SGB.PATH.path(SGB.EXECUTOR.get_executor_path(executor_name)),
                        PSTOOLS.NO_BANNER,
                        PSTOOLS.ACCEPTEULA,
                    ]
                    + if_else(e(login), [], lambda: ["-u", login])
                    + if_else(e(password), [], lambda: ["-p", password])
                )
                + command
            )

        @staticmethod
        def create_command_for_powershell(command: strtuple) -> strtuple:
            if command[0].lower() != POWERSHELL.NAME:
                command = (POWERSHELL.NAME,) + command
            return command

        @staticmethod
        def create_command_for_psexec_powershell(
            command: strtuple,
            host: nstr = None,
            login: nstr = None,
            password: nstr = None,
            interactive: nbool = False,
            run_from_system_account: bool = False,
            run_with_elevetion: bool = False,
            allow_use_local_host: bool = True,
            use_raw_host_name: bool = False,
            use_raw_login: bool = False,
        ) -> strtuple:
            return SGB.EXECUTOR.create_command_for_psexec(
                SGB.EXECUTOR.create_command_for_powershell(command),
                host,
                login,
                password,
                interactive,
                run_from_system_account,
                run_with_elevetion,
                allow_use_local_host,
                use_raw_host_name,
                use_raw_login,
            )

        @staticmethod
        def create_command_for_psexec(
            command: strtuple,
            host: nstr = None,
            login: nstr = None,
            password: nstr = None,
            interactive: nbool | tuple[bool, int] = False,
            run_from_system_account: bool = False,
            run_with_elevetion: bool = False,
            allow_use_local_host: bool = True,
            use_raw_host_name: bool = False,
            use_raw_login: bool = False,
        ) -> strtuple:
            interactive_is_tuple: bool = isinstance(interactive, tuple)
            command_prefix: strlist = DataTool.check_not_none(
                interactive,
                lambda: (
                    [["-d", "-i"][1 if interactive_is_tuple else interactive]]
                    + (
                        []
                        if not interactive_is_tuple
                        else ([interactive[1]] + ["-d"] if not interactive[0] else [])
                    )
                ),
                [],
            )
            local_host: bool = allow_use_local_host and SGB.SYS.host_is_local(host)
            if not local_host:
                if ne(host):
                    command_prefix.append(
                        SGB.DATA.FORMAT.host(
                            host, use_default_domain=not use_raw_host_name
                        )
                    )
                login = (
                    SGB.DATA.FORMAT.link(LINK.ADMINISTRATOR_LOGIN)
                    if SGB.EXECUTOR.client.call_with_service
                    else (
                        login
                        or SGB.DATA.VARIABLE.ENVIRONMENT.value(
                            LINK.ADMINISTRATOR_LOGIN, False
                        )
                    )
                )
                password = (
                    SGB.DATA.FORMAT.link(LINK.ADMINISTRATOR_PASSWORD)
                    if SGB.EXECUTOR.client.call_with_service
                    else (
                        password
                        or SGB.DATA.VARIABLE.ENVIRONMENT.value(
                            LINK.ADMINISTRATOR_PASSWORD, False
                        )
                    )
                )
            if run_from_system_account:
                command_prefix.append("-s")
            if run_with_elevetion:
                command_prefix.append("-h")
            return SGB.EXECUTOR.create_command_for_executor(
                PSTOOLS.PS_EXECUTOR,
                tuple(command_prefix) + command,
                login,
                password,
                use_raw_login,
            )

        @staticmethod
        def create_command_for_start_service(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            interactive: nbool = False,
            host: nstr = None,
            as_standalone: bool = False,
        ) -> strtuple:
            description: ServiceDescription = ServiceRoleTool.service_description(
                service_object
            )
            python_command: strtuple = (
                ()
                if as_standalone
                else (description.python_executable_path or PYTHON.EXECUTOR_ALIAS,)
            )

            is_local: bool = SGB.SYS.host_is_local(host or description.host)

            def local_action(value: Any) -> Any:
                return if_else(is_local, None, value)

            login: nstr = local_action(
                DataTool.check_not_none(
                    description.login,
                    lambda: SGB.DATA.FORMAT.variable(
                        description.login, from_environment=True
                    ),
                )
            )
            password: nstr = local_action(
                DataTool.check_not_none(
                    description.password,
                    lambda: SGB.DATA.FORMAT.variable(
                        description.password, from_environment=True
                    ),
                )
            )
            interactive = local_action(interactive)
            return (
                SGB.EXECUTOR.create_command_for_powershell(python_command)
                if is_local
                else SGB.EXECUTOR.create_command_for_psexec(
                    python_command,
                    host or local_action(SGB.SERVICE.client.get_host(service_object)),
                    login,
                    password,
                    interactive,
                    description.run_from_system_account,
                    False,
                )
            )

        client: IResultExecutorClient = ExecutorClient.RESULT()

        @staticmethod
        def execute(
            command: strtuple | str,
            show_output: bool = False,
            capture_output: bool = False,
            command_as_text: bool = True,
            as_shell: bool = False,
            encoding: nstr = None,
            call_with_service: bool = False,
        ) -> CompletedProcess:
            if (
                SGB.SYS.is_linux()
                or call_with_service
                or SGB.EXECUTOR.client.call_with_service
            ):
                if SGB.SERVICE.check_on_availabllity(SERVICE_ROLE.EXECUTOR):
                    return SGB.EXECUTOR.client.execute(
                        command,
                        show_output,
                        capture_output,
                        command_as_text,
                        as_shell,
                        encoding,
                    ).data
            if show_output:
                if capture_output:
                    process_result = subprocess.run(
                        command,
                        capture_output=True,
                        text=command_as_text,
                        shell=as_shell,
                        encoding=encoding,
                    )
                else:
                    process_result = subprocess.run(command, text=command_as_text)
            else:
                process_result = subprocess.run(
                    command, stdout=DEVNULL, stderr=STDOUT, text=command_as_text
                )
            return process_result

        @staticmethod
        def extract_result(value: CompletedProcess) -> nstr:
            result: str = str(value.stdout).strip()
            return None if e(result) else result

        @staticmethod
        def extract_not_found(value: CompletedProcess) -> bool:
            error: str = lw(value.stderr).strip()
            return (
                False
                if e(error)
                else error.find("не удается найти указанный файл") != -1
            )

        @staticmethod
        def execute_for_result(
            command: strtuple | str,
            command_as_text: bool = True,
            as_shell: bool = False,
            encoding: nstr = None,
        ) -> nstr:
            return SGB.EXECUTOR.extract_result(
                SGB.EXECUTOR.execute(
                    command,
                    True,
                    True,
                    command_as_text,
                    as_shell,
                    encoding,
                )
            )

        @staticmethod
        def python_for_result(
            command: strtuple | str,
            host: nstr = None,
            is_linux: nbool = None,
        ) -> nstr:
            complete_process: CompletedProcess | None = None
            if n(is_linux) or not is_linux:
                complete_process = SGB.EXECUTOR.execute_python_for_windows(
                    command, host
                )
            if nn(complete_process):
                return SGB.EXECUTOR.extract_result(complete_process)
            return first(SGB.RESULT.SSH.execute_python(command, host))

        @staticmethod
        def execute_python_for_windows(
            command: strtuple | str, host: nstr = None
        ) -> CompletedProcess | None:
            command = j(command, ";") if isinstance(command, tuple) else command
            for executor_name in (PYTHON.EXECUTOR_ALIAS, PYTHON.EXECUTOR):
                command_list: strtuple = (
                    executor_name,
                    PYTHON.COMMAND.FLAG,
                    command,
                )
                result = SGB.EXECUTOR.execute(
                    (
                        command_list
                        if SGB.SYS.host_is_local(host)
                        else SGB.EXECUTOR.create_command_for_psexec(
                            command_list,
                            host,
                            interactive=True,
                        )
                    ),
                    show_output=True,
                    capture_output=True,
                )
                if SGB.DATA.CHECK.complete_process_wrong_descriptor(result):
                    return None
                if SGB.DATA.CHECK.returncode(result):
                    return result
            return None

        @staticmethod
        def execute_python_localy(
            text: str,
            parameters: strdict | None = None,
            stdout_redirect: nbool = True,
            catch_exceptions: bool = False,
            use_default_stdout: bool = False,
        ) -> str | strdict | None:
            result_parameters: strdict = globals()
            if nn(parameters):
                for key, value in parameters.items():
                    result_parameters[key] = value
            if "self" not in result_parameters:
                result_parameters["self"] = OutputStub()
            if "self" in result_parameters:
                if use_default_stdout:
                    OutputStub().set_to(globals()["self"])

            def action() -> None:

                try:
                    exec(
                        text,
                        globals(),
                        result_parameters,
                    )
                except Exception as exception:
                    if catch_exceptions:
                        raise exception

                    SGB.ERROR.global_except_hook(exception, SGB.SYS.host())

            if stdout_redirect or n(stdout_redirect):
                stdout = StringIO()
                with redirect_stdout(stdout):
                    action()
                    if n(stdout_redirect):
                        return globals()
                    return stdout.getvalue()
            else:
                action()
                return globals()
            return None

        @staticmethod
        def python_via_psexec_for_result(
            command: strtuple | str, host: nstr = None
        ) -> str:
            return SGB.EXECUTOR.extract_result(
                SGB.EXECUTOR.execute_python_for_windows(command, host)
            )

        @staticmethod
        def kill_process(
            name_or_pid: str | int,
            host: nstr = None,
            via_standart_tools: bool = True,
            show_output: bool = False,
        ) -> bool:
            local: bool = SGB.SYS.host_is_local(host)
            if via_standart_tools:
                is_string: bool = isinstance(name_or_pid, str)
                command: strtuple = ("taskkill",)
                if not local:
                    command += ("/s", host)
                return (
                    SGB.EXECUTOR.execute(
                        command
                        + (
                            "/t",
                            "/f",
                            "/im" if is_string else "/pid",
                            (
                                SGB.PATH.add_extension(name_or_pid, FILE.EXTENSION.EXE)
                                if is_string
                                else str(name_or_pid)
                            ),
                        ),
                        show_output,
                    ).returncode
                    < 2
                )

            return SGB.DATA.EXTRACT.returncode(
                SGB.EXECUTOR.execute(
                    SGB.EXECUTOR.create_command_for_executor(
                        PSTOOLS.PS_KILL_EXECUTOR,
                        (
                            (
                                str(name_or_pid)
                                if local
                                else (host or SGB.SYS.host(), "-t", str(name_or_pid))
                            ),
                        ),
                        show_output,
                    )
                )
            )

        @staticmethod
        def check_process_is_running(
            pid_or_name: int | str,
            host: nstr = None,
            login: nstr = None,
            password: nstr = None,
        ) -> bool:
            value_is_str: bool = isinstance(pid_or_name, str)
            if value_is_str:
                pid_or_name = SGB.PATH.add_extension(pid_or_name, FILE.EXTENSION.EXE)
            command_list: strlist = [
                "tasklist",
                "/fi",
                esc(
                    j_s(
                        (
                            ["pid", "imagename"][value_is_str],
                            "eq",
                            pid_or_name,
                        )
                    )
                ),
                "/fo",
                "list",
            ]
            login = SGB.DATA.FORMAT.login(
                AD.DOMAIN_DNS,
                login
                or SGB.DATA.VARIABLE.ENVIRONMENT.value(LINK.ADMINISTRATOR_LOGIN, False),
            )
            password = password or SGB.DATA.VARIABLE.ENVIRONMENT.value(
                LINK.ADMINISTRATOR_PASSWORD
            )
            if ne(host):
                command_list += ["/s", host]
                command_list += ["/u", login]
                command_list += ["/p", password]
            output: str = (
                bytes(
                    SGB.EXECUTOR.execute(
                        command_list, True, True, command_as_text=False
                    ).stdout
                )
                .decode(WINDOWS.CHARSETS.ALTERNATIVE)
                .lower()
            )
            return output.find("pid") != -1

        @staticmethod
        def kill_python_process(
            host: str, via_standart_tools: bool, show_output: bool = False
        ) -> bool:
            return SGB.EXECUTOR.kill_process(
                PYTHON.EXECUTOR, host, via_standart_tools, show_output=show_output
            )

        @staticmethod
        def _ws_action(value: str, host: str, show_output: bool = False) -> bool:
            return SGB.DATA.EXTRACT.returncode(
                SGB.EXECUTOR.execute(
                    SGB.EXECUTOR.create_command_for_psexec(
                        ("shutdown", value, "/t", "0"), host
                    ),
                    show_output,
                )
            )

        @staticmethod
        def ws_reboot(host: str, show_output: bool = False) -> bool:
            return SGB.EXECUTOR._ws_action("/r", host, show_output)

        @staticmethod
        def ws_shutdown(host: str, show_output: bool = False) -> bool:
            return SGB.EXECUTOR._ws_action("/s", host, show_output)

    class EVENT:

        @staticmethod
        def send(
            value: Events,
            parameters: tuple[Any, ...] | Any = None,
            flags: nint = None,
            ignore_send_once: bool = False,
            block: bool = False,
            send_on_accessibility: bool = False,
        ) -> bool:
            if send_on_accessibility:
                block = False
            elif not SGB.SERVICE.check_on_availabllity(SERVICE_ROLE.EVENT):
                return False
            if not ignore_send_once and BM.has(
                EnumTool.get(value).flags, LogMessageFlags.SEND_ONCE
            ):
                if SGB.CHECK.EVENTS.has_by_key(value, parameters):
                    return False

            def internal_send(
                command_name: str, parameters: strdict, flags: nint
            ) -> Any:
                if send_on_accessibility:
                    while_not_do(
                        lambda: SGB.SERVICE.check_on_availabllity(SERVICE_ROLE.EVENT),
                        sleep_time=1,
                    )
                try:
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.send_event,
                            (command_name, parameters, flags),
                        )
                    )
                except Error as error:
                    SGB.output.error("Log send error")

            if block:
                return SGB.ERROR.wrap(
                    lambda: internal_send(
                        value.name,
                        SGB.EVENT.BUILDER.create_parameters_map(
                            value, DataTool.as_list(parameters)
                        ),
                        flags,
                    )
                )()
            SGB.LOG.executor.submit(
                SGB.ERROR.wrap(internal_send),
                value.name,
                SGB.EVENT.BUILDER.create_parameters_map(
                    value, DataTool.as_list(parameters)
                ),
                flags,
            )
            return True

        @staticmethod
        def mri_filter_was_changed() -> None:
            SGB.EVENT.send(
                Events.MRI_CHILLER_FILTER_WAS_CHANGED,
                (
                    SGB.DATA.MATERIALIZED_RESOURCES.get_quantity(
                        MATERIALIZED_RESOURCES.Types.CHILLER_FILTER
                    ),
                ),
            )

        @staticmethod
        def computer_was_started(name: str) -> None:
            SGB.EVENT.send(Events.COMPUTER_WAS_STARTED, (name,))

        @staticmethod
        def server_was_started(name: str) -> None:
            SGB.EVENT.send(Events.SERVER_WAS_STARTED, (name,))

        @staticmethod
        def get_parameter(
            event: Events, parameters: strdict, parameter_name: nstr = None
        ) -> Any | strdict:
            parameters_map: strdict = SGB.EVENT.BUILDER.create_parameters_map(
                event, parameters
            )
            return DataTool.check_not_none(
                parameter_name, lambda: parameters_map[parameter_name], parameters_map
            )

        class BUILDER:
            @staticmethod
            def create_parameters_map(
                event: Events,
                parameters: tuple[Any, ...] | None = None,
                check_for_parameters_count: bool = True,
            ) -> strdict:
                event_description: EventDescription = EnumTool.get(event)
                parameter_pattern_list: list = DataTool.as_list(
                    event_description.params
                )
                parameters = parameters or ()
                if check_for_parameters_count and len(parameter_pattern_list) > len(
                    parameters
                ):
                    raise Exception(
                        "Income parameter list length is less that parameter list length of command"
                    )
                result: strdict = {}
                for index, parameter_pattern_item in enumerate(parameter_pattern_list):
                    if index < len(parameters):
                        parameter_pattern: ParamItem = parameter_pattern_item
                        value: Any = parameters[index]
                        if nn(value):
                            result[parameter_pattern.name] = value
                    else:
                        break
                return result

            @staticmethod
            def create_event(
                event: Events,
                paramters: Any = None,
                parameters_getter: Callable[[], tuple[Any, ...]] | None = None,
                default_value: tuple[Any, ...] | Any = None,
                check_all: bool = False,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return DataTool.check_not_none(
                    paramters,
                    lambda: (event, parameters_getter()),
                    event if n(default_value) else (event, default_value),
                    check_all,
                )

            @staticmethod
            def by_key(
                value: Events | None, parameters: tuple[Any, ...] | Any
            ) -> tuple[Events, tuple[Any, ...]]:
                event_description: EventDescription = EnumTool.get(value)
                key_len: int = len(
                    DataTool.filter(lambda item: item.key, event_description.params)
                )
                if len(parameters) != len(event_description.params):
                    if key_len == len(parameters):
                        result_parameters: list[Any] = []
                        index: int = 0
                        for item in event_description.params:
                            result_parameters.append(
                                parameters[index] if item.key else None
                            )
                            if item.key:
                                index += 1
                    parameters = result_parameters
                return (
                    value,
                    (
                        parameters
                        if key_len == 0
                        else DataTool.map(
                            lambda item: item[1] if item[0].key else None,
                            list(zip(event_description.params, parameters)),
                        )
                    ),
                )

            @staticmethod
            def polibase_person_with_inaccessable_email_was_detected(
                person: PolibasePerson | None = None,
                registrator_person: PolibasePerson | None = None,
                actual: bool = False,
            ) -> tuple[Events, tuple[Any, ...]] | Events:
                def get_information() -> tuple[Any, ...]:
                    workstation_name: str = "<не определён>"
                    workstation_description: str = "<не определён>"
                    if actual:
                        try:
                            user: User = SGB.RESULT.USER.by_polibase_pin(
                                registrator_person.pin
                            ).data
                            workstation: Workstation = (
                                SGB.RESULT.get_first_item(
                                    SGB.RESULT.WORKSTATION.by_login(user.login)
                                )
                                or SGB.RESULT.WORKSTATION.by_name(
                                    CONST.TEST.WORKSTATION_MAME
                                ).data
                            )
                            if nn(workstation):
                                workstation_name = workstation.name
                                workstation_description = workstation.description
                        except NotFound as _:
                            pass
                    return (
                        person.FullName,
                        person.pin,
                        person.email,
                        registrator_person.FullName,
                        workstation_name,
                        workstation_description,
                    )

                event: Events = (
                    Events.POLIBASE_PERSON_WITH_INACCESSABLE_EMAIL_WAS_DETECTED
                )
                return SGB.EVENT.BUILDER.create_event(
                    event,
                    registrator_person,
                    get_information,
                    DataTool.check_not_none(person, lambda: (None, person.pin)),
                )

            @staticmethod
            def polibase_person_duplication_was_detected(
                person: PolibasePerson | None = None,
                duplicated_person: PolibasePerson | None = None,
                registrator_person: PolibasePerson | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                event: Events = Events.POLIBASE_PERSON_DUPLICATION_WAS_DETECTED

                def get_information() -> tuple[Any, ...]:
                    return (
                        person.FullName,
                        person.pin,
                        duplicated_person.pin,
                        duplicated_person.pin,
                        registrator_person.FullName,
                    )

                return SGB.EVENT.BUILDER.create_event(event, person, get_information)

            @staticmethod
            def polibase_person_email_was_added(
                value: PolibasePerson | None = None,
                value_for_search: PolibasePerson | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.POLIBASE_PERSON_EMAIL_WAS_ADDED,
                    value,
                    lambda: (value.FullName, value.pin, value.email),
                    DataTool.check_not_none(
                        value_for_search, lambda: (None, value_for_search.pin)
                    ),
                )

            @staticmethod
            def ask_for_polibase_person_email(
                value: PolibasePerson | None = None,
                localy: bool = True,
                secret: nint = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.ASK_FOR_POLIBASE_PERSON_EMAIL,
                    value,
                    lambda: (value.FullName, value.pin, localy, randrange(100000)),
                    None if n(secret) else (None, None, None, secret),
                )

            @staticmethod
            def indication_device_was_registered(
                value: IndicationDevice | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.INDICATION_DEVICES_WAS_REGISTERED,
                    value,
                    lambda: (value.name, value.description, value.ip_address),
                )

            @staticmethod
            def service_was_started(
                information: ServiceInformation | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.SERVICE_WAS_STARTED,
                    information,
                    lambda: (
                        information.name,
                        information.host,
                        information.port,
                        information.pid,
                        information,
                    ),
                )

            @staticmethod
            def service_is_being_started(
                information: ServiceInformation | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.SERVICE_IS_BEING_STARTED,
                    information,
                    lambda: (
                        information.name,
                        information.host,
                        information.port,
                    ),
                )

            @staticmethod
            def chiller_temperature_alert_was_fired() -> Events:
                return SGB.EVENT.BUILDER.create_event(
                    Events.MRI_CHILLER_TEMPERATURE_ALERT_WAS_FIRED
                )

            @staticmethod
            def chiller_temperature_alert_was_resolved() -> Events:
                return SGB.EVENT.BUILDER.create_event(
                    Events.MRI_CHILLER_TEMPERATURE_ALERT_WAS_RESOLVED
                )

            @staticmethod
            def polibase_person_set_card_registry_folder(
                name: nstr = None,
                person: PolibasePerson | None = None,
                registrator: PolibasePerson | None = None,
                set_by_polibase: bool = True,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                person_pin: nint = None if n(person) else person.pin
                if set_by_polibase:
                    return SGB.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_WAS_SET_FOR_POLIBASE_PERSON,
                        (name, person, registrator),
                        lambda: (
                            person_pin,
                            (
                                None
                                if n(name)
                                else SGB.DATA.FORMAT.polibase_person_card_registry_folder(
                                    name
                                )
                            ),
                            None if n(registrator) else registrator.FullName,
                            None if n(registrator) else registrator.pin,
                        ),
                    )
                else:
                    return SGB.EVENT.BUILDER.create_event(
                        Events.CARD_REGISTRY_FOLDER_WAS_SET_NOT_FROM_POLIBASE_FOR_POLIBASE_PERSON,
                        (person_pin,),
                        lambda: (person_pin,),
                    )

            @staticmethod
            def polibase_person_set_suitable_card_registry_folder(
                name: nstr = None,
                person_or_pin: PolibasePerson | nint = None,
                registrator: PolibasePerson | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.CARD_REGISTRY_SUITABLE_FOLDER_WAS_SET_FOR_POLIBASE_PERSON,
                    (name, person_or_pin, registrator),
                    lambda: (
                        DataTool.if_not_empty(
                            person_or_pin,
                            lambda person: SGB.RESULT.POLIBASE._person_pin(person),
                        ),
                        (
                            None
                            if n(name)
                            else SGB.DATA.FORMAT.polibase_person_card_registry_folder(
                                name
                            )
                        ),
                        None if n(registrator) else registrator.FullName,
                        None if n(registrator) else registrator.pin,
                    ),
                )

            @staticmethod
            def card_registry_folder_was_registered(
                name: nstr = None,
                place_a: nint = None,
                place_b: nint = None,
                place_c: nint = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                if nn(name):
                    name = SGB.DATA.FORMAT.polibase_person_card_registry_folder(name)
                return SGB.EVENT.BUILDER.create_event(
                    Events.CARD_REGISTRY_FOLDER_WAS_REGISTERED,
                    name,
                    lambda: (name, place_a, place_b, place_c),
                )

            @staticmethod
            def card_registry_folder_start_card_sorting(
                name: nstr = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.CARD_REGISTRY_FOLDER_START_CARD_SORTING,
                    name,
                    lambda: (name,),
                )

            @staticmethod
            def card_registry_folder_complete_card_sorting(
                name: nstr = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.CARD_REGISTRY_FOLDER_COMPLETE_CARD_SORTING,
                    name,
                    lambda: (
                        SGB.DATA.FORMAT.polibase_person_card_registry_folder(name),
                    ),
                )

            staticmethod

            def chiller_was_turned_off() -> Events:
                return SGB.EVENT.BUILDER.create_event(Events.MRI_CHILLER_WAS_TURNED_OFF)

            @staticmethod
            def chiller_was_turned_on() -> Events:
                return SGB.EVENT.BUILDER.create_event(Events.MRI_CHILLER_WAS_TURNED_ON)

            @staticmethod
            def service_was_stopped(
                information: ServiceDescriptionBase | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.SERVICE_WAS_STOPPED,
                    information,
                    lambda: (information.name, information),
                )

            @staticmethod
            def polibase_persons_barcodes_old_format_were_detected(
                person_pin_list: list[int] | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.POLIBASE_PERSONS_WITH_OLD_FORMAT_BARCODE_WAS_DETECTED,
                    person_pin_list,
                    lambda: (person_pin_list,),
                )

            @staticmethod
            def polibase_person_barcodes_new_format_were_created(
                person_pin_list: list[int] | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.POLIBASE_PERSON_BARCODES_WITH_OLD_FORMAT_WERE_CREATED,
                    person_pin_list,
                    lambda: (person_pin_list,),
                )

            @staticmethod
            def polibase_person_was_created(
                value: PolibasePerson | None = None,
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.POLIBASE_PERSON_WAS_CREATED,
                    value,
                    lambda: (value.FullName, value.pin, value),
                )

            @staticmethod
            def mail_to_polibase_person_was_sent(
                id: nint = None, person_pin: nint = None
            ) -> Events | tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.MAIL_TO_POLIBASE_PERSON_WAS_SENT,
                    (id, person_pin),
                    lambda: (id, person_pin),
                )

            @staticmethod
            def polibase_person_was_updated(
                value: PolibasePerson | None = None,
            ) -> tuple[Events, tuple[Any, ...]]:
                return SGB.EVENT.BUILDER.create_event(
                    Events.POLIBASE_PERSON_WAS_UPDATED,
                    value,
                    lambda: (value.FullName, value.pin, value),
                )

        @staticmethod
        def polibase_person_answered(
            who: PolibasePerson, value: str, answer_type: int
        ) -> None:
            SGB.EVENT.send(
                Events.POLIBASE_PERSON_ANSWERED,
                (who.pin, who.telephoneNumber, plain(value), answer_type),
            )
            SGB.LOG.polibase(
                j_nl(
                    (
                        value,
                        "____",
                        j_s(("Тип ответа:", answer_type)),
                    )
                )
            )

        @staticmethod
        def resource_accessible(resource: ResourceStatus, at_first_time: bool) -> None:
            SGB.EVENT.send(
                Events.RESOURCE_ACCESSABLE, (resource.name, resource, at_first_time)
            )

        @staticmethod
        def resource_inaccessible(
            resource: ResourceStatus,
            at_first_time: bool,
            reason: ResourceInaccessableReasons | None = None,
        ) -> None:
            reason_string: str = ""
            reason_name: nstr = None
            if ne(reason):
                reason_string = j_s(("Причина:", reason.value))
                reason_name = reason.name
            SGB.EVENT.send(
                Events.RESOURCE_INACCESSABLE,
                (resource.name, resource, at_first_time, reason_string, reason_name),
            )

        @staticmethod
        def login() -> None:
            login: str = SGB.session.get_login()
            user: User = SGB.RESULT.USER.by_login(login).data
            SGB.EVENT.send(Events.LOG_IN, (user.name, login, SGB.SYS.host()))

        @staticmethod
        def whatsapp_message_received(message: WhatsAppMessage) -> None:
            SGB.EVENT.send(Events.WHATSAPP_MESSAGE_RECEIVED, (message,))

        @staticmethod
        def new_file_detected(path: str) -> None:
            SGB.EVENT.send(Events.NEW_FILE_DETECTED, (SGB.PATH.path(path),))

        @staticmethod
        def new_mail_message_was_received(value: NewMailMessage) -> None:
            SGB.EVENT.send(
                Events.NEW_EMAIL_MESSAGE_WAS_RECEIVED,
                (value.mailbox_address, value.subject, value.from_, value),
            )

        @staticmethod
        def new_polibase_scanned_document_detected(
            value: PolibaseDocument,
        ) -> None:
            SGB.EVENT.send(
                Events.NEW_POLIBASE_DOCUMENT_DETECTED,
                (value.polibase_person_pin, value.file_path, value.document_type, 0),
            )

        @staticmethod
        def new_polibase_scanned_document_processed(file_path: str) -> None:
            event_ds: EventDS | None = first(
                SGB.RESULT.EVENTS.get(
                    Events.NEW_POLIBASE_DOCUMENT_DETECTED, (None, file_path)
                )
            )
            if nn(event_ds):
                parameters: strdict = event_ds.parameters
                SGB.EVENT.send(
                    Events.NEW_POLIBASE_DOCUMENT_DETECTED,
                    (
                        parameters[PARAM_ITEMS.PERSON_PIN.name],
                        file_path,
                        parameters[PARAM_ITEMS.DOCUMENT_NAME.name],
                        1,
                    ),
                )

        @staticmethod
        def start_session() -> None:
            argv: strlist | None = SGB.session.argv
            argv_str: str = ""
            if ne(argv):
                argv_str = j_s(argv)
                argv_str = f"({argv_str})"
            login: str = SGB.session.get_login()
            user: User = SGB.RESULT.USER.by_login(login).data
            SGB.EVENT.send(
                Events.SESSION_STARTED,
                (
                    user.name,
                    login,
                    j_s((SGB.session.file_name, argv_str)),
                    SGB.VERSION.value,
                    SGB.SYS.host(),
                ),
            )

        @staticmethod
        def backup_robocopy_job_was_started(
            name: str, job_status: RobocopyJobStatus
        ) -> None:
            SGB.EVENT.send(
                Events.BACKUP_ROBOCOPY_JOB_WAS_STARTED, (name, job_status.pid)
            )

        @staticmethod
        def backup_robocopy_job_was_completed(
            name: str, job_status: RobocopyJobStatus
        ) -> None:
            status: int = job_status.last_status
            is_live: bool = job_status.pid > 0
            status_string: str = "live job" if is_live else str(status)
            pid_string: str = str(job_status.pid) if is_live else "not live job"
            if status >= ROBOCOPY.ERROR_CODE_START:
                status_string = j_s((status_string, "(есть ошибки)"))
            SGB.EVENT.send(
                Events.BACKUP_ROBOCOPY_JOB_WAS_COMPLETED,
                (name, status_string, status, pid_string),
            )

        @staticmethod
        def service_is_inaccessable_and_will_be_restarted(
            service_information: ServiceInformation,
        ) -> None:
            SGB.EVENT.send(
                Events.SERVICE_IS_INACCESIBLE_AND_WILL_BE_RESTARTED,
                (service_information.name, service_information),
            )

        @staticmethod
        def service_was_not_started(
            service_information: ServiceInformation, error: str
        ) -> None:
            SGB.EVENT.send(
                Events.SERVICE_WAS_NOT_STARTED,
                (
                    service_information.name,
                    service_information.host,
                    service_information.port,
                    error,
                    service_information,
                ),
            )

        """
        @staticmethod
        def service_was_started(service_information: ServiceInformation) -> None:
            SGB.EVENT.send(
                *SGB.EVENT.BUILDER.service_was_started(service_information),
            )
        """
        """
        @staticmethod
        def service_is_being_started(service_information: ServiceInformation) -> None:
            SGB.EVENT.send(
                *SGB.EVENT.BUILDER.service_is_being_started(service_information),
            )'
        """

        @staticmethod
        def hr_notify_about_new_employee(login: User) -> None:
            user: User = SGB.RESULT.USER.by_login(login, True, False).data
            hr_user: User = ResultTool.get_first_item(
                SGB.RESULT.USER.by_job_position(AD.JobPositions.HR)
            )
            SGB.EVENT.send(
                Events.HR_NOTIFY_ABOUT_NEW_EMPLOYEE,
                (FullNameTool.to_given_name(hr_user.name), user.name, user.mail),
            )

        @staticmethod
        def it_notify_about_create_user(
            login: str, password: str, additional_information: str
        ) -> None:
            it_user_list: list[User] = SGB.RESULT.USER.by_job_position(
                AD.JobPositions.IT
            ).data
            me_user_login: str = SGB.session.get_login()
            it_user_list = DataTool.filter(
                lambda user: user.login != me_user_login, it_user_list
            )
            it_user: User = it_user_list[0]
            user: User = SGB.RESULT.USER.by_login(login).data
            SGB.EVENT.send(
                Events.IT_NOTIFY_ABOUT_CREATE_USER,
                (
                    user.name,
                    user.description,
                    user.login,
                    password,
                    user.telephoneNumber,
                    user.mail,
                    additional_information,
                ),
            )
            SGB.EVENT.send(
                Events.IT_TASK_AFTER_CREATE_USER,
                (
                    FullNameTool.to_given_name(it_user.name),
                    user.name,
                    user.mail,
                    password,
                    additional_information,
                ),
            )

        @staticmethod
        def it_notify_about_create_person(
            full_name: FullName,
            email_address: str,
            password: str,
            description: str,
            telephone_number: str,
        ) -> None:
            it_user_list: list[User] = SGB.RESULT.USER.by_job_position(
                AD.JobPositions.IT
            ).data
            me_user_login: str = SGB.session.get_login()
            it_user_list = DataTool.filter(
                lambda user: user.login != me_user_login, it_user_list
            )
            it_user: User = it_user_list[0]
            SGB.EVENT.send(
                Events.IT_NOTIFY_ABOUT_CREATE_PERSON,
                (
                    FullNameTool.fullname_to_string(full_name),
                    email_address,
                    description,
                    password,
                    telephone_number,
                ),
            )
            SGB.EVENT.send(
                Events.IT_TASK_AFTER_CREATE_PERSON,
                (
                    FullNameTool.to_given_name(it_user.name),
                    FullNameTool.fullname_to_string(full_name),
                    email_address,
                    password,
                ),
            )

        @staticmethod
        def printer_report(name: str, location: str, report_text: str) -> None:
            SGB.EVENT.send(Events.PRINTER_REPORT, (name, location, report_text))

        @staticmethod
        def on_service_command(
            value: SERVICE_COMMAND,
            handler: Callable[[ParameterList, IClosable], None],
            block: bool = True,
        ) -> None:
            def thread_handler() -> None:
                ServiceListener().listen_for(
                    [value],
                    lambda _, pl, service_listener: handler(pl, service_listener),
                )

            if block:
                thread_handler()
            else:
                SGBThread(thread_handler)

        @staticmethod
        def on_event(
            handler: Callable[[ParameterList, IClosable], None],
            block: bool = True,
        ) -> None:
            SGB.EVENT.on_service_command(SERVICE_COMMAND.send_event, handler, block)

        @staticmethod
        def wait_server_start(
            handler_or_server_name: Callable[[str, Callable[[], None]], None] | str,
        ) -> None:
            def internal_handler(pl: ParameterList, listener: IClosable) -> None:
                event, parameters = SGB.DATA.EXTRACT.EVENT.with_parameters(pl)
                if event == Events.SERVER_WAS_STARTED:
                    server_name: str = parameters[0]
                    if callable(handler_or_server_name):
                        handler_or_server_name(server_name, listener.close)
                    else:
                        if handler_or_server_name.startswith(server_name):
                            listener.close()

            SGB.EVENT.on_event(internal_handler)

        @staticmethod
        def on_service_starts(
            handler_or_service_role_or_information: (
                Callable[[str, Callable[[], None]], None]
                | SERVICE_ROLE
                | ServiceDescriptionBase
            ),
        ) -> None:
            def internal_handler(pl: ParameterList, listener: ServiceListener) -> None:
                event, parameters = SGB.DATA.EXTRACT.EVENT.with_parameters(pl)
                if event == SGB.EVENT.BUILDER.service_was_started():
                    service_description_name: str = parameters[0]
                    if callable(handler_or_service_role_or_information):
                        handler_or_service_role_or_information(
                            service_description_name, listener.close
                        )
                    elif (
                        handler_or_service_role_or_information
                        == service_description_name
                    ):
                        listener.close()

            SGB.EVENT.on_event(internal_handler)

        @staticmethod
        def on_robocopy_job_complete(
            handler_or_robocopy_job_name: (
                Callable[[str, int, ServiceListener], None] | str
            ),
        ) -> nbool:
            class DH:
                result: nbool = None

            def internal_handler(pl: ParameterList, listener: ServiceListener) -> None:
                event, parameters = SGB.DATA.EXTRACT.EVENT.with_parameters(pl)
                if event == Events.BACKUP_ROBOCOPY_JOB_WAS_COMPLETED:
                    robocopy_job_status_name: str = parameters[0]
                    robocopy_job_status: int = parameters[-1]
                    DH.result = robocopy_job_status < ROBOCOPY.ERROR_CODE_START
                    if callable(handler_or_robocopy_job_name):
                        handler_or_robocopy_job_name(
                            robocopy_job_status_name, robocopy_job_status, listener
                        )
                    else:
                        if robocopy_job_status_name.startswith(
                            handler_or_robocopy_job_name
                        ):
                            listener.close()

            SGB.EVENT.on_event(internal_handler)
            return DH.result

    class SERVICE(ServiceTool):

        command_map: dict[SERVICE_COMMAND, ServiceDescription] = {}
        client: ServiceClient = ServiceClient(RootSuppport())

        ClientBase.service_client = client

        @staticmethod
        def collection() -> IServiceCollection:
            return SGB.SERVICE.client.service_collection

        @staticmethod
        def collection_list() -> list[ServiceInformation]:
            return DataTool.to_list(SGB.SERVICE.collection().get())

        @staticmethod
        def get_information(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            cached: bool = True,
        ) -> ServiceInformation | None:
            return SGB.SERVICE.client.get_information(service_object, cached)

        @staticmethod
        def check_on_host_chanchable(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> bool:
            description: ServiceDescription = ServiceRoleTool.service_description(
                service_object
            )
            return description.host_changeable or SGB.SYS.host_is_local(
                description.host
            )

        @staticmethod
        def call(
            service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
            command: SERVICE_COMMAND,
            parameters: Any = None,
            timeout: nint = None,
            blocked: bool = True,
        ) -> nstr:
            def action() -> nstr:
                return SGB.SERVICE.client.call_service(
                    service_object, command, parameters, timeout
                )

            if blocked:
                return action()
            else:
                SGBThread(action)
                return None

        @staticmethod
        def call_command(
            value: SERVICE_COMMAND | str,
            parameters: Any = None,
            timeout: nint = None,
            blocked: bool = True,
        ) -> nstr:
            return SGB.SERVICE.call(None, value, parameters, timeout, blocked)

        @staticmethod
        def call_command_for_service(
            value: SERVICE_ROLE | ServiceDescriptionBase,
            command: SERVICE_COMMAND | str,
            parameters: Any = None,
            timeout: nint = None,
            blocked: bool = True,
        ) -> nstr:
            return SGB.SERVICE.call(value, command, parameters, timeout, blocked)

        @staticmethod
        def get_support_host_list(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> strlist:
            return DataTool.filter(
                lambda item: item.name.startswith(
                    j(
                        (
                            SUPPORT_NAME_PREFIX,
                            ServiceRoleTool.service_description(service_object).name,
                        )
                    )
                ),
                SGB.SERVICE.client.service_collection.get(),
            )

        @staticmethod
        def clear_service_collection() -> None:
            SGB.SERVICE.client.service_collection.clear()

        @staticmethod
        def update_service_information(
            value: ServiceDescriptionBase | list[ServiceDescriptionBase],
            add: bool = True,
            overwrite: bool = False,
        ) -> None:
            SGB.SERVICE.client.service_collection.update(value, add, overwrite)

        @staticmethod
        def check_on_startable(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> nbool:
            service_description: ServiceDescription = EnumTool.get(service_object)
            login_value: nstr = service_description.login
            login_variable_name_list: strlist | None = SGB.DATA.EXTRACT.variables(
                login_value
            )
            if ne(login_variable_name_list):
                if e(SGB.DATA.FORMAT.variable(login_value, True)):
                    raise Exception(
                        f"Login for start service {service_description.host} ({login_variable_name_list[0]}) is not set"
                    )
            if nn(login_value):
                password_value: nstr = service_description.password
                password_variable_name_list: strlist | None = (
                    SGB.DATA.EXTRACT.variables(password_value)
                )
                if ne(SGB.DATA.EXTRACT.variables(password_value)):
                    if e(SGB.DATA.FORMAT.variable(password_value, True)):
                        raise Exception(
                            f"Password for start service {service_description.host} ({password_variable_name_list[0]}) is not set"
                        )
            return True

        @staticmethod
        def change_host_on_local(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> None:
            ServiceRoleTool.service_description(service_object).host = SGB.SYS.host()

        @staticmethod
        def information_list() -> list[ServiceInformation]:
            return DataTool.to_list(SGB.SERVICE.client.service_collection.get())

        @staticmethod
        def kill_all(
            local: bool = True,
            via_standart_tools: bool = True,
            exclude_me: bool = False,
        ) -> None:
            hosts: set[str] = set()
            for server_role in SERVICE_ROLE:
                host: nstr = server_role.host
                if ne(host):
                    hosts.add(host)

            def kill_python(host: str, local: bool, via_standart_tools: bool) -> None:
                if local:
                    SGB.EXECUTOR.kill_python_process(host, via_standart_tools, True)
                else:
                    SGB.ACTION.WORKSTATION.kill_python_process(host, via_standart_tools)

            for host in hosts:
                if host != SGB.SYS.host():
                    kill_python(host, local, via_standart_tools)
            if not exclude_me:
                for host in hosts:
                    if host == SGB.SYS.host():
                        kill_python(host, local, via_standart_tools)

        @staticmethod
        def subscribe_on(
            service_description: ServiceDescriptionBase,
            service_command: SERVICE_COMMAND | str,
            type: int = SUBSCRIBTION_TYPE.ON_RESULT,
            name: nstr = None,
        ) -> bool:
            return SGB.SERVICE.client.service.subscribe_on(
                service_description, service_command, type, name
            )

        @staticmethod
        def subscribe_on_router(
            command: str,
            name: nstr = None,
        ) -> bool:
            return SGB.SERVICE.client.service.subscribe_on(
                SERVICE_ROLE.ROUTER, command, SUBSCRIBTION_TYPE.ON_CALL, name
            )

        @staticmethod
        def unsubscribe(service_command: SERVICE_COMMAND, type: int) -> bool:
            return SGB.SERVICE.client.service.unsubscribe(service_command, type)

        @staticmethod
        def create_developer_service_description(
            port: nint = None,
        ) -> ServiceDescription:
            service_description: ServiceDescription = EnumTool.get(
                SERVICE_ROLE.DEVELOPER
            )
            if n(port) or port == service_description.port:
                return service_description
            return ServiceDescription(
                j(("Developer", port), CONST.SPLITTER),
                host=CONST.HOST.DEVELOPER.NAME,
                port=CONST_RPC.PORT(port),
            )

        @staticmethod
        def create_support_service_or_master_service_description(
            master_service_desctiption: ServiceDescription, host: nstr = None
        ) -> ServiceDescription:
            if SGB.SERVICE.check_on_availabllity(master_service_desctiption):
                if not StringTool.contains(master_service_desctiption.host, host):
                    return DataTool.fill_data_from_source(
                        ServiceDescription(
                            name=j(
                                (
                                    j(
                                        (
                                            SUPPORT_NAME_PREFIX,
                                            master_service_desctiption.name,
                                        )
                                    ),
                                    host,
                                ),
                                CONST.SPLITTER,
                            ),
                            description=j_s(
                                (
                                    "Support service for",
                                    master_service_desctiption.name,
                                    "on",
                                    host,
                                )
                            ),
                            host=host or SGB.SYS.host(),
                            port=SGB.SERVICE.create_port(master_service_desctiption),
                            auto_restart=False,
                            use_standalone=master_service_desctiption.use_standalone,
                        ),
                        master_service_desctiption,
                        skip_not_none=True,
                    )

            return master_service_desctiption

        @staticmethod
        def as_developer(
            service_role: SERVICE_ROLE, port: int = None
        ) -> ServiceDescription:
            developer_service_description: ServiceDescription = (
                SGB.SERVICE.create_developer_service_description(port)
            )
            description: ServiceDescription = ServiceRoleTool.service_description(
                service_role
            )
            description.isolated = True
            description.host = developer_service_description.host
            description.port = developer_service_description.port
            return description

        @staticmethod
        def isolate(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> ServiceDescription:
            description: ServiceDescription = ServiceRoleTool.service_description(
                service_object
            )
            description.host = SGB.SYS.host()
            description.isolated = True
            description.auto_restart = False
            return description

        @staticmethod
        def restart(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            show_output: bool = True,
        ) -> nbool:
            if SGB.SERVICE.check_on_startable(service_object):
                SGB.SERVICE.stop(service_object, False)
                return SGB.SERVICE.start(service_object, False, show_output)
            return None

        @staticmethod
        def start(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            check_if_started: bool = False,
            isgb_install: bool = True,
            sgb_install: bool = True,
            service_package_install: bool = True,
            show_output: bool = True,
        ) -> nbool:
            service_description: ServiceDescription = EnumTool.get(service_object)
            host_is_linux: nbool = None
            host: nstr = service_description.host
            as_standalone: nbool = None
            if n(host_is_linux):
                host_is_linux = SGB.SYS.is_linux(host)
            if SGB.SYS.python_exists(host):

                version: nstr = service_description.version
                sgb_version: nstr = service_description.sgb_version
                parameters: Any = service_description.parameters
                can_use_standalone: bool = (
                    nn(service_description.standalone_name)
                    and service_description.use_standalone
                )
                as_standalone = (
                    can_use_standalone
                    or nn(service_description.standalone_name)
                    and service_description.use_standalone
                )
                if SGB.SYS.is_virtual_environment():
                    isgb_install = False
                    sgb_install = False
                    """
                    if as_standalone:
                        SGB.output.error(
                            js(
                                (
                                    "Sorry, you can not start service",
                                    esc(service_description.name),
                                    "in standalone mode for virtual environment.",
                                    nl(),
                                    "Service will be started in normal mode.",
                                )
                            )
                        )
                    as_standalone = False
                    """
                #
                if sgb_install:
                    sgb_version_list: strlist = SGB.UPDATER.versions(SGB.NAME)
                    sgb_last_version: str = first(sgb_version_list)
                    if nn(sgb_version) and sgb_version not in sgb_version_list:
                        sgb_version = None
                    sgb_version = sgb_version or sgb_last_version
                else:
                    sgb_version = SGB.VERSION.value
                service_description.sgb_version = sgb_version
                host = host or service_description.host
                if isgb_install:
                    SGB.UPDATER.install_package(
                        name=isgb.NAME,
                        version=isgb.VERSION,
                        host=host,
                        show_output=show_output,
                    )
                if sgb_install and nn(sgb_version):
                    SGB.UPDATER.install_package(
                        name=SGB.NAME,
                        version=sgb_version,
                        host=host,
                        show_output=show_output,
                    )
                package_name: str = SGB.PATH.FACADE.DITRIBUTIVE.NAME(
                    service_description.standalone_name
                )
                if as_standalone:
                    if service_package_install:
                        version_list: strlist = SGB.UPDATER.versions(package_name)
                        if nn(version):
                            if version not in version_list:
                                version = first(version_list)
                        SGB.UPDATER.install_package(
                            name=package_name,
                            version=version,
                            host=host,
                            show_output=show_output,
                        )
                else:
                    SGB.UPDATER.uninstall_package(
                        name=package_name,
                        version=None,
                        host=host,
                        show_output=show_output,
                    )
                if host_is_linux:
                    SGB.ACTION.SSH.mount_facade_for_linux_host(host)
                try:
                    SGB.SERVICE.check_on_startable(service_description)
                    if check_if_started:
                        if SGB.SERVICE.check_on_availabllity(service_description):
                            return None
                    command_list: strlist = []
                    file_path: nstr = None
                    if as_standalone:
                        file_path = SGB.PATH.FACADE.DITRIBUTIVE.NAME(
                            service_description.standalone_name
                        )
                    else:
                        service_file: str = PathTool.add_extension(
                            CONST.SERVICE.NAME, FILE.EXTENSION.PYTHON
                        )
                        if e(service_description.service_path):
                            file_path = SGB.PATH.adapt_for_linux(
                                SGB.PATH.join(
                                    PATH_FACADE.VALUE,
                                    j(
                                        (
                                            service_description.name,
                                            FACADE.SERVICE_FOLDER_SUFFIX,
                                        )
                                    ),
                                    service_file,
                                ),
                                host=host,
                                host_is_linux=host_is_linux,
                            )
                        else:
                            file_path = SGB.PATH.join(
                                service_description.service_path, service_file
                            )
                    command_list.append(file_path)
                    command_list.append(j((ARGUMENT_PREFIX, ISOLATED_ARG_NAME)))
                    command_list.append("0")
                    if ne(parameters):
                        if isinstance(parameters, (list, tuple)):
                            for parameter_item in parameters:
                                command_list.append(parameter_item)
                        elif isinstance(parameters, dict):
                            for parameter_item in parameters:
                                command_list.append(
                                    j((ARGUMENT_PREFIX, parameter_item))
                                )
                                command_list.append(parameters[parameter_item])
                        else:
                            command_list.append(parameter_item)
                    if not host_is_linux or n(host_is_linux):
                        command_list = (
                            list(
                                SGB.EXECUTOR.create_command_for_start_service(
                                    service_description,
                                    host=host,
                                    as_standalone=as_standalone,
                                )
                            )
                            + command_list
                        )
                        complete_process: CompletedProcess = SGB.EXECUTOR.execute(
                            tuple(command_list), show_output
                        )
                    if host_is_linux or (
                        n(host_is_linux)
                        and n(SGB.DATA.CHECK.returncode(complete_process))
                    ):
                        return SGB.RESULT.SSH.execute_python_file(
                            j_s(command_list),
                            host,
                            in_background=True,
                            as_standalone=as_standalone,
                        )
                    return True
                except Exception as error:
                    return None
            else:
                raise Exception(j_s(("Python is not exists on host:", host)))

        @staticmethod
        def kill(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            local: bool = True,
            via_standart_tools: bool = True,
        ) -> nbool:
            information: ServiceInformation | None = SGB.SERVICE.get_information(
                service_object
            )
            if e(information):
                return None
            pid: int = information.pid
            host: str = SGB.SERVICE.client.get_host(information)
            if local:
                return SGB.EXECUTOR.kill_process(pid, host, via_standart_tools)
            return SGB.ACTION.WORKSTATION.kill_process(pid, host, via_standart_tools)

        @staticmethod
        def serve(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            call_handler: Callable[[SERVICE_COMMAND, ParameterList], Any] | None = None,
            starts_handler: (
                Callable[[IService], None] | Callable[[], None] | None
            ) = None,
            max_workers: nint = None,
            stop_before: bool = True,
            isolate: bool = False,
            as_standalone: bool = False,
            show_output: bool = True,
        ) -> None:
            service_description: ServiceDescription = EnumTool.get(service_object)
            service_description.sgb_version = (
                service_description.sgb_version or SGB.VERSION.value
            )
            as_standalone = not isolate and (
                as_standalone
                and (
                    nn(service_description.standalone_name)
                    if n(service_description.use_standalone)
                    else service_description.use_standalone
                )
            )
            host: str = SGB.SYS.host()
            service_description = ServiceRoleTool.service_description(service_object)
            if SGB.SERVICE.check_on_host_chanchable(service_description) or isolate:
                if isolate:
                    SGB.SERVICE.isolate(service_description)
                else:
                    if not SGB.DATA.contains(host, service_description.host):
                        SGB.SERVICE.change_host_on_local(service_description)
                    if stop_before:
                        if SGB.SERVICE.check_on_availabllity(service_description):
                            SGB.SERVICE.stop(service_description)

                def internal_starts_handler(service: IService) -> None:
                    if SGB.SYS.is_linux():
                        SGB.ACTION.SSH.mount_facade_for_linux_host(host)
                        SGB.EVENT.send(
                            *SGB.EVENT.BUILDER.service_is_being_started(
                                service_description
                            ),
                            send_on_accessibility=True,
                        )

                    if nn(starts_handler):
                        if starts_handler.__code__.co_argcount == 1:
                            starts_handler(service)
                        else:
                            starts_handler()

                def internal_call_handler(
                    sc: SERVICE_COMMAND, pl: ParameterList, context
                ) -> Any:
                    with SGB.ERROR.detect():
                        if ne(call_handler):
                            sig: Signature = signature(call_handler)
                            arg_count: int = len(sig.parameters) - (
                                "self" in sig.parameters
                            )
                            if arg_count == 3:
                                if DataTool.is_in(sig.parameters, "context"):
                                    return call_handler(
                                        sc,
                                        pl,
                                        context,
                                    )
                                if DataTool.is_in(
                                    sig.parameters, "subscribtion_result"
                                ):
                                    return call_handler(
                                        sc,
                                        pl,
                                        SGB.DATA.EXTRACT.subscribtion_result(pl),
                                    )
                            return call_handler(
                                sc,
                                pl,
                            )
                    return None

                with A.ER.detect_interruption("Выход"):
                    SGB.SERVICE.client.create_service().serve(
                        service_description,
                        internal_call_handler,
                        internal_starts_handler,
                        max_workers,
                        as_standalone,
                        show_output,
                        SGB.SERVICE.check_on_availabllity(SERVICE_ROLE.SERVICE_ADMIN),
                    )
            else:
                SGB.ERROR.service_host_is_unchangeable(service_description.host)

        @staticmethod
        def stop(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
            check_if_started: bool = True,
            direct_call: bool = False,
        ) -> bool:
            description: ServiceDescription | None = (
                ServiceRoleTool.service_description(service_object)
            )
            if not check_if_started or SGB.SERVICE.check_on_availabllity(description):
                if SGB.SERVICE.is_service_as_listener(description) or direct_call:
                    SGB.SERVICE.call(description, SERVICE_COMMAND.stop_service)
                    return True
                service_information: ServiceDescriptionBase | None = (
                    DataTool.fill_data_from_source(
                        ServiceDescriptionBase(),
                        SGB.SERVICE.get_information(description),
                    )
                )
                if n(service_information):
                    return False
                SGB.SERVICE.call(service_information, SERVICE_COMMAND.stop_service)
                return True
            return False

        @staticmethod
        def validate(
            cached: bool = False,
            include_isolated: bool = False,
            service_description_list: list[ServiceDescription] | None = None,
        ) -> tuple[list, list]:
            if not cached:
                SGB.SERVICE.client.get_service_information_list()
            service_information_list: list[ServiceInformation] = (
                SGB.SERVICE.information_list()
            )
            if not include_isolated:
                service_information_list = DataTool.filter(
                    lambda item: not item.isolated, service_information_list
                )
            if ne(service_information_list):
                length: int = len(service_information_list)
                with ErrorableThreadPoolExecutor(max_workers=length) as executor:
                    future_to_bool = {
                        executor.submit(
                            SGB.ERROR.wrap(SGB.SERVICE.check_on_availabllity),
                            service_descroption,
                        ): service_descroption
                        for service_descroption in service_information_list
                    }
                    offline_service_list: list[ServiceInformation] = []
                    for value in futures.as_completed(future_to_bool):
                        if not value.result():
                            service_information: ServiceInformation = future_to_bool[
                                value
                            ]
                            offline_service_list.append(service_information)
                            service_information_list.remove(service_information)
                            SGB.SERVICE.client.service_collection.remove_service(
                                service_information
                            )
                    service_description_list = service_description_list or (
                        DataTool.filter(
                            lambda item: item.visible_for_admin,
                            DataTool.map(
                                lambda item: ServiceRoleTool.service_description(item),
                                SERVICE_ROLE,
                            ),
                        )
                    )
                    for service_description_item in service_description_list:
                        if (
                            service_description_item not in service_information_list
                            and service_description_item not in offline_service_list
                        ):
                            offline_service_list.append(service_description_item)
                    return offline_service_list, service_information_list
            return [], []

        @staticmethod
        def check_on_availabllity(
            service_object: SERVICE_ROLE | ServiceDescriptionBase, cached: bool = False
        ) -> bool:
            return SGB.SERVICE.client.check_on_availability(service_object, cached)

        @staticmethod
        def get_information_or_description(
            service_object: SERVICE_ROLE | ServiceDescriptionBase,
        ) -> ServiceInformation | ServiceDescription:
            return SGB.SERVICE.get_information(
                service_object
            ) or ServiceRoleTool.service_description(service_object)

        @staticmethod
        def description_by_service_command(
            value: SERVICE_COMMAND | str,
        ) -> ServiceDescription | None:
            if e(SGB.SERVICE.command_map):
                for service_role_item in SERVICE_ROLE:
                    description: ServiceDescription = (
                        ServiceRoleTool.service_description(service_role_item)
                    )
                    if nn(description.commands):
                        service_command_item: SERVICE_COMMAND
                        for service_command_item in description.commands:
                            SGB.SERVICE.command_map[service_command_item.name] = (
                                description
                            )
            return (
                SGB.SERVICE.command_map[value.name]
                if (value.name if isinstance(value, SERVICE_COMMAND) else value)
                in SGB.SERVICE.command_map
                else None
            )

    class PATH(PATHS, PathTool):

        DIRECTORY_INFO_SECTION: str = "directory_info"

        @staticmethod
        def current_folder_path(file: str) -> str:
            return pathlib.Path(file).parent.resolve()

        @staticmethod
        def get_file_directory(path: str) -> str:
            return SGB.PATH.path(PathTool.get_file_directory(path))

        @staticmethod
        def join(path: str, *paths) -> str:
            return SGB.PATH.path(os.path.join(path, *paths))

        @staticmethod
        def get_modification_time(path: str) -> float:
            return os.path.getmtime(SGB.PATH.adapt_for_linux(path))

        @staticmethod
        def get_creation_time(path: str) -> float:
            return os.path.getctime(SGB.PATH.adapt_for_linux(path))

        @staticmethod
        def adapt_for_linux(
            path: str, host: nstr = None, host_is_linux: nbool = None
        ) -> str:
            path = SGB.PATH.path(path)
            if host_is_linux or SGB.SYS.is_linux(host):
                alias: str = PATH_FACADE.VALUE
                if path.find(alias) == 0:
                    path = path[len(alias) :]
                    path = PATHS.FACADE.LINUX_MOUNT_POINT_PATH + path
            return path

        @staticmethod
        def file_path_list_by_directory_info(
            directory_path: str, confirmed: nbool = None
        ) -> strlist | None:
            info: DirectoryInfo | None = SGB.PATH.directory_info(directory_path)
            if n(confirmed):
                return SGB.PATH.get_file_list(
                    directory_path,
                    DataTool.if_not_empty(
                        info,
                        lambda info: info.last_created_file_timestamp,
                    ),
                )
            else:
                confirmed_file_path_list: strlist = DataTool.map(
                    lambda item: SGB.PATH.join(directory_path, item[0]),
                    info.confirmed_file_list,
                )
                if confirmed:
                    return confirmed_file_path_list
                non_confirmed_file_path_list: strlist = ListTool.diff(
                    confirmed_file_path_list,
                    DataTool.map(SGB.PATH.path, SGB.PATH.get_file_list(directory_path)),
                )
                non_exist_file_path_list: strlist = DataTool.filter(
                    lambda item: not PathTool.exists(item), non_confirmed_file_path_list
                )
                if ne(non_exist_file_path_list):
                    confirmed_file_list: list[tuple[str, float]] = []
                    for item in info.confirmed_file_list:
                        if (
                            SGB.PATH.join(directory_path, item[0])
                            not in non_exist_file_path_list
                        ):
                            confirmed_file_list.append(item)
                    info.confirmed_file_list = confirmed_file_list
                    SGB.ACTION.DATA_STORAGE.value(
                        info,
                        SGB.PATH._directory_info_name(directory_path),
                        SGB.PATH.DIRECTORY_INFO_SECTION,
                    )
                    non_confirmed_file_path_list = ListTool.diff(
                        non_confirmed_file_path_list, non_exist_file_path_list
                    )
                return non_confirmed_file_path_list

        @staticmethod
        def _directory_info_name(file_path: nstr, directory_path: nstr = None) -> str:
            return j(
                (
                    SGB.PATH.DIRECTORY_INFO_SECTION,
                    (directory_path or SGB.PATH.get_file_directory(file_path)),
                ),
                CONST.NAME_SPLITTER,
            )

        @staticmethod
        def confirm_file(path: str) -> bool:
            path = SGB.PATH.path(path)
            file_info: tuple[str, float] = (
                PathTool.get_file_name(path, True),
                int(SGB.PATH.get_creation_time(path)),
            )
            info: DirectoryInfo = SGB.PATH.directory_info(
                PathTool.get_file_directory(path)
            ) or DirectoryInfo(path, [file_info])

            def filter_file_list(
                function: Callable[[tuple[str, float]], bool],
                file_list: list[tuple[str, float]],
            ) -> list[tuple[str, float]]:
                return DataTool.filter(lambda item: function(item), file_list)

            file_list: list[tuple[str, float]] = filter_file_list(
                lambda item: PathTool.get_file_name(item[0], True) == file_info[0],
                info.confirmed_file_list,
            )
            if e(file_list) or e(
                filter_file_list(lambda item: item[1] == file_info[1], file_list)
            ):
                confirmed_file_list: list[tuple[str, float]] = info.confirmed_file_list
                confirmed_file_list.append(file_info)
                info.confirmed_file_list = confirmed_file_list
                SGB.ACTION.DATA_STORAGE.value(
                    info,
                    SGB.PATH._directory_info_name(path),
                    SGB.PATH.DIRECTORY_INFO_SECTION,
                )
                return True
            return False

        @staticmethod
        def save_timestamp_for_directory_info(path: str) -> None:
            path = SGB.PATH.path(path)
            SGB.ACTION.DATA_STORAGE.value(
                DirectoryInfo(path, int(DateTimeTool.now().timestamp())),
                SGB.PATH._directory_info_name(path),
                SGB.PATH.DIRECTORY_INFO_SECTION,
            )

        @staticmethod
        def directory_info(path: str) -> DirectoryInfo | None:
            return SGB.RESULT.DATA_STORAGE.value(
                SGB.PATH._directory_info_name(None, SGB.PATH.path(path)),
                DirectoryInfo(),
                SGB.PATH.DIRECTORY_INFO_SECTION,
            ).data

        @staticmethod
        def host(value: str) -> str:
            return SGB.DATA.FORMAT.host(value, reverse=True)

        @staticmethod
        def resolve(value: str, host: nstr = None) -> str:
            if value[0] == "{" and value[-1] == "}":
                value = value[1:-1]
            return PathTool.resolve(value, host or SGB.SYS.host())

    class DATA(
        DataTool,
        ListTool,
        EnumTool,
        StringTool,
        DateTimeTool,
        FullNameTool,
        ServiceRoleTool,
    ):
        
        class COMMUNITY:
             
            @staticmethod
            def by_telephone_number(value: int) -> COMMUNITY | None:
                for community in TELEPHONE_POOL:
                    telephone_range_list: tuple[
                        dict[COMMUNITY, tuple[int, int]], ...
                    ] = TELEPHONE_POOL[community]
                    for communit_item in telephone_range_list:
                        telephone_range_item: tuple[int, int] = telephone_range_list[
                            communit_item
                        ]
                        if (
                            value >= telephone_range_item[0]
                            and value <= telephone_range_item[1]
                        ):
                            return community
                return None
                    

        class FILE:

            @staticmethod
            def read_content_by_computer(
                file_path: str, computer: Computer, encoding: str = CHARSETS.UTF8
            ) -> str:
                with open(
                    A.PTH.resolve(file_path, computer.name), "r", encoding=encoding
                ) as file:
                    return file.read()

        class EVENT:

            @staticmethod
            def remove_save_flag(value: Events) -> int:
                return BM.remove(EnumTool.get(value).flags, LogMessageFlags.SAVE)

        class JOURNAL:
            @staticmethod
            def type_by_any(
                value: str | nint, full_equaliment: bool = True
            ) -> list[JournalType] | None:
                result: list[JournalType] = []
                if n(value):
                    return None
                try:
                    value = int(value)
                    data: OrderedNameCaptionDescription | None = first(
                        DataTool.filter(
                            lambda item: item[0] == value, DataTool.to_list(JournalType)
                        )
                    )
                    return None if n(data) else [JournalType(data)]
                except ValueError as _:
                    pass
                value = value.lower()
                for item in JournalType:
                    item_data: OrderedNameCaptionDescription = EnumTool.get(item)
                    item_data_param: ParamItem = item_data[1]
                    a: bool = (
                        item_data_param.name.lower() == value
                        if full_equaliment
                        else StringTool.contains(item_data_param.name, value)
                    )
                    b: bool = StringTool.contains(item_data_param.caption, value)
                    if a or b:
                        result.append(item)
                        if not b and full_equaliment:
                            break
                return None if e(result) else result

            @staticmethod
            def tag_by_id(value: int) -> Tags | None:
                data: IconedOrderedNameCaptionDescription | None = first(
                    DataTool.filter(
                        lambda item: item[0] == value, DataTool.to_list(Tags)
                    )
                )
                return None if n(data) else Tags(data)

        @staticmethod
        def translit(value, language_code=None, reversed=False, strict=False):
            return translit(value, language_code, reversed, strict)

        class VARIABLE:
            SECTION_DELIMITER: str = "__"
            SECTION_DELIMITER_ALT: str = "."

            @staticmethod
            def _get_as_name(value: str | StorageVariableHolder) -> str:
                if isinstance(value, StorageVariableHolder):
                    return value.key_name
                return value

            class TIMESTAMP:
                @staticmethod
                def value(name: str | StorageVariableHolder) -> datetime | None:
                    return DateTimeTool.datetime_from_string(
                        SGB.DATA.VARIABLE.value(
                            SGB.DATA.VARIABLE._get_as_name(name),
                            from_environment_only=False,
                            section=SGB.DATA.VARIABLE.Sections.TIMESTAMP,
                        )
                    )

                @staticmethod
                def find(name: nstr = None) -> list[StorageVariableHolder] | None:
                    return (
                        SGB.DATA.VARIABLE.TIMESTAMP.get(name)
                        if n(name)
                        else SGB.DATA.VARIABLE.find(
                            name, SGB.DATA.VARIABLE.Sections.TIMESTAMP
                        )
                    )

                @staticmethod
                def get(
                    name: nstr = None,
                ) -> StorageVariableHolder | list[StorageVariableHolder] | None:
                    return SGB.DATA.VARIABLE.get(
                        name, SGB.DATA.VARIABLE.Sections.TIMESTAMP
                    )

                @staticmethod
                def set(
                    name: str | StorageVariableHolder,
                    value: datetime | None,
                    description: str,
                ) -> str:
                    return SGB.DATA.VARIABLE.set(
                        SGB.DATA.VARIABLE._get_as_name(name),
                        DateTimeTool.datetime_to_string(value or DateTimeTool.now()),
                        description,
                        SGB.DATA.VARIABLE.Sections.TIMESTAMP,
                    )

                @staticmethod
                def update(
                    name: str | StorageVariableHolder, value: datetime | None = None
                ) -> bool:
                    holder: StorageVariableHolder | None = (
                        SGB.DATA.VARIABLE.TIMESTAMP.get(name)
                    )
                    if nn(holder):
                        SGB.DATA.VARIABLE.TIMESTAMP.set(
                            SGB.DATA.VARIABLE._get_as_name(name),
                            value,
                            holder.description,
                        )
                        return True
                    return False

                @staticmethod
                def remove(name: str) -> None:
                    SGB.DATA.VARIABLE.remove(
                        SGB.DATA.VARIABLE._get_as_name(name),
                        SGB.DATA.VARIABLE.Sections.TIMESTAMP,
                    )
                    item: ExpiredTimestampVariableHolder | None = None
                    for item in SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder():
                        if item.timestamp == name:
                            SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.remove(name)

                class EXPIRED:
                    @staticmethod
                    def remove(name: str) -> None:
                        SGB.DATA.VARIABLE.remove(
                            SGB.DATA.VARIABLE._get_as_name(name),
                            SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED,
                        )

                    @staticmethod
                    def set(
                        name: str,
                        description: str,
                        timestamp_variable_name: str,
                        life_time_variable_name: str,
                        note_name_resolver: str,
                    ) -> None:
                        timestamp_value: datetime | None = (
                            SGB.DATA.VARIABLE.TIMESTAMP.value(timestamp_variable_name)
                        )
                        if nn(timestamp_value):
                            life_time_variable: nint = int(
                                SGB.DATA.VARIABLE.value(life_time_variable_name)
                            )
                            SGB.DATA.VARIABLE.set(
                                name,
                                ExpiredTimestampVariableHolder(
                                    timestamp_variable_name,
                                    life_time_variable_name,
                                    note_name_resolver,
                                ),
                                description,
                                SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED,
                            )

                    @staticmethod
                    def get(
                        name: nstr = None,
                    ) -> StorageVariableHolder | list[StorageVariableHolder] | None:
                        return SGB.DATA.VARIABLE.get(
                            name, SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED
                        )

                    @staticmethod
                    def holder(
                        name: str | StorageVariableHolder | None = None,
                    ) -> (
                        ExpiredTimestampVariableHolder
                        | list[ExpiredTimestampVariableHolder]
                        | None
                    ):
                        result: list[ExpiredTimestampVariableHolder] = (
                            DataTool.fill_data_from_list_source(
                                ExpiredTimestampVariableHolder,
                                DataTool.map(
                                    lambda item: item.default_value,
                                    SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.get(name),
                                ),
                            )
                        )
                        if nn(name):
                            if e(result):
                                return None
                        return result if n(name) else DataTool.get_first_item(result)

                    @staticmethod
                    def value(
                        name_or_holder: (
                            str | ExpiredTimestampVariableHolder | StorageVariableHolder
                        ),
                    ) -> datetime | None:
                        if isinstance(name_or_holder, str):
                            name_or_holder = SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(
                                name_or_holder
                            )
                        if isinstance(name_or_holder, StorageVariableHolder):
                            name_or_holder = DataTool.fill_data_from_source(
                                ExpiredTimestampVariableHolder(),
                                name_or_holder.defaul_value,
                            )
                        life_time: nint = None
                        try:
                            life_time = int(name_or_holder.life_time)
                        except ValueError as _:
                            life_time = int(
                                SGB.DATA.VARIABLE.value(name_or_holder.life_time)
                            )
                        return (
                            None
                            if e(name_or_holder)
                            else DateTimeTool.add_months(
                                SGB.DATA.VARIABLE.TIMESTAMP.value(
                                    name_or_holder.timestamp
                                ),
                                life_time,
                            )
                        )

                    @staticmethod
                    def timestamp(
                        name_or_variable_holder: str | ExpiredTimestampVariableHolder,
                    ) -> datetime | None:
                        variable_holder: ExpiredTimestampVariableHolder | None = (
                            SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(
                                name_or_variable_holder
                            )
                            if isinstance(name_or_variable_holder, str)
                            else name_or_variable_holder
                        )
                        return (
                            None
                            if e(variable_holder)
                            else SGB.DATA.VARIABLE.TIMESTAMP.value(
                                variable_holder.timestamp
                            )
                        )

                    @staticmethod
                    def life_time(
                        name_or_variable_holder: str | ExpiredTimestampVariableHolder,
                    ) -> nint:
                        variable_holder: ExpiredTimestampVariableHolder | None = (
                            SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(
                                name_or_variable_holder
                            )
                            if isinstance(name_or_variable_holder, str)
                            else name_or_variable_holder
                        )
                        return (
                            None
                            if e(variable_holder)
                            else DateTimeTool.day_count(
                                SGB.DATA.VARIABLE.TIMESTAMP.value(
                                    variable_holder.timestamp
                                ),
                                int(SGB.DATA.VARIABLE.value(variable_holder.life_time)),
                            )
                        )

                    @staticmethod
                    def left_life_time(
                        name_or_variable_holder: str | ExpiredTimestampVariableHolder,
                    ) -> nint:
                        variable_holder: ExpiredTimestampVariableHolder | None = (
                            SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(
                                name_or_variable_holder
                            )
                            if isinstance(name_or_variable_holder, str)
                            else name_or_variable_holder
                        )
                        return (
                            None
                            if e(variable_holder)
                            else (
                                SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.value(
                                    variable_holder
                                )
                                - DateTimeTool.now()
                            ).days
                            + 1
                        )

            class ENVIRONMENT:

                raise_exception_if_not_exist: bool = True

                @staticmethod
                def value(name: str, raise_exception_if_not_exist: bool = True) -> Any:
                    result = SGB.DATA.VARIABLE.value(name, True)
                    if (
                        SGB.DATA.VARIABLE.ENVIRONMENT.raise_exception_if_not_exist
                        and raise_exception_if_not_exist
                        and n(result)
                    ):
                        raise NotFound(
                            j_s(("Переменная окружения", esc(name), "не найдена!"))
                        )
                    return result

            class Sections(Enum):
                VARIABLE = "variable"
                TIMESTAMP = "timestamp"
                TIMESTAMP_EXPIRED = "timestamp_expired"

            @staticmethod
            def remove(
                name: str | StorageVariableHolder, section: Sections | None = None
            ) -> None:
                if isinstance(name, StorageVariableHolder):
                    name = name.key_name
                index: int = name.find(SGB.DATA.VARIABLE.SECTION_DELIMITER)
                if index != -1:
                    return SGB.DATA.VARIABLE.remove(
                        name[index + len(SGB.DATA.VARIABLE.SECTION_DELIMITER) :],
                        name[0:index],
                    )
                SGB.ACTION.DATA_STORAGE.value(
                    None,
                    name,
                    section,
                )

            @staticmethod
            def set(
                name: str,
                value: Any,
                description: nstr = None,
                section: Sections | nstr = None,
            ) -> Any:
                section = section or SGB.DATA.VARIABLE.Sections.VARIABLE
                index: int = name.find(SGB.DATA.VARIABLE.SECTION_DELIMITER)
                if index != -1:
                    return SGB.DATA.VARIABLE.set(
                        name[index + len(SGB.DATA.VARIABLE.SECTION_DELIMITER) :],
                        value,
                        description,
                        name[0:index],
                    )
                SGB.ACTION.DATA_STORAGE.value(
                    StorageVariableHolder(name, value, description),
                    name,
                    EnumTool.get(section),
                )
                return value

            @staticmethod
            def get(
                name: nstr = None, section: Sections | nstr = None
            ) -> StorageVariableHolder | list[StorageVariableHolder] | None:
                section = section or SGB.DATA.VARIABLE.Sections.VARIABLE
                section_name: nstr = EnumTool.get(section)
                data: strdict | list[strdict] | None = SGB.RESULT.DATA_STORAGE.value(
                    name,
                    None if n(name) else StorageVariableHolder,
                    section_name,
                ).data

                def convert(
                    value_holder: StorageVariableHolder | None,
                ) -> StorageVariableHolder | None:
                    if e(value_holder):
                        return value_holder
                    if value_holder.section == EnumTool.get(
                        SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED
                    ):
                        value_holder.default_value = DataTool.fill_data_from_source(
                            ExpiredTimestampVariableHolder(), value_holder.default_value
                        )
                    return value_holder

                if n(name):
                    result: list[StorageVariableHolder] = []
                    for item in data:
                        value_holder: StorageVariableHolder = (
                            DataTool.fill_data_from_source(
                                StorageVariableHolder(section=section_name),
                                data[item],
                                skip_not_none=True,
                            )
                        )
                        result.append(convert(value_holder))
                    return result
                if nn(data):
                    data.section = section_name
                return convert(data)

            @staticmethod
            def find(
                name: str | Enum | None = None,
                sections: strlist | str | list[Sections] | Sections | None = None,
            ) -> list[MATERIALIZED_RESOURCES.Types | SETTINGS | StorageVariableHolder]:
                if isinstance(name, Enum):
                    name = name.name
                result: list[StorageVariableHolder] = []
                section_name_list = (
                    None
                    if e(sections)
                    else list(
                        map(
                            lambda item: (
                                EnumTool.get(item)
                                if isinstance(item, SGB.DATA.VARIABLE.Sections)
                                else item
                            ),
                            sections if isinstance(sections, list) else [sections],
                        )
                    )
                ) or list(
                    map(lambda item: EnumTool.get(item), SGB.DATA.VARIABLE.Sections)
                )
                for section_name_item in section_name_list:
                    for item in SGB.DATA.VARIABLE.get(section=section_name_item):
                        item: StorageVariableHolder = item
                        if (
                            e(name)
                            or StringTool.contains(item.key_name, name)
                            or StringTool.contains(item.description, name)
                        ):
                            """if len(section_name_list) > 1:
                            item.key_name = j(
                                (section_name_item, item.key_name), SGB.DATA.VARIABLE.SECTION_DELIMITER_ALT)
                            """
                            item.section = section_name_item
                            result.append(item)
                return (
                    (
                        SGB.DATA.MATERIALIZED_RESOURCES.find(name)
                        + SGB.SETTINGS.find(name)
                    )
                    if e(sections)
                    else []
                ) + result

            @staticmethod
            def link(name: str) -> str:
                return SGB.DATA.FORMAT.variable(SGB.DATA.FORMAT.link(name))

            @staticmethod
            def value(
                variable_name: str,
                from_environment_only: bool = False,
                section: str | Sections | None = None,
            ) -> Any:
                result: Any = SGB.DATA.VARIABLE.value_with_section(
                    variable_name, from_environment_only, section
                )
                return result if from_environment_only else result[0]

            @staticmethod
            def value_with_section(
                variable_name: str,
                from_environment_only: bool = False,
                section: str | Sections | None = None,
            ) -> tuple[Any, Sections]:
                section = EnumTool.get(section)
                variable_name = variable_name.replace(
                    SGB.DATA.VARIABLE.SECTION_DELIMITER_ALT,
                    SGB.DATA.VARIABLE.SECTION_DELIMITER,
                )
                index: int = variable_name.find(SGB.DATA.VARIABLE.SECTION_DELIMITER)
                if index != -1:
                    return SGB.DATA.VARIABLE.value_with_section(
                        variable_name[
                            index + len(SGB.DATA.VARIABLE.SECTION_DELIMITER) :
                        ],
                        from_environment_only,
                        variable_name[0:index],
                    )
                environment_variable_handler: Callable[[str], Any] = (
                    SGB.SYS.environment_variable
                )
                if from_environment_only:
                    return environment_variable_handler(variable_name)

                def get_value(
                    variable_name: str, section: SGB.DATA.VARIABLE.Sections | str
                ) -> Any:
                    if section == SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED:
                        return SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(variable_name)
                    return DataTool.if_not_empty(
                        SGB.DATA.VARIABLE.get(variable_name, section),
                        lambda item: item.default_value,
                    )

                def is_in_section(
                    value: nstr, section: SGB.DATA.VARIABLE.Sections
                ) -> bool:
                    return value == EnumTool.get(section) or e(value)

                for value in (
                    environment_variable_handler(variable_name),
                    (
                        get_value(variable_name, SGB.DATA.VARIABLE.Sections.VARIABLE)
                        if is_in_section(section, SGB.DATA.VARIABLE.Sections.VARIABLE)
                        else None
                    ),
                    (
                        get_value(variable_name, SGB.DATA.VARIABLE.Sections.TIMESTAMP)
                        if is_in_section(section, SGB.DATA.VARIABLE.Sections.TIMESTAMP)
                        else None
                    ),
                    (
                        get_value(
                            variable_name, SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED
                        )
                        if is_in_section(
                            section, SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED
                        )
                        else None
                    ),
                    SGB.DATA.MATERIALIZED_RESOURCES.get_quantity(variable_name),
                    SGB.SETTINGS.get(variable_name),
                ):
                    if nn(value):
                        break
                if section not in DataTool.to_list(SGB.DATA.VARIABLE.Sections):
                    value = get_value(variable_name, section)
                return (
                    value,
                    EnumTool.get_by_value(SGB.DATA.VARIABLE.Sections, section),
                )

        @staticmethod
        def save_base64_as_image(path: str, content: str) -> bool:
            with open(path, "wb") as file:
                file.write(base64.decodebytes(bytes(content, CHARSETS.UTF8)))
                return True
            return False

        @staticmethod
        def uuid() -> str:
            return str(uuid.uuid4().hex)

        class USER:

            @staticmethod
            def community(value: User) -> COMMUNITY:
                distinguishedName: str = value.distinguishedName.lower()
                for item in COMMUNITY_USER_CONTAINER_NAME:
                    if (
                        COMMUNITY_USER_CONTAINER_NAME[item] or item.name
                    ).lower() in distinguishedName:
                        return item

            @staticmethod
            def admin_list_by_user_name(value: str) -> list[User] | None:
                result: list[User] = ResultTool.filter(
                    lambda user_item: StringTool.contains(user_item.description, value),
                    SGB.RESULT.USER.admins(),
                )
                return result if ne(result) else None

            @staticmethod
            def session_id_by_host(value: str) -> int:
                return SGB.EXECUTOR.get_user_session_id_for_host(value)

            @staticmethod
            def by_login(
                value: str, active: nbool = None, cached: nbool = None
            ) -> User:
                return SGB.RESULT.USER.by_login(value, active, cached).data

            @staticmethod
            def login_by_workstation(name_or_ip: str) -> nstr:
                return SGB.EXECUTOR.get_logged_user(name_or_ip)

            @staticmethod
            def by_name(value: str) -> list[User]:
                return SGB.RESULT.USER.by_name(value).data

        class SETTINGS:
            @staticmethod
            def get(value: SETTINGS) -> Any:
                return SGB.RESULT.SETTINGS.get(value).data

        class FILTER:

            @staticmethod
            def by_string(
                string: str,
                value: list[Any] | Any,
                data_item_to_string_function: Callable[[Any], str] | None = None,
                filter_function: Callable[[Any, str], bool] | None = None,
            ) -> list[Any]:
                string = lw(string)
                return DataTool.filter(
                    lambda item: (
                        (
                            lw(
                                item
                                if n(data_item_to_string_function)
                                else data_item_to_string_function(item)
                            ).find(string)
                        )
                        != -1
                        if n(filter_function)
                        else filter_function(item, string)
                    ),
                    value,
                )

            @staticmethod
            def symbols_only_in(value: str, check_value: str) -> str:
                return "".join(c for c in value if c in check_value)

            @staticmethod
            def users_by_dn(value: list[User], dn: str) -> list:
                return DataTool.filter(
                    lambda item: item.distinguishedName.find(dn) != -1, value
                )

            @staticmethod
            def users_by_activity(value: list[User], active: bool) -> list[User]:
                return SGB.DATA.FILTER.users_by_dn(
                    value,
                    (
                        AD.ALL_ACTIVE_USERS_CONTAINER_DN
                        if active
                        else AD.INACTIVE_USERS_CONTAINER_DN
                    ),
                )

            @staticmethod
            def computers_with_property(
                list: list[Computer], value: AD.ComputerProperties
            ) -> list[Computer]:
                def filter_function(computer: Computer) -> bool:
                    return BM.has(computer.properties, EnumTool.get(value))

                return DataTool.filter(filter_function, list)

        class EXTRACT:

            @staticmethod
            def service_information(
                value: dict | ServiceInformation,
            ) -> ServiceInformation:
                return ServiceTool.extract_service_information(value)

            @staticmethod
            def returncode(
                value: CompletedProcess | None, check_on_success: bool = False
            ) -> int | nbool:
                if n(value):
                    return False if check_on_success else None
                returncode: int = value.returncode
                return (
                    True
                    if returncode == 0
                    else (
                        None
                        if returncode in [2, 2250, 2120, 112]
                        else False if check_on_success else returncode
                    )
                )

            @staticmethod
            def command_type(value: str | File) -> CommandTypes | None:
                if isinstance(value, File):
                    return SGB.DATA.EXTRACT.command_type(value.title)
                value = value.split(CONST.SPLITTER)[0]
                for item in CommandTypes:
                    if value.lower() in DataTool.map(
                        lambda item: item.lower(), EnumTool.get(item)[1:]
                    ):
                        return item
                return None

            @staticmethod
            def new_mail_message(value: dict) -> NewMailMessage:
                return DataTool.fill_data_from_source(NewMailMessage(), value)

            @staticmethod
            def mailbox_info(value: dict | None) -> MailboxInfo | None:
                if n(value):
                    return None
                result: MailboxInfo = DataTool.fill_data_from_source(
                    MailboxInfo(), value
                )
                result.timestamp = DateTimeTool.datetime_from_string(result.timestamp)
                return result

            @staticmethod
            def polibase_person(value: dict | None) -> PolibasePerson | None:
                if n(value):
                    return None
                polibase_person: PolibasePerson = DataTool.fill_data_from_source(
                    PolibasePerson(), value
                )
                polibase_person.Birth = DateTimeTool.datetime_from_string(
                    polibase_person.Birth
                )
                polibase_person.registrationDate = DateTimeTool.datetime_from_string(
                    polibase_person.registrationDate
                )
                return polibase_person

            @staticmethod
            def datetime(value: nstr, format: str) -> datetime | None:
                if e(value):
                    return None
                result: datetime | None = None
                try:
                    result = DateTimeTool.datetime_from_string(value, format)
                except ValueError as error:
                    date_extract_pattern: str = "[0-9]{1,2}\\.[0-9]{1,2}\\.[0-9]{4}"
                    date_list: strlist = re.findall(date_extract_pattern, value)
                    if ne(date_list):
                        result = SGB.DATA.EXTRACT.datetime(date_list[0], format)
                return result

            @staticmethod
            def date(value: nstr, format: str) -> date | None:
                datetime_value: datetime | None = SGB.DATA.EXTRACT.datetime(
                    value, format
                )
                if nn(datetime_value):
                    return datetime_value.date()
                return None

            @staticmethod
            def boolean(value: int | nstr) -> nbool:
                if e(value):
                    return False
                if isinstance(value, str):
                    value = value.lower()
                    if value in ["1", "yes", "да"]:
                        return True
                    if value in ["0", "no", "нет"]:
                        return True
                if isinstance(value, int):
                    if value == 1:
                        return True
                    if value == 0:
                        return False
                return None

            @staticmethod
            def wappi_telephone_number(value: str | dict) -> nstr:
                if isinstance(value, str):
                    return SGB.DATA.FORMAT.telephone_number(
                        value.split(CONST.MESSAGE.WHATSAPP.WAPPI.CONTACT_SUFFIX)[0]
                    )
                if isinstance(value, dict):
                    return SGB.DATA.FORMAT.telephone_number(value["user"])
                return None

            class EVENT:
                @staticmethod
                def parameter(event_ds: EventDS | None, param_item: ParamItem) -> Any:
                    if n(event_ds):
                        return None
                    event: Events = EnumTool.get(Events, event_ds.name)
                    event_description: EventDescription = EnumTool.get(event)
                    param_index: int = event_description.params.index(param_item)
                    if param_index == -1 or param_index >= len(event_ds.parameters):
                        return None
                    for index, name in enumerate(event_ds.parameters):
                        if index == param_index:
                            return event_ds.parameters[name]

                @staticmethod
                def value(
                    value: EventDS | None,
                    name_holder: str | ParamItem | nint = None,
                ) -> Any:
                    if n(value):
                        return None
                    if isinstance(name_holder, int):
                        return DataTool.by_index(
                            DataTool.to_list(value.parameters), name_holder
                        )
                    return (
                        value.parameters
                        if n(name_holder)
                        else DataTool.if_is_in(
                            value.parameters,
                            (
                                name_holder
                                if isinstance(name_holder, str)
                                else name_holder.name
                            ),
                        )
                    )

                @staticmethod
                def whatsapp_message(
                    value: ParameterList,
                ) -> WhatsAppMessage | None:
                    allow: nbool = SGB.DATA.EXTRACT.subscribtion_result(value).result
                    message: WhatsAppMessage | None = None
                    if allow:
                        event, parameters = SGB.DATA.EXTRACT.EVENT.with_parameters(
                            value
                        )
                        if event == Events.WHATSAPP_MESSAGE_RECEIVED:
                            message = DataTool.fill_data_from_source(
                                WhatsAppMessage(), parameters[0]
                            )
                            if ne(message.message):
                                message.message = unquote(message.message)
                    return message

                @staticmethod
                def action(value: strdict) -> ActionWasDone:
                    action: ActionWasDone = DataTool.fill_data_from_source(
                        ActionWasDone(),
                        SGB.EVENT.get_parameter(Events.ACTION_WAS_DONE, value),
                        copy_by_index=True,
                    )
                    action.action = EnumTool.get(Actions, action.action)
                    return action

                @staticmethod
                def get(value: ParameterList) -> Events:
                    event_content: Any | list[Any] = (
                        value.values[0]
                        if ServiceTool.has_subscribtion_result(value)
                        else value.values
                    )
                    return EnumTool.get(Events, event_content[0])

                @staticmethod
                def with_parameters(
                    value: ParameterList,
                ) -> tuple[Events, list[Any]]:
                    event_data: Any | list[Any] = (
                        value.values[0]
                        if ServiceTool.has_subscribtion_result(value)
                        else value.values
                    )
                    event: Events = EnumTool.get(Events, event_data[0])
                    parameters: strdict = event_data[1]
                    result_parameters: list[Any] = []
                    if ne(event.value.params):
                        for event_parameters_description in event.value.params:
                            event_parameters_description: ParamItem = (
                                event_parameters_description
                            )
                            if event_parameters_description.optional:
                                if DataTool.is_in(
                                    parameters, event_parameters_description.name
                                ):
                                    result_parameters.append(
                                        parameters[event_parameters_description.name]
                                    )
                                else:
                                    result_parameters.append(None)
                            else:
                                result_parameters.append(
                                    parameters[event_parameters_description.name]
                                )
                    return event, result_parameters

                @staticmethod
                def parameters(
                    value: ParameterList,
                ) -> list[Any]:
                    return SGB.DATA.EXTRACT.EVENT.with_parameters(value)[1]

            @staticmethod
            def subscribtion_result(
                pl: ParameterList,
            ) -> SubscribtionResult | None:
                def extract() -> SubscriberInformation:
                    result: SubscribtionResult = DataTool.fill_data_from_source(
                        SubscribtionResult(), pl.values[-1]
                    )
                    if isinstance(result.result, str):
                        try:
                            result.result = DataTool.rpc_decode(result.result)
                        except Exception as _:
                            pass
                    return result

                return (
                    None
                    if e(pl.values) or not ServiceTool.has_subscribtion_result(pl)
                    else extract()
                )

            @staticmethod
            def email(value: nstr) -> nstr:
                if n(value):
                    return None
                email_list: strlist = re.findall(
                    r"[A-Za-z0-9_%+-.]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,5}", value
                )
                if len(email_list) > 0:
                    return email_list[0]
                return None

            @staticmethod
            def float(value: str) -> float | None:
                if ne(value):
                    floats: strlist = re.findall(r"\d+[\.\,]*\d*", value)
                    if len(floats) > 0:
                        return float(floats[0].replace(",", "."))
                return None

            @staticmethod
            def decimal(
                value: str | int,
                min: nint = None,
                max: nint = None,
                simple: bool = False,
            ) -> nint:
                if isinstance(value, int):
                    return value
                value = value.strip()
                result: nint = None
                if simple:
                    try:
                        result = int(value)
                    except ValueError as _:
                        return None
                else:
                    numbers: strlist = re.findall(r"\d+", value)
                    if ne(numbers):
                        result = int(numbers[0])
                    if n(result):
                        return None
                if nn(min) and nn(max) and (result < min or result > max):
                    result = None
                return result

            @staticmethod
            def variables(value: nstr) -> strlist | None:
                if n(value):
                    return None
                fields: strlist | None = [
                    name for _, name, _, _ in Formatter().parse(value) if name
                ]
                if e(fields):
                    return None
                return fields

            @staticmethod
            def parameter(object: dict, name: str) -> str:
                return object[name] if name in object else ""

            @staticmethod
            def telephone(user_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    user_object, FIELD_NAME_COLLECTION.TELEPHONE_NUMBER
                )

            @staticmethod
            def login(user_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    user_object, FIELD_NAME_COLLECTION.LOGIN
                )

            @staticmethod
            def name(mark_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    mark_object, FIELD_NAME_COLLECTION.NAME
                )

            @staticmethod
            def dn(user_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(user_object, FIELD_NAME_COLLECTION.DN)

            @staticmethod
            def group_name(mark_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    mark_object, FIELD_NAME_COLLECTION.GROUP_NAME
                )

            @staticmethod
            def group_id(mark_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    mark_object, FIELD_NAME_COLLECTION.GROUP_ID
                )

            @staticmethod
            def as_full_name(mark_object: dict) -> FullName:
                return FullNameTool.fullname_from_string(
                    SGB.DATA.EXTRACT.full_name(mark_object)
                )

            @staticmethod
            def full_name(mark_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    mark_object, FIELD_NAME_COLLECTION.FULL_NAME
                )

            @staticmethod
            def person_id(mark_object: dict) -> str:
                return SGB.DATA.EXTRACT.parameter(
                    mark_object, FIELD_NAME_COLLECTION.PERSON_ID
                )

            @staticmethod
            def description(object: dict) -> str:
                result = SGB.DATA.EXTRACT.parameter(
                    object, FIELD_NAME_COLLECTION.DESCRIPTION
                )
                if isinstance(result, tuple) or isinstance(result, list):
                    return result[0]

            @staticmethod
            def container_dn(user_object: dict) -> str:
                return SGB.DATA.EXTRACT.container_dn_from_dn(
                    SGB.DATA.EXTRACT.dn(user_object)
                )

            @staticmethod
            def container_dn_from_dn(dn: str) -> str:
                return j(dn.split(",")[1:], ",")

        class CONVERT:
            @staticmethod
            def settings_to_datetime(
                item: SETTINGS, format: str = CONST.SECONDLESS_TIME_FORMAT
            ) -> datetime | list[datetime]:
                settings_value: str | strlist | None = SGB.SETTINGS.get(item)
                return (
                    SGB.DATA.CONVERT.settings_to_datetime_list(item, format)
                    if isinstance(settings_value, list)
                    else DateTimeTool.datetime_from_string(settings_value, format)
                )

            @staticmethod
            def settings_to_datetime_list(
                item: SETTINGS, format: str = CONST.SECONDLESS_TIME_FORMAT
            ) -> list[datetime]:
                return list(
                    map(
                        lambda item: DateTimeTool.datetime_from_string(item, format),
                        SGB.SETTINGS.get(item),
                    )
                )

            @staticmethod
            def file_to_base64(path: str) -> nstr:
                path = SGB.PATH.adapt_for_linux(path)
                while True:
                    try:
                        with open(path, "rb") as file:
                            return SGB.DATA.CONVERT.bytes_to_base64(file.read())
                    except Exception:
                        pass
                return None

            @staticmethod
            def bytes_to_base64(value: bytes) -> str:
                return SGB.DATA.CONVERT.bytes_to_string(
                    SGB.DATA.CONVERT.to_base64(value)
                )

            @staticmethod
            def to_base64(value: Any) -> str:
                return base64.b64encode(value)

            @staticmethod
            def bytes_to_string(value: bytes) -> str:
                return value.decode(CHARSETS.UTF8)

        class STATISTICS:
            NAME: str = "statistics"

            @staticmethod
            def by_name(value: str) -> TimeSeriesStatistics | None:
                def is_equal(value: MATERIALIZED_RESOURCES.Types, name: str) -> bool:
                    return EnumTool.get(value).key_name == name or value.name == name

                if is_equal(MATERIALIZED_RESOURCES.Types.CHILLER_FILTER, value):
                    return SGB.DATA.STATISTICS.for_chiller_filter()
                return None

            @staticmethod
            def for_chiller_filter() -> TimeSeriesStatistics | None:
                events_result: Result[list[EventDS]] = SGB.RESULT.EVENTS.get(
                    *SGB.EVENT.BUILDER.action_was_done(Actions.CHILLER_FILTER_CHANGING)
                )
                if e(events_result):
                    return None
                datetime_list: list[datetime] = ResultTool.map(
                    lambda event: event.timestamp, events_result
                ).data
                distance: list[timedelta] = []
                for index, _ in enumerate(datetime_list):
                    if index == len(datetime_list) - 1:
                        break
                    value: timedelta = datetime_list[index + 1] - datetime_list[index]
                    distance.append(int(value.total_seconds()))
                return TimeSeriesStatistics(
                    len(events_result),
                    datetime_list,
                    distance,
                    min(distance),
                    max(distance),
                    int(sum(distance) / len(distance)),
                )

        class CHECK(CheckTool):

            @staticmethod
            def zabbix_metrics_has_name(value: ZabbixMetrics, name: str) -> bool:
                name = lw(name)
                return (
                    lw(value.name).find(name) != -1
                    or lw(value.key_).find(name) != -1
                    or lw(value.description).find(name) != -1
                )

            @staticmethod
            def returncode(value: CompletedProcess) -> bool:
                return SGB.DATA.EXTRACT.returncode(value, check_on_success=True)

            @staticmethod
            def complete_process_wrong_descriptor(value: CompletedProcess) -> bool:
                return value.returncode == 2250

            @staticmethod
            def now(cron_string: str, value: datetime | None = None) -> bool:
                return SGB.DATA.is_now(cron_string, value)

            class VARIABLE:
                class TIMESTAMP:
                    class EXPIRED:
                        @staticmethod
                        def exists(name: str) -> bool:
                            return ne(SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(name))

                        @staticmethod
                        def exists_by_timestamp(name: str) -> bool:
                            return ne(
                                DataTool.filter(
                                    lambda item: item.timestamp == name,
                                    SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.holder(),
                                )
                            )

            @staticmethod
            def by_secondless_time(value_datetime: datetime, value_str: nstr) -> bool:
                return (
                    False
                    if e(value_str)
                    else DateTimeTool.is_equal_by_time(
                        value_datetime,
                        DateTimeTool.datetime_from_string(
                            value_str, CONST.SECONDLESS_TIME_FORMAT
                        ),
                    )
                )

            class INDICATIONS:
                @staticmethod
                def chiller_value_actual(
                    value_container: ChillerIndicationsValueContainer,
                ) -> bool:
                    return (
                        DateTimeTool.now()
                        - DateTimeTool.datetime_from_string(
                            value_container.timestamp, CONST.ISO_DATETIME_FORMAT
                        )
                    ).total_seconds() // 60 <= INDICATIONS.CHILLER.ACTUAL_VALUES_TIME_DELTA_IN_MINUTES

                @staticmethod
                def chiller_value_valid(value: ChillerIndicationsValue) -> bool:
                    return ne(value.temperature)

        class FORMAT(FormatTool):
            """
            class IOTDevices:

                @staticmethod
                def status_value(device_id: str, code: str) -> nstr:
                    value: Any = SGB.DATA.IOTDevices.status_value(device_id, code)
                    if n(value):
                        return None
                    status_properties: list[IOTDeviceStatusProperty] | None = (
                        SGB.RESULT.IOTDevices.status_properties(device_id).data
                    )
                    if n(status_properties):
                        return None
                    for status_property_item in status_properties:
                        if status_property_item.code == code:
                            return js((value, status_property_item.unit))
                    return None
            """

            @staticmethod
            def domain(value: str) -> str:
                return FormatTool.domain(A.SYS.domain(), value)

            @staticmethod
            def console_message(text: str) -> str:
                return (
                    text.replace(BOLD_BEGIN, Style.BRIGHT)
                    .replace(BOLD_END, Style.RESET_ALL)
                    .replace(ITALICS_BEGIN, "")
                    .replace(ITALICS_END, "")
                )

            @staticmethod
            def as_plain_message(text: str) -> str:
                return (
                    text.replace(BOLD_BEGIN, "")
                    .replace(BOLD_END, "")
                    .replace(ITALICS_BEGIN, "")
                    .replace(ITALICS_END, "")
                )

            @staticmethod
            def whatsapp_message(value: nstr) -> nstr:
                if n(value):
                    return value
                b: str = MESSAGE.WHATSAPP.STYLE.BOLD
                i: str = MESSAGE.WHATSAPP.STYLE.ITALIC
                return (
                    value.replace(BOLD_BEGIN, b)
                    .replace(BOLD_END, b)
                    .replace(ITALICS_BEGIN, i)
                    .replace(ITALICS_END, i)
                )

            @staticmethod
            def bold(value: str) -> str:
                return b(value)

            @staticmethod
            def italics(value: Any) -> str:
                return StringTool.italics(value)

            @staticmethod
            def wappi_status(
                value: WappiStatus | CONST.MESSAGE.WHATSAPP.WAPPI.Profiles,
            ) -> str:
                profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | None = None
                if isinstance(value, CONST.MESSAGE.WHATSAPP.WAPPI.Profiles):
                    profile = value
                    value = SGB.MESSAGE.WHATSAPP.WAPPI.get_status(value)
                title: str = j(
                    (
                        "Статус ",
                        CONST.MESSAGE.WHATSAPP.WAPPI.NAME,
                        ": ",
                        b(value.name or ("" if n(profile) else profile.name)),
                        nl(),
                    )
                )
                if value.authorized:
                    payment_expired_at: datetime = DateTimeTool.datetime_from_string(
                        value.payment_expired_at,
                        CONST.MESSAGE.WHATSAPP.WAPPI.DATETIME_FORMAT,
                    )
                    day_last_for_payment_expiration: int = (
                        payment_expired_at - DateTimeTool.now()
                    ).days
                    return j(
                        (
                            title,
                            " ",
                            CONST.VISUAL.GOOD,
                            " ",
                            "Сервис авторизован",
                            nl(),
                            "  ",
                            CONST.VISUAL.BULLET,
                            " ",
                            "Оплачено до: ",
                            SGB.DATA.FORMAT.date(payment_expired_at),
                            nl(),
                            "  ",
                            CONST.VISUAL.BULLET,
                            " ",
                            "Следующий платеж через: ",
                            day_last_for_payment_expiration,
                            " дней",
                        )
                    )
                else:
                    return j(
                        (title, " ", CONST.VISUAL.WARNING, " Сервис не авторизован")
                    )

            @staticmethod
            def to_mysql(value: str) -> str:
                return json.dumps(value, ensure_ascii=False)[1:-1].replace("'", "<%>")

            @staticmethod
            def from_mysql(value: str) -> str:
                return value.replace("<%>", "'")

            @staticmethod
            def full_name(value: str) -> str:
                return j_s(
                    (
                        DataTool.map(
                            StringTool.capitalize,
                            ListTool.not_empty_items(
                                DataTool.map(
                                    lambda item: str(item).strip(),
                                    value.split(FullNameTool.SPLIT_SYMBOL),
                                )
                            ),
                        )
                    )
                )

            """
            class BACKUP:
                SPLITTER: str = "::"

                @staticmethod
                def job_full_name(name: str, source: str, destination: str) -> str:
                    return j(
                        (source, destination, name), SGB.DATA.FORMAT.BACKUP.SPLITTER
                    )

                @staticmethod
                def job_status_name(name: str, source: str, destination: str) -> str:
                    return j(
                        (
                            "robocopy_job_status",
                            SGB.DATA.FORMAT.BACKUP.job_full_name(
                                name, source, destination
                            ),
                        ),
                        SGB.DATA.FORMAT.BACKUP.SPLITTER,
                    )
            """

            @staticmethod
            def link(name: str) -> str:

                return (
                    name
                    if name.startswith("{") and name.endswith("}")
                    else j(("{", name, "}"))
                )

            @staticmethod
            def variable(value: nstr, from_environment: bool = False) -> nstr:
                if n(value):
                    return value
                variable_name_list: strlist | None = SGB.DATA.EXTRACT.variables(value)
                if e(variable_name_list):
                    return None
                variable_name: str = variable_name_list[0]
                return (
                    SGB.DATA.VARIABLE.ENVIRONMENT.value(variable_name)
                    if from_environment
                    else SGB.DATA.VARIABLE.value(variable_name)
                )

            @staticmethod
            def variable_name(value: str) -> str:
                value = value.lower()
                return re.sub("[\\\\.\\-@:]", CONST.NAME_SPLITTER, value)

            @staticmethod
            def statistics(value: MATERIALIZED_RESOURCES.Types) -> nstr:
                statistics: TimeSeriesStatistics | None = SGB.DATA.STATISTICS.by_name(
                    value.name
                )
                if n(statistics):
                    return None
                count: int = SGB.DATA.MATERIALIZED_RESOURCES.get_quantity(value)

                def to_days(value: int) -> int:
                    return int(DateTimeTool.seconds_to_days(value))

                return j(
                    (
                        "Остаток по времени (дней):",
                        f" {CONST.VISUAL.BULLET} Максимально: {count * to_days(statistics.max)}",
                        f" {CONST.VISUAL.BULLET} Минимально: {count * to_days(statistics.min)}",
                        f" {CONST.VISUAL.BULLET} В среднем: {count * to_days(statistics.avg)}",
                    ),
                    nl(),
                )

            @staticmethod
            def yes_no(value: nbool, symbolic: bool = False) -> str:
                c: Callable[
                    [bool, Callable[[], Any] | Any, Callable[[], Any] | Any, None],
                    Any,
                ] = DataTool.check
                return c(
                    value,
                    c(symbolic, CONST.VISUAL.YES, "Да"),
                    c(symbolic, CONST.VISUAL.NO, "Нет"),
                )

            @staticmethod
            def size(
                value: int | float, round_value: int = 0, use_megabites: bool = False
            ) -> str:
                value = value / 1024 / 1024 / (1 if use_megabites else 1024)
                return j_s(
                    (
                        str(
                            int(value)
                            if round_value == 0
                            else round(value, round_value)
                        ),
                        "Мб" if use_megabites else "Гб",
                    )
                )

            @staticmethod
            def format(
                value: str,
                parameters: strdict | None = None,
                use_python: bool = False,
            ) -> str:
                result_parameters: strdict = globals()
                # result_parameters["print"] = print
                if nn(parameters):
                    for lkey, lvalue in parameters.items():
                        result_parameters[lkey] = lvalue
                io: StringIO = StringIO()
                part: str
                for part in re.findall(
                    r"(\{['\"\,.*?\w\n\[\]\(\)\/:=+\-\!\\ а-яА-Я#]*\})", value
                ):
                    try:
                        if use_python or ne(re.findall(r"print\(.*?\)", part)):
                            io.truncate(0)
                            io.seek(0)
                            with redirect_stdout(io):
                                exec(part[1:-1], globals(), result_parameters)
                            value = value.replace(part, io.getvalue().strip())
                            continue
                    except Exception as exception:
                        SGB.ERROR.global_except_hook(exception)
                    if part.find(SGB.DATA.VARIABLE.SECTION_DELIMITER_ALT) != -1:
                        value = value.replace(
                            part,
                            part.replace(
                                SGB.DATA.VARIABLE.SECTION_DELIMITER_ALT,
                                SGB.DATA.VARIABLE.SECTION_DELIMITER,
                            ),
                        )
                field_list: strlist = [
                    name for _, name, _, _ in Formatter().parse(value) if name
                ]
                formatter: dict[str, str] = {}
                for field_item in field_list:
                    formatter[field_item] = SGB.DATA.FORMAT.by_formatter_name(
                        field_item, None
                    )
                if e(formatter):
                    return value
                return value.format(**formatter)

            @staticmethod
            def index(value: int) -> str:
                return str(value + 1) if value > 0 else ""

            @staticmethod
            def user_principal_name(login: str) -> str:
                return j((login, SGB.SYS.domain()), CONST.DOMAIN_SPLITTER)

            @staticmethod
            def as_string(
                value: Any,
                escaped_string: bool = False,
                mapper: Callable[[Any], str] | None = None,
            ) -> nstr:
                result: nstr = None
                if isinstance(value, Enum):
                    result = value.name
                else:
                    result = str(value)
                if escaped_string:
                    if isinstance(value, (str, datetime, Enum)):
                        result = escs(result)
                    if isinstance(value, dict):
                        result = escs(DataTool.rpc_encode(value, False))
                return DataTool.check_not_none(mapper, lambda: mapper(result), result)

            @staticmethod
            def host(
                value: nstr,
                reverse: bool = False,
                use_default_domain: bool = True,
            ) -> nstr:
                if n(value):
                    return None
                value = value.lower()
                host_start: str = r"\\"
                if reverse:
                    return ListTool.not_empty_items(
                        j(
                            j(value.replace("\\", CONST.SPLITTER)).replace(
                                "/", CONST.SPLITTER
                            )
                        ).split(CONST.SPLITTER)
                    )[0]
                if use_default_domain and not value.endswith(SGB.SYS.domain()):
                    value = j_p((value, SGB.SYS.domain()))
                return ("" if value.startswith(host_start) else host_start) + value

            @staticmethod
            def host_name(value: str) -> str:
                return value.split(".")[0]

            @staticmethod
            def get_chiller_indications_value_image_name(
                datetime: datetime | str,
            ) -> str:
                if isinstance(datetime, str):
                    datetime = SGB.DATA.datetime_from_string(
                        datetime, CONST.ISO_DATETIME_FORMAT
                    )
                return SGB.PATH.replace_prohibited_symbols_from_path_with_symbol(
                    SGB.DATA.datetime_to_string(
                        datetime, CONST.DATETIME_SECOND_ZEROS_FORMAT
                    )
                )

            @staticmethod
            def by_formatter_name(value: Enum | str, data: Any) -> nstr:
                if isinstance(value, str):
                    value = EnumTool.get_by_value(DATA.FORMATTER, value) or value
                if isinstance(value, str):
                    name: str = j((SGB.DATA.STATISTICS.NAME, CONST.NAME_SPLITTER))
                    index: int = value.lower().find(name)
                    if index != -1:
                        index += len(name)
                        value: MATERIALIZED_RESOURCES.Types | None = (
                            EnumTool.get_by_value_or_key(
                                MATERIALIZED_RESOURCES.Types, value[index:].upper()
                            )
                        )
                        if n(value):
                            return None
                        return SGB.DATA.FORMAT.statistics(value)
                if isinstance(value, str):
                    result: Any = None
                    section: SGB.DATA.VARIABLE.Sections | None = None
                    """
                    result, section = SGB.DATA.VARIABLE.value_with_section(value)
                    if section == SGB.DATA.VARIABLE.Sections.TIMESTAMP_EXPIRED:
                        result: ExpiredTimestampVariableHolder = result
                        return j_s(
                            (
                                SGB.DATA.FORMAT.datetime(
                                    SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.value(result),
                                    CONST.DATE_FORMAT,
                                ),
                                "(ещё",
                                SGB.DATA.VARIABLE.TIMESTAMP.EXPIRED.left_life_time(
                                    result
                                ),
                                "дней)",
                            )
                        )
                    if section == SGB.DATA.VARIABLE.Sections.TIMESTAMP:
                        return SGB.DATA.FORMAT.datetime(result, CONST.DATE_FORMAT)'
                    """
                    return result
                if value == DATA.FORMATTER.MY_DATETIME:
                    return SGB.DATA.FORMAT.datetime(data)
                if value == DATA.FORMATTER.MY_DATE:
                    return SGB.DATA.FORMAT.date(data)
                return None

            @staticmethod
            def mobile_helper_command(value: str) -> str:
                return value.lower()

            @staticmethod
            def mobile_helper_qr_code_text(value: str) -> str:
                return SGB.DATA.FORMAT.whatsapp_send_message_to(
                    SGB.DATA.FORMAT.telephone_number_international(
                        SGB.DATA.TELEPHONE_NUMBER.it_administrator()
                    ),
                    j_s((SGB.NAME, value)),
                    quote=True,
                )

            @staticmethod
            def whatsapp_send_message_to(
                telephone_number: str, message: str, quote: bool = False
            ) -> str:
                return CONST.MESSAGE.WHATSAPP.SEND_MESSAGE_TO_TEMPLATE.format(
                    telephone_number,
                    quote_plus(message) if quote else message.replace(" ", "+"),
                )

            @staticmethod
            def whatsapp_send_message_to_it(message: str) -> str:
                keyword_found: bool = False
                for item in [SGB.NAME, SGB.NAME_ALT]:
                    keyword_found = message.lower().startswith(item)
                    if keyword_found:
                        break
                if not keyword_found:
                    message = j_s((SGB.NAME, message))
                return SGB.DATA.FORMAT.whatsapp_send_message_to(
                    SGB.DATA.FORMAT.telephone_number_international(
                        SGB.DATA.TELEPHONE_NUMBER.it_administrator()
                    ),
                    message,
                    quote=True,
                )

            @staticmethod
            def telephone_number(
                value: nstr, prefix: str = CONST.TELEPHONE_NUMBER_PREFIX
            ) -> nstr:
                if e(value) or value.endswith(CONST.MESSAGE.WHATSAPP.GROUP_SUFFIX):
                    return value
                if prefix != CONST.TELEPHONE_NUMBER_PREFIX:
                    value = value[value.find(prefix) :]
                src_value: str = value
                if ne(value):
                    value = re.sub("[\\-\\(\\) ]", "", value)
                    if value.startswith(prefix):
                        value = value[len(prefix) :]
                    if len(value) == 0:
                        return src_value
                    value = prefix + (
                        value[1:]
                        if (
                            value[0] == "8"
                            or value[0] == CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX
                        )
                        else value
                    )
                    pattern: str = (
                        ("^\\" if prefix[0] == "+" else "^") + prefix + "[0-9]{10}"
                    )
                    matcher: re.Match = re.match(pattern, value)
                    if matcher is not None:
                        return matcher.group(0)
                    else:
                        return src_value
                else:
                    return src_value

            @staticmethod
            def telephone_number_international(value: str) -> str:
                return SGB.DATA.FORMAT.telephone_number(
                    value, CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX
                )

            @staticmethod
            def email(
                value: str,
                use_default_domain: bool = False,
                email_correction: bool = False,
            ) -> str:
                if use_default_domain and value.find(CONST.EMAIL_SPLITTER) == -1:
                    value = SGB.DATA.FORMAT.email(
                        j((value, ADDRESSES.SITE_ADDRESS), CONST.EMAIL_SPLITTER)
                    )
                if email_correction:
                    for char in '"(),:;<>[\\] ':
                        value = value.replace(char, "")
                    value = value.replace("/", ".")
                    email_name, email_domain = value.split(CONST.EMAIL_SPLITTER)
                    SGB.RESULT.FILES.execute("@email_correction")
                    for email_correction_item in EMAIL_CORRECTION:
                        if email_domain in email_correction_item[0]:
                            email_domain = email_correction_item[1]
                            break
                    value = j((email_name, email_domain), CONST.EMAIL_SPLITTER)
                return value.lower()

            @staticmethod
            def name(
                value: str,
                remove_non_alpha: bool = False,
                name_part_minimal_length: nint = None,
            ) -> str:
                name_part_list: strlist = DataTool.filter(
                    lambda item: len(item)
                    > (
                        0
                        if name_part_minimal_length is None
                        else name_part_minimal_length - 1
                    ),
                    value.split(" "),
                )
                if len(name_part_list) == 1:
                    value = value.lower()
                    value = re.sub("[^а-я]+", "", value) if remove_non_alpha else value
                    if len(value) > 1:
                        value = StringTool.capitalize(value)
                    return value
                return j_s(
                    list(
                        map(
                            lambda item: SGB.DATA.FORMAT.name(item, remove_non_alpha),
                            name_part_list,
                        )
                    )
                )

            @staticmethod
            def location_list(
                value: str, remove_first: bool = True, reversed: bool = True
            ) -> strlist:
                location_list: strlist = value.split(",")[int(remove_first) :]
                if reversed:
                    location_list.reverse()
                return DataTool.map(lambda item: item.split("=")[-1], location_list)

            @staticmethod
            def get_user_account_control_values(uac: int) -> strlist:
                result: strlist = []
                for count, item in enumerate(AD.USER_ACCOUNT_CONTROL):
                    if (pow(2, count) & uac) != 0:
                        result.append(item)
                return result

            @staticmethod
            def description(value: str) -> str:
                return SGB.DATA.FORMAT.description_list(value)[0]

            @staticmethod
            def description_list(value: str) -> strlist:
                return DataTool.map(lambda item: item.strip(), value.split("|"))

            @staticmethod
            def to_date(value: str) -> str:
                value = value.strip()
                value = value.replace("/", CONST.DATE_PART_DELIMITER)
                value = value.replace(",", CONST.DATE_PART_DELIMITER)
                value = value.replace(" ", CONST.DATE_PART_DELIMITER)
                return value

            @staticmethod
            def date(iso_datetime_value: str | datetime) -> str:
                return DateTimeTool.datetime_to_string(
                    (
                        datetime.fromisoformat(iso_datetime_value)
                        if isinstance(iso_datetime_value, str)
                        else iso_datetime_value
                    ),
                    CONST.DATE_FORMAT,
                )

            @staticmethod
            def datetime(iso_value: str | datetime, format: nstr = None) -> str:
                return DateTimeTool.datetime_to_string(
                    (
                        iso_value
                        if isinstance(iso_value, datetime)
                        else datetime.fromisoformat(iso_value)
                    ),
                    format or CONST.DATETIME_SECOND_ZEROS_FORMAT,
                )

        class TELEPHONE_NUMBER:

            pass


            """
            wappi_profile_to_telephone_number_map: dict | None = None
            cache: dict[str, str] = {}

            @staticmethod
            def all(active: bool = True) -> strlist:
                def filter_function(user: User) -> str:
                    return user.telephoneNumber is not None

                def map_function(user: User) -> str:
                    return SGB.DATA.FORMAT.telephone_number(user.telephoneNumber)

                return ResultTool.map(
                    map_function,
                    ResultTool.filter(
                        filter_function,
                        SGB.RESULT.USER.by_name(AD.SEARCH_ALL_PATTERN, active=active),
                    ),
                ).data

            @staticmethod
            def for_wappi(value: Any) -> nstr:
                WP = CONST.MESSAGE.WHATSAPP.WAPPI.Profiles
                value = EnumTool.get_by_value_or_key(WP, value)
                map: dict = (
                    SGB.DATA.TELEPHONE_NUMBER.wappi_profile_to_telephone_number_map
                )
                if n(map):
                    map = {
                        WP.CALL_CENTRE: SGB.DATA.TELEPHONE_NUMBER.call_centre_administrator(),
                        WP.IT: SGB.DATA.TELEPHONE_NUMBER.it_administrator(),
                        WP.MARKETER: SGB.DATA.TELEPHONE_NUMBER.marketer_administrator(),
                    }
                    SGB.DATA.TELEPHONE_NUMBER.wappi_profile_to_telephone_number_map = (
                        map
                    )
                return DataTool.if_is_in(map, value)

            @staticmethod
            def by_login(
                value: str,
                format: bool = True,
                active: bool = True,
                cached: bool = True,
            ) -> str:
                if cached and value in SGB.DATA.TELEPHONE_NUMBER.cache:
                    return SGB.DATA.TELEPHONE_NUMBER.cache[value]

                result: str = SGB.DATA.USER.by_login(
                    value, active, True
                ).telephoneNumber
                result = SGB.DATA.FORMAT.telephone_number(result) if format else result
                SGB.DATA.TELEPHONE_NUMBER.cache[value] = result
                return result

            @staticmethod
            def by_workstation_name(value: str) -> str:
                workstation: Workstation = SGB.RESULT.WORKSTATION.by_name(value).data
                return SGB.DATA.TELEPHONE_NUMBER.by_login(workstation.login)

            @staticmethod
            def by_full_name(value: Any, format: bool = True) -> str:
                value_string: nstr = None
                if isinstance(value, str):
                    value_string = value
                    value = FullNameTool.fullname_from_string(value)
                else:
                    value_string = FullNameTool.fullname_to_string(value)
                telephone_number: str = SGB.RESULT.MARK.by_full_name(
                    value_string, True
                ).data.telephoneNumber
                if SGB.CHECK.telephone_number(telephone_number):
                    return (
                        SGB.DATA.FORMAT.telephone_number(telephone_number)
                        if format
                        else telephone_number
                    )
                telephone_number = SGB.RESULT.USER.by_full_name(
                    value_string, True
                ).data.telephoneNumber
                if SGB.CHECK.telephone_number(telephone_number):
                    return (
                        SGB.DATA.FORMAT.telephone_number(telephone_number)
                        if format
                        else telephone_number
                    )
                details: str = f"Телефон для {value_string} не найден"
                raise NotFound(details)
            """
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
        def os_name() -> str:
            return SGB.SYS.environment_variable("OS")

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

    class RESULT(ResultTool):

        USER: IResultUserClient = UserClient.RESULT()
        SKYPE_BUSINESS: IResultSkypeBusinessClient = SkypeBusinessClient.RESULT()
        COMPUTER: IResultComputerClient = ComputerClient.RESULT()
        SSH: IResultSSHClient | None = SSHClient.RESULT()
        PASSWORD: IResultPasswordClient = PasswordClient.RESULT()
        
        WORKSTATION: IResultWorkstationClient | None = None
        
        def __init__(self):
            SGB.RESULT.WORKSTATION = WorkstationClient.RESULT(
                AD.WORKSTATIONS_CONTAINER_DN,
                SGB.RESULT.USER,
                SGB.CHECK.USER,
                SGB.RESULT.COMPUTER,
            )

        class SERVER:

            CONTAINER_DN: str = AD.SERVERS_CONTAINER_DN

            @staticmethod
            def all_description() -> Result[list[Computer]]:
                return SGB.RESULT.COMPUTER.all_description_by_container_dn(
                    SGB.RESULT.SERVER.CONTAINER_DN
                )

            @staticmethod
            def all() -> Result[list[Server]]:
                return SGB.RESULT.COMPUTER.by_container_dn(
                    SGB.RESULT.SERVER.CONTAINER_DN, Server
                )

            @staticmethod
            def by_name(value: str) -> Result[Server]:
                try:
                    return SGB.RESULT.COMPUTER.by_name(
                        value, SGB.RESULT.SERVER.CONTAINER_DN, Server
                    )
                except NotFound as _:
                    raise NotFound(f"Сервер с именем {value} не найден")

        """
        class ZABBIX:

            @staticmethod
            def _call(
                command: ZABBIX.Commands, parameters: tuple[Any, ...] | None = None
            ) -> nstr:
                return SGB.SERVICE.call_command_for_service(
                    SERVICE_ROLE.ZABBIX,
                    SERVICE_COMMAND.serve_command,
                    (command.name, *(parameters or ())),
                )

            @staticmethod
            def hosts() -> Result[list[ZabbixHost]]:
                return DataTool.to_result(
                    SGB.RESULT.ZABBIX._call(ZABBIX.Commands.get_host_list), ZabbixHost
                )

            @staticmethod
            def items(
                host_id: int,
                item_ids: int | tuple[int, ...] | None = None,
                fields: strtuple | None = None,
            ) -> Result[list[ZabbixMetrics]]:
                def mapper(item: ZabbixMetrics) -> ZabbixMetrics:
                    item.itemid = int(item.itemid)
                    item.lastclock = datetime.fromtimestamp(int(item.lastclock))
                    return item

                return ResultTool.map(
                    mapper,
                    DataTool.to_result(
                        SGB.RESULT.ZABBIX._call(
                            ZABBIX.Commands.get_item_list,
                            (
                                host_id,
                                item_ids,
                                fields,
                            ),
                        ),
                        ZabbixMetrics,
                    ),
                )

            @staticmethod
            def item(host_id: int, item_id: int) -> Result[ZabbixMetricsValue]:
                return ResultTool.with_first_item(
                    SGB.RESULT.ZABBIX.items(host_id, item_id)
                )

            @staticmethod
            def values(
                host_id: int, item_id: int | tuple[int, ...], limit: nint = None
            ) -> Result[list[ZabbixMetricsValue]]:
                def mapper(item: ZabbixMetricsValue) -> ZabbixMetricsValue:
                    item.clock = datetime.fromtimestamp(int(item.clock))
                    return item

                return ResultTool.map(
                    mapper,
                    DataTool.to_result(
                        SGB.RESULT.ZABBIX._call(
                            ZABBIX.Commands.get_value_list,
                            (host_id, item_id, limit),
                        ),
                        ZabbixMetricsValue,
                    ),
                )

            @staticmethod
            def value(host_id: int, item_id: int) -> Result[ZabbixMetricsValue]:
                return ResultTool.with_first_item(
                    SGB.RESULT.ZABBIX.values(host_id, item_id)
                )

        class JOURNALS:
            @staticmethod
            def get(
                value: JournalType | None = None, tag: Tags | None = None
            ) -> Result[list[JournalRecord]]:
                parameters: tuple = ()
                parameters += (EnumTool.get(tag)[0] if nn(tag) else None,)
                parameters += (EnumTool.get(value)[0] if nn(value) else None,)
                user_cache: dict[str, User] = {}

                def convert(event: EventDS) -> JournalRecord:
                    user: User | None = None
                    login: str = event.parameters[PARAM_ITEMS.LOGIN.name]
                    if login in user_cache:
                        user = user_cache[login]
                    else:
                        user = SGB.DATA.USER.by_login(login)
                        user_cache[login] = user
                    event.parameters[PARAM_ITEMS.TAG.name] = SGB.DATA.JOURNAL.tag_by_id(
                        event.parameters[PARAM_ITEMS.TAG.name]
                    )
                    event.parameters[PARAM_ITEMS.TYPE.name] = (
                        SGB.DATA.JOURNAL.type_by_any(
                            event.parameters[PARAM_ITEMS.TYPE.name]
                        )
                    )
                    title: nstr = event.parameters["title"]
                    try:
                        title: str = SGB.DATA.FORMAT.format(title)
                    except Exception as _:
                        pass
                    text: nstr = event.parameters["text"]
                    try:
                        text: str = SGB.DATA.FORMAT.format(text)
                    except Exception as _:
                        pass
                    return DataTool.fill_data_from_source(
                        JournalRecord(
                            event.timestamp,
                            applicant_user=user,
                            title=title,
                            text=text,
                        ),
                        event.parameters,
                        skip_not_none=True,
                    )

                return ResultTool.map(
                    convert,
                    SGB.RESULT.EVENTS.get(Events.ADD_JOURNAL_RECORD, parameters),
                )
        """

        class EMAIL:
            @staticmethod
            def information(value: str) -> Result[strdict]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_email_information,
                        (value, EmailVerificationMethods.ABSTRACT_API),
                    )
                )

            """@staticmethod
            def corrected(value: str) -> Result[nstr]:
                result: str = SGB.RESULT.EMAIL.information(value).data["autocorrect"]
                return Result(None, None if e(result) else result)
            """

        class EVENTS:

            @staticmethod
            def get_by_key(
                event_type: Events | None,
                parameters: tuple[Any, ...] | Any = None,
                timestamp: datetime | date | str | nint = None,
                count_as_result: bool = False,
            ) -> Result[list[EventDS] | int]:
                if not isinstance(parameters, (Tuple, List)):
                    parameters = (parameters,)
                return SGB.RESULT.EVENTS.get(
                    *SGB.EVENT.BUILDER.by_key(event_type, parameters),
                    timestamp,
                    count_as_result,
                )

            @staticmethod
            def get(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
                timestamp: (
                    datetime
                    | date
                    | str
                    | int
                    | tuple[date | datetime, date | datetime]
                    | None
                ) = None,
                count_as_result: bool = False,
            ) -> Result[list[EventDS] | int]:
                def extract_function(data: Any, count_as_result: bool) -> EventDS | int:
                    if count_as_result:
                        return data
                    result: EventDS = DataTool.fill_data_from_source(EventDS(), data)
                    # from json string to python object
                    result.parameters = DataTool.rpc_decode(result.parameters)
                    if isinstance(result.timestamp, str):
                        result.timestamp = DateTimeTool.datetime_from_string(
                            result.timestamp
                        )
                    return result

                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        (
                            SERVICE_COMMAND.get_event_count
                            if count_as_result
                            else SERVICE_COMMAND.get_event
                        ),
                        (
                            EventDS(timestamp=timestamp)
                            if n(event_type)
                            else EventDS(
                                event_type.name,
                                SGB.EVENT.BUILDER.create_parameters_map(
                                    event_type,
                                    parameters,
                                    check_for_parameters_count=False,
                                ),
                                timestamp=timestamp,
                            )
                        ),
                    ),
                    lambda data: extract_function(data, count_as_result),
                )

            @staticmethod
            def get_last(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
                count: int = 1,
            ) -> Result[list[EventDS]]:
                return SGB.RESULT.EVENTS.get(event_type, parameters, -abs(count))

            @staticmethod
            def get_last_by_key(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
                count: int = 1,
            ) -> Result[list[EventDS]]:
                return SGB.RESULT.EVENTS.get_by_key(event_type, parameters, -abs(count))

            @staticmethod
            def get_first(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
                count: int = 1,
            ) -> Result[list[EventDS]]:
                return SGB.RESULT.EVENTS.get(event_type, parameters, abs(count))

            @staticmethod
            def get_first_by_key(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
                count: int = 1,
            ) -> Result[list[EventDS]]:
                return SGB.RESULT.EVENTS.get_by_key(event_type, parameters, abs(count))

            @staticmethod
            def get_count(
                event_type: Events | None = None,
                parameters: tuple[Any, ...] | None = None,
            ) -> Result[int]:
                return SGB.RESULT.EVENTS.get(
                    event_type, parameters, count_as_result=True
                )

        class NOTES:

            _knowledge_database_cache: dict[
                str, tuple[Result[list[Note]], dict[str, Result[Note]]]
            ] = defaultdict()
            _local_database_cache: dict[
                str, tuple[Result[list[Note]], dict[str, Result[Note]]]
            ] = defaultdict()

            @staticmethod
            def find(value: str, label: nstr = None) -> Result[list[File]]:
                value = lw(value)
                filter_function: Callable[[Note], bool] = (
                    lambda item: lw(item.title).find(value) != -1
                )
                label = label or CONST.NOTES.SECTION
                if label not in SGB.RESULT.NOTES._local_database_cache or e(
                    SGB.RESULT.NOTES._local_database_cache[label]
                ):
                    SGB.ACTION.NOTES.cache_local_database()
                if e(SGB.RESULT.NOTES._local_database_cache[label]):
                    if label not in SGB.RESULT.NOTES._knowledge_database_cache or e(
                        SGB.RESULT.NOTES._knowledge_database_cache[label]
                    ):
                        SGB.ACTION.NOTES.cache_knowledge_database()
                result: Result[list[File]] = (
                    SGB.RESULT.NOTES._knowledge_database_cache
                    or SGB.RESULT.NOTES._local_database_cache
                )[label][0]
                if nn(value):
                    result = ResultTool.filter(filter_function, result, True)

                def sort_function(value: File) -> str:
                    return value.title

                return ResultTool.sort(sort_function, result)

            @staticmethod
            def find_gkeep_item(
                name: nstr = None,
                title: nstr = None,
                full_equaliment: bool = False,
            ) -> Result[list[GKeepItem]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_gkeep_item_list_by_any,
                        (name, title, full_equaliment),
                    ),
                    GKeepItem,
                )

            @staticmethod
            def fetch_from_local_database_by_label(
                args: list[Any] | None = None,
            ) -> Result[list[Note]]:
                event = args[1] or Events.SAVE_NOTE_FROM_KNOWLEDGE_BASE
                return ResultTool.map(
                    lambda item: SGB.RESULT.NOTES._convert_from_event(item).data,
                    SGB.RESULT.EVENTS.get(event),
                )

            @staticmethod
            def fetch_from_knowledge_database_by_label(
                args: list[Any],
            ) -> Result[list[Note]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_note_list_by_label,
                        (args[0], True),
                    ),
                    Note,
                )

            @staticmethod
            def fetch_default_from_knowledge_database() -> Result[list[Note]]:
                return SGB.RESULT.NOTES.fetch_from_knowledge_database_by_label(
                    CONST.NOTES.SECTION
                )

            @staticmethod
            def all(
                cached: bool = True, local: bool = True, label: nstr = None
            ) -> Result[list[Note]]:
                return SGB.RESULT.NOTES._all(
                    cached,
                    local,
                    label,
                )

            @staticmethod
            def _all(
                cached: bool = True,
                local: bool = True,
                label: nstr = None,
                event: Events | None = None,
            ) -> Result[list[Note]]:
                label = label or CONST.NOTES.SECTION
                if not local and (
                    not cached
                    or label not in SGB.RESULT.NOTES._knowledge_database_cache
                ):
                    SGB.ACTION.NOTES.cache_knowledge_database_by_label(label)
                    return SGB.RESULT.NOTES._knowledge_database_cache[label][0]
                if local and (
                    not cached or label not in SGB.RESULT.NOTES._local_database_cache
                ):
                    SGB.ACTION.NOTES.cache_local_database_by_label(label, event)
                    return SGB.RESULT.NOTES._local_database_cache[label][0]
                return (
                    SGB.RESULT.NOTES._local_database_cache
                    if local
                    else SGB.RESULT.NOTES._knowledge_database_cache
                )[label][0]

            @staticmethod
            def get_by_id(value: str, label: nstr = None) -> Result[Note] | None:
                label = label or CONST.NOTES.SECTION
                holder: tuple[
                    tuple[
                        Callable[[strlist], bool],
                        dict[str, tuple[Result[list[Note]], dict[str, Result[Note]]]],
                    ]
                ] = (
                    (
                        SGB.ACTION.NOTES.cache_local_database_by_label,
                        SGB.RESULT.NOTES._local_database_cache,
                    ),
                    (
                        SGB.ACTION.NOTES.cache_knowledge_database_by_label,
                        SGB.RESULT.NOTES._knowledge_database_cache,
                    ),
                )
                for item in holder:
                    if label not in item[1]:
                        item[0](label)
                    if value in item[1][label][1]:
                        return item[1][label][1][value]
                return None

            @staticmethod
            def _convert_from_event(value: EventDS) -> Result[Note | File]:
                parameters: strdict = value.parameters
                result: File | Note | None = File(
                    SGB.DATA.FORMAT.from_mysql(parameters[FIELD_NAME_COLLECTION.TITLE]),
                    SGB.DATA.FORMAT.from_mysql(parameters[FIELD_NAME_COLLECTION.TEXT]),
                    parameters[FIELD_NAME_COLLECTION.ID],
                )
                if value.name == Events.SAVE_NOTE_FROM_KNOWLEDGE_BASE.name:
                    result = DataTool.fill_data_from_source(
                        Note(images=parameters[FIELD_NAME_COLLECTION.IMAGES]),
                        result,
                        skip_not_none=True,
                    )

                return Result(data=result)

        class FILES:

            last_file_id: nint = None

            @staticmethod
            def fetch_from_local_database() -> Result[list[File]]:
                event: Events = Events.SAVE_FILE_FROM_KNOWLEDGE_BASE
                return ResultTool.map(
                    lambda item: DataTool.fill_data_from_source(File(), item),
                    SGB.RESULT.NOTES.fetch_from_local_database_by_label(event),
                )

            @staticmethod
            def all(cached: bool = True, local: bool = True) -> Result[list[File]]:
                return ResultTool.map(
                    lambda item: DataTool.fill_data_from_source(File(), item),
                    SGB.RESULT.NOTES._all(
                        cached,
                        local,
                        CONST.FILES.SECTION,
                        Events.SAVE_FILE_FROM_KNOWLEDGE_BASE,
                    ),
                )

            @staticmethod
            def by_name(value: str) -> Result[File]:
                return SGB.RESULT.FILES.find(value, strict_equality=True)

            @staticmethod
            def find(
                value: nstr = None,
                command_type: CommandTypes | None = None,
                exclude_private_files: bool = False,
                strict_equality: bool = False,
            ) -> Result[list[File]]:
                value = lw(value)
                filter_function: Callable[[File], bool] = lambda item: (
                    StringTool.contains(nns(item.title), nns(value))
                    if strict_equality
                    else StringTool.full_right_intersection_by_tokens(
                        nns(item.title),
                        nns(value),
                        (" ", CONST.NAME_SPLITTER, CONST.SPLITTER, ","),
                    )
                )
                was_updated: bool = False
                section: str = CONST.FILES.SECTION
                if section not in SGB.RESULT.NOTES._local_database_cache or e(
                    SGB.RESULT.NOTES._local_database_cache[section]
                ):
                    SGB.ACTION.FILES.cache_local_database()
                if e(SGB.RESULT.NOTES._local_database_cache[section]):
                    if section not in SGB.RESULT.NOTES._knowledge_database_cache or e(
                        SGB.RESULT.NOTES._knowledge_database_cache[section]
                    ):
                        SGB.ACTION.FILES.cache_knowledge_database()
                        was_updated = True
                else:
                    event: Events = Events.SAVE_FILE_FROM_KNOWLEDGE_BASE
                    if n(SGB.RESULT.FILES.last_file_id):
                        SGB.RESULT.FILES.last_file_id = SGB.DATA.VARIABLE.value(
                            FIELD_NAME_COLLECTION.LAST_ID, False
                        )
                    last_file_id: int = first(
                        SGB.RESULT.EVENTS.get_last(event), EventDS()
                    ).id
                    need_update: bool = last_file_id != SGB.RESULT.FILES.last_file_id
                    if need_update:
                        SGB.RESULT.FILES.last_file_id = last_file_id
                        SGB.DATA.VARIABLE.set(
                            FIELD_NAME_COLLECTION.LAST_ID, last_file_id
                        )
                        if not was_updated:
                            SGB.ACTION.FILES.cache_local_database()
                result: Result[list[File]] = (
                    None
                    if e(SGB.RESULT.NOTES._knowledge_database_cache)
                    else ResultTool.map(
                        lambda item: File(item.title, item.text, item.id),
                        SGB.RESULT.NOTES._knowledge_database_cache[section][0],
                    )
                ) or SGB.RESULT.NOTES._local_database_cache[section][0]
                result = (
                    SGB.RESULT.NOTES._local_database_cache[section][0]
                    if n(value)
                    else ResultTool.filter(filter_function, result, True)
                )
                result = (
                    result
                    if n(command_type)
                    else ResultTool.filter(
                        lambda item: SGB.DATA.EXTRACT.command_type(item)
                        == command_type,
                        result,
                    )
                )
                result = (
                    ResultTool.filter(
                        lambda item: item.title.find(j((CONST.SPLITTER, "@"))) == -1,
                        result,
                    )
                    if exclude_private_files
                    else result
                )

                def sort_function(value: File) -> str:
                    title_list: strlist = lw(value.title).split(CONST.SPLITTER)
                    return j(
                        [title_list[0]] + [title_list[-1]] + title_list[1:-1],
                        CONST.SPLITTER,
                    )

                return ResultTool.sort(sort_function, result)

            @staticmethod
            def execute(
                file_search_request: str,
                parameters: strdict | None = None,
                stdout_redirect: nbool = True,
                catch_exceptions: bool = False,
                use_default_stdout: bool = False,
            ) -> str | strdict | None:
                file: File | None = first(SGB.RESULT.FILES.by_name(file_search_request))
                if n(file):
                    return None
                return SGB.EXECUTOR.execute_python_localy(
                    nnt(file).text,
                    parameters,
                    stdout_redirect,
                    catch_exceptions,
                    use_default_stdout,
                )

            @staticmethod
            def execute_some(
                file_search_request: str,
                parameters: strdict | None = None,
                stdout_redirect: bool = True,
                catch_exceptions: bool = False,
                use_default_stdout: bool = False,
            ) -> strlist | None:
                file: File | None = None
                result: strlist = []
                file_list: list[File] = SGB.RESULT.FILES.find(file_search_request).data
                if e(file_list):
                    return None
                for file in file_list:
                    result.append(
                        SGB.EXECUTOR.execute_python_localy(
                            file.text,
                            parameters,
                            stdout_redirect,
                            catch_exceptions,
                            use_default_stdout,
                        )
                    )
                return result
            

        class DATA_STORAGE:
            @staticmethod
            def joke() -> Result[str]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.joke,
                    ),
                )

            @staticmethod
            def value(
                name: nstr,
                class_type_holder: T | Callable[[Any], T] | None,
                section: nstr = None,
            ) -> Result[T]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_storage_value, (name, section)
                    ),
                    class_type_holder,
                )

            @staticmethod
            def ogrn(code: str) -> Result[OGRN]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.get_ogrn_value, (code,)),
                    OGRN,
                )

            @staticmethod
            def fms_unit_name(code: str) -> Result[str]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.get_fms_unit_name, (code,))
                )

            @staticmethod
            def execute(query: str) -> Result[list[strdict]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.execute_data_source_query, (query,)
                    )
                )

        class MESSAGE:
            class DELAYED:
                @staticmethod
                def get(
                    search_condition: MessageSearchCritery | None = None,
                    take_to_work: bool = False,
                ) -> Result[list[DelayedMessageDS]]:
                    return DataTool.to_result(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.search_delayed_messages,
                            (search_condition, take_to_work),
                        ),
                        DelayedMessageDS,
                    )

        class RESOURCES:
            @staticmethod
            def get_status_list(
                checkable_section_list: list[CheckableSections] | None = None,
                force_update: bool = False,
                all: bool = False,
            ) -> Result[list[IResourceStatus]]:
                def fill_data(data: dict) -> IResourceStatus:
                    result: IResourceStatus | None = None
                    if "disk_list" in data:
                        result = DisksStatisticsStatus()
                    elif "check_certificate_status" in data:
                        result = SiteResourceStatus()
                    else:
                        result = ResourceStatus()
                    result = DataTool.fill_data_from_source(
                        result,
                        data,
                    )
                    if isinstance(result, DisksStatisticsStatus):
                        result.disk_list = DataTool.fill_data_from_list_source(
                            DiskStatistics, result.disk_list
                        )
                    return result

                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_resource_status_list,
                        (
                            (
                                None
                                if e(checkable_section_list)
                                else DataTool.map(
                                    lambda item: item.name, checkable_section_list
                                )
                            ),
                            force_update,
                            all,
                        ),
                    ),
                    fill_data,
                )

            @staticmethod
            def get_resource_status_list(
                force_update: bool = False, all: bool = False
            ) -> Result[list[ResourceStatus]]:
                return SGB.RESULT.RESOURCES.get_status_list(
                    [CheckableSections.RESOURCES], force_update, all
                )

            @staticmethod
            def get_status(
                checkable_section_list: list[CheckableSections],
                resource_desription_or_address: Any,
                force: bool = False,
            ) -> ResourceStatus:
                address: nstr = None
                if isinstance(resource_desription_or_address, ResourceDescription):
                    address = resource_desription_or_address.address
                elif isinstance(resource_desription_or_address, str):
                    address = resource_desription_or_address
                if ne(address):
                    resource_list: list[ResourceStatus] | None = (
                        SGB.RESULT.RESOURCES.get_status_list(
                            checkable_section_list, force
                        ).data
                    )
                    for item in resource_list:
                        if item.address == address:
                            return item
                return None

            @staticmethod
            def get_resource_status(
                resource_desription_or_address: Any, force: bool = False
            ) -> ResourceStatus:
                return SGB.RESULT.RESOURCES.get_status(
                    [CheckableSections.RESOURCES], resource_desription_or_address, force
                )

        class INDICATIONS:
            class DEVICE:
                @staticmethod
                def get(
                    name: nstr = None,
                ) -> Result[list[IndicationDevice] | IndicationDevice | None]:
                    getter: Callable = (
                        SGB.EVENT.BUILDER.indication_device_was_registered
                    )
                    result: Result[list[IndicationDevice]] = ResultTool.map(
                        lambda event: DataTool.fill_data_from_source(
                            IndicationDevice(), event.parameters
                        ),
                        SGB.RESULT.EVENTS.get(
                            *(
                                (getter(None), None)
                                if n(name)
                                else getter(IndicationDevice(name))
                            )
                        ),
                    )
                    return result if n(name) else ResultTool.with_first_item(result)

            @staticmethod
            def last_ct_value_containers(
                cached: bool, count: int = 1
            ) -> Result[list[CTIndicationsValueContainer]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_last_ct_indications_value_container_list,
                        (cached, count),
                    ),
                    CTIndicationsValueContainer,
                )

            @staticmethod
            def last_chiller_value_containers(
                cached: bool, count: int = 1, valid_values: bool = True
            ) -> Result[list[ChillerIndicationsValueContainer]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_last_сhiller_indications_value_container_list,
                        (cached, count, valid_values),
                    ),
                    ChillerIndicationsValueContainer,
                )

        class BACKUP:
            @staticmethod
            def robocopy_job_status_list() -> Result[list[RobocopyJobStatus]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.robocopy_get_job_status_list
                    ),
                    RobocopyJobStatus,
                )

        class SETTINGS:
            @staticmethod
            def key(key: nstr, default_value: Any = None) -> Result[Any]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_settings_value, (key, default_value)
                    )
                )

            @staticmethod
            def get(
                settings_item: SETTINGS | StorageVariableHolder | None,
            ) -> Result[Any] | Result[list[strdict]]:
                settings_item = EnumTool.get(settings_item)
                if n(settings_item):
                    SGB.RESULT.SETTINGS.get_by_name(None)
                return SGB.RESULT.SETTINGS.get_by_name(
                    settings_item.key_name or settings_item.name,
                    settings_item.default_value,
                )

            @staticmethod
            def get_by_name(value: nstr, default_value: Any = None) -> Result[Any]:
                return SGB.RESULT.SETTINGS.key(value, default_value)

        class INVENTORY:
            @staticmethod
            def report(
                report_file_path: str, open_for_edit: bool = False
            ) -> Result[list[InventoryReportItem]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_inventory_report,
                        (report_file_path, open_for_edit),
                    ),
                    InventoryReportItem,
                )

        class TIME_TRACKING:
            @staticmethod
            def today(
                tab_number_list: strlist | None = None,
            ) -> Result[list[TimeTrackingResultByPerson]]:
                return SGB.RESULT.TIME_TRACKING.create(tab_number_list=tab_number_list)

            def yesterday(
                tab_number_list: strlist | None = None,
            ) -> Result[list[TimeTrackingResultByPerson]]:
                yesterday: datetime = DateTimeTool.yesterday()
                return SGB.RESULT.TIME_TRACKING.create(
                    DateTimeTool.begin_date(yesterday),
                    DateTimeTool.begin_date(yesterday),
                    tab_number_list,
                )

            @staticmethod
            def in_period(
                day_start: int = 1,
                day_end: nint = None,
                month: nint = None,
                tab_number: strlist | None = None,
            ) -> Result[list[TimeTrackingResultByPerson]]:
                now: datetime = datetime.now()
                if nn(month):
                    now = now.replace(month=month)
                start_date: datetime = DateTimeTool.begin_date(now)
                end_date: datetime = DateTimeTool.end_date(now)
                if day_start < 0:
                    start_date -= timedelta(days=abs(day_start))
                else:
                    start_date = start_date.replace(day=day_start)
                if nn(day_end):
                    if day_end < 0:
                        day_end -= timedelta(days=abs(day_start))
                    else:
                        day_end = start_date.replace(day=day_start)
                return SGB.RESULT.TIME_TRACKING.create(start_date, end_date, tab_number)

            @staticmethod
            def create(
                start: datetime | date | None = None,
                end_date: datetime | date | None = None,
                tab_number_list: strlist | None = None,
            ) -> Result[list[TimeTrackingResultByPerson]]:
                now: datetime | None = DataTool.check(
                    e(start) or e(end_date),
                    datetime.now(),
                )
                if isinstance(start, date):
                    start = DateTimeTool.begin_date(start or now)
                if isinstance(end_date, date):
                    end_date = DateTimeTool.end_date(end_date or now)

                def get_date_or_time(entity: TimeTrackingEntity, date: bool) -> str:
                    return DataTool.check_not_none(
                        entity,
                        lambda: entity.TimeVal.split(DATE_TIME.SPLITTER)[not date],
                    )

                result_data: dict = {}
                full_name_by_tab_number_map: dict = {}
                result_data = defaultdict(
                    lambda: defaultdict(lambda: defaultdict(list))
                )
                data: list[TimeTrackingEntity] | None = DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_time_tracking,
                        (start, end_date, tab_number_list),
                    ),
                    TimeTrackingEntity,
                ).data
                for time_tracking_entity in data or []:
                    tab_number: str = time_tracking_entity.TabNumber
                    full_name_by_tab_number_map[tab_number] = (
                        time_tracking_entity.FullName
                    )
                    result_data[time_tracking_entity.DivisionName][tab_number][
                        get_date_or_time(time_tracking_entity, True)
                    ].append(time_tracking_entity)
                result: list[TimeTrackingResultByDivision] = []
                has_lunch_break: strlist = []
                ResultTool.every(
                    lambda user: has_lunch_break.append(user.name),
                    SGB.RESULT.USER.by_property(AD.UserProperies.HasLunchBreak),
                )
                for division_name in result_data:
                    if n(division_name):
                        continue
                    result_division_item: TimeTrackingResultByDivision = (
                        TimeTrackingResultByDivision(division_name)
                    )
                    result.append(result_division_item)
                    for tab_number in result_data[division_name]:
                        full_name: str = full_name_by_tab_number_map[tab_number]
                        result_person_item: TimeTrackingResultByPerson = (
                            TimeTrackingResultByPerson(
                                tab_number, full_name_by_tab_number_map[tab_number]
                            )
                        )
                        result_division_item.list.append(result_person_item)
                        for date_item in result_data[division_name][tab_number]:
                            time_tracking_entity_list: list[TimeTrackingEntity] = (
                                result_data[division_name][tab_number][date_item]
                            )
                            time_tracking_enter_entity: TimeTrackingEntity = None
                            time_tracking_exit_entity: TimeTrackingEntity = None
                            for (
                                time_tracking_entity_list_item
                            ) in time_tracking_entity_list:
                                if time_tracking_entity_list_item.Mode == 1:
                                    time_tracking_enter_entity = (
                                        time_tracking_entity_list_item
                                    )
                                if time_tracking_entity_list_item.Mode == 2:
                                    time_tracking_exit_entity = (
                                        time_tracking_entity_list_item
                                    )
                            duration: int = 0
                            if time_tracking_enter_entity is not None:
                                if time_tracking_exit_entity is not None:
                                    enter_time: datetime = datetime.fromisoformat(
                                        time_tracking_enter_entity.TimeVal
                                    ).timestamp()
                                    exit_time: datetime = datetime.fromisoformat(
                                        time_tracking_exit_entity.TimeVal
                                    ).timestamp()
                                    if enter_time < exit_time:
                                        #    enter_time, exit_time = exit_time, enter_time
                                        #    time_tracking_enter_entity, time_tracking_exit_entity = time_tracking_exit_entity, time_tracking_enter_entity
                                        duration = int(exit_time - enter_time) - (
                                            60 * 60
                                            if (full_name in has_lunch_break)
                                            else 0
                                        )
                                    result_person_item.duration += duration
                            result_person_item.list.append(
                                TimeTrackingResultByDate(
                                    date_item,
                                    get_date_or_time(time_tracking_enter_entity, False),
                                    get_date_or_time(time_tracking_exit_entity, False),
                                    duration,
                                )
                            )
                for division in result:
                    for person in division.list:
                        index: int = 0
                        length: int = len(person.list)
                        for _ in range(length):
                            item: TimeTrackingResultByDate = person.list[index]
                            if item.duration == 0:
                                # if item.enter_time is None and item.exit_time is not None:
                                if index < length - 1:
                                    item_next: TimeTrackingResultByDate = person.list[
                                        index + 1
                                    ]
                                    if nn(item.exit_time):
                                        if nn(item_next.enter_time):
                                            duration = int(
                                                datetime.fromisoformat(
                                                    item.date
                                                    + DATE_TIME.SPLITTER
                                                    + item.exit_time
                                                ).timestamp()
                                                - datetime.fromisoformat(
                                                    item_next.date
                                                    + DATE_TIME.SPLITTER
                                                    + item_next.enter_time
                                                ).timestamp()
                                            )
                                            # print(full_name, full_name in has_lunch_break)
                                            # duration -= 60*60 if (full_name in has_lunch_break) else 0
                                            item.duration = duration
                                            person.duration += duration
                                            if n(item_next.exit_time):
                                                index += 1
                            index += 1
                            if index >= length - 1:
                                break

                return Result(FIELD_COLLECTION.ORION.TIME_TRACKING_RESULT, result)

        class PRINTER:
            @staticmethod
            def call(printer_name: str, oid: str) -> Result[Any]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.printer_snmp_call, (printer_name, oid)
                    )
                )

            @staticmethod
            def all() -> Result[list[PrinterADInformation]]:
                def filter_by_server_name(
                    printer_list: list[PrinterADInformation],
                ) -> list[PrinterADInformation]:
                    return DataTool.filter(
                        lambda item: item.serverName.find(
                            CONST.HOST.PRINTER_SERVER.NAME
                        )
                        == 0,
                        printer_list,
                    )

                result: Result[list[PrinterADInformation]] = DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.get_printer_list),
                    PrinterADInformation,
                )
                return Result(result.fields, filter_by_server_name(result.data))

            @staticmethod
            def report() -> Result[list[PrinterReport]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.printers_report),
                    PrinterReport,
                )

        class MARK:
            @staticmethod
            def by_tab_number(value: str | int) -> Result[Mark]:
                result: Result[Mark] = DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_mark_by_tab_number, str(value)
                    ),
                    Mark,
                )
                if e(result):
                    raise NotFound(
                        j_s(("Карта доступа с номером", escs(value), "не найдена"))
                    )
                return result

            @staticmethod
            def by_division(division_or_id: PersonDivision | int) -> Result[list[Mark]]:
                division_id: int = DataTool.check(
                    isinstance(division_or_id, PersonDivision),
                    lambda: division_or_id.id,
                    division_or_id,
                )
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_mark_list_by_division_id, division_id
                    ),
                    Mark,
                )

            @staticmethod
            def person_divisions() -> Result[list[PersonDivision]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_mark_person_division_list
                    ),
                    PersonDivision,
                )

            @staticmethod
            def by_name(value: str, first_item: bool = False) -> Result[list[Mark]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.get_mark_by_person_name, value
                    ),
                    Mark,
                    first_item,
                )

            @staticmethod
            def by_full_name(
                value: FullName | str, first_item: bool = False
            ) -> Result[list[Mark]]:
                return SGB.RESULT.MARK.by_name(
                    (
                        FullNameTool.fullname_to_string(value)
                        if isinstance(value, FullName)
                        else value
                    ),
                    first_item,
                )

            @staticmethod
            def temporary_list() -> Result[list[TemporaryMark]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.get_temporary_mark_list),
                    TemporaryMark,
                )

            @staticmethod
            def by_any(value: str | int) -> Result[list[Mark]]:
                if isinstance(value, int):
                    value = str(value)
                if SGB.CHECK.MARK.tab_number(value):
                    return ResultTool.as_list(SGB.RESULT.MARK.by_tab_number(value))
                elif SGB.CHECK.name(value, True):
                    return SGB.RESULT.MARK.by_name(value)
                return Result()

            @staticmethod
            def all() -> Result[list[Mark]]:
                return DataTool.to_result(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.get_mark_list), Mark
                )

            @staticmethod
            def temporary_mark_owner(mark: Mark) -> Result[Mark]:
                return DataTool.check(
                    mark is not None
                    and EnumTool.get(MarkType, mark.type) == MarkType.TEMPORARY,
                    lambda: DataTool.to_result(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.get_owner_mark_for_temporary_mark,
                            mark.TabNumber,
                        ),
                        Mark,
                    ),
                    None,
                )

            @staticmethod
            def temporary_mark_owner_by_tab_number(value: str) -> Result[Mark]:
                return SGB.RESULT.MARK.temporary_mark_owner(
                    SGB.RESULT.MARK.by_tab_number(value).data
                )

    class CHECK:

        USER: ICheckUserClient = UserClient.CHECK()

        def __init__(self):
            pass

        class BACKUP:

            @staticmethod
            def robocopy_job_is_active(name: str) -> nbool:
                result: list[RobocopyJobStatus] = DataTool.filter(
                    lambda job: job.name == name,
                    SGB.RESULT.BACKUP.robocopy_job_status_list().data,
                )
                if e(result):
                    return None
                return first(result).active

        class EVENTS:
            @staticmethod
            def has(
                value: Events | None, parameters: tuple[Any, ...] | None = None
            ) -> bool:
                return ne(SGB.RESULT.EVENTS.get(value, parameters))

            @staticmethod
            def has_by_key(
                value: Events | None, parameters: tuple[Any, ...] | None = None
            ) -> nbool:
                return SGB.CHECK.EVENTS.has(
                    *SGB.EVENT.BUILDER.by_key(value, parameters)
                )

            @staticmethod
            def timeouted(
                event: Events,
                parameters: dict | None = None,
                timeout_in_seconds: nint = None,
            ) -> bool:
                event_ds: EventDS | None = SGB.RESULT.get_first_item(
                    SGB.RESULT.sort(
                        SGB.RESULT.EVENTS.get(event, parameters),
                        lambda item: item.timestamp,
                        reserve=True,
                    )
                )
                return (
                    n(event_ds)
                    or (DateTimeTool.now() - event_ds.timestamp).total_seconds()
                    > timeout_in_seconds
                )

            @staticmethod
            def compare_by_timestamp(event_type: Events, event_type2: Events) -> bool:
                get_event_timestamp: Callable[[Events], datetime] = (
                    lambda event: ResultTool.get_first_item(
                        SGB.RESULT.EVENTS.get_last(event)
                    ).timestamp
                )
                return get_event_timestamp(event_type) > get_event_timestamp(
                    event_type2
                )

        class SETTINGS:
            @staticmethod
            def by_time(current: datetime, settings: SETTINGS) -> bool:
                return DateTimeTool.is_equal_by_time(
                    current, SGB.SETTINGS.to_datetime(settings)
                )

        class NOTES:
            @staticmethod
            def exists(
                name: nstr, title: nstr = None, full_equaliment: bool = True
            ) -> bool:
                return ne(
                    SGB.RESULT.NOTES.find_gkeep_item(name, title, full_equaliment)
                )

        class JOURNALS:
            @staticmethod
            def exists(name: nstr, caption: nstr = None) -> bool:
                return nn(
                    SGB.DATA.JOURNAL.type_by_any(name)
                    or SGB.DATA.JOURNAL.type_by_any(caption)
                )

        class RESOURCE:
            @staticmethod
            def accessibility_by_psping_with_port(
                address_or_ip: str,
                port: int,
                host: nstr = None,
                count: nint = None,
                check_all: bool = True,
            ) -> nbool:
                return SGB.CHECK.RESOURCE.accessibility_by_psping(
                    j((address_or_ip, port), CONST.SPLITTER), host, count, check_all
                )

            @staticmethod
            def accessibility_by_smb_port(
                address_or_ip: str,
                host: nstr = None,
                count: nint = None,
                check_all: bool = True,
            ) -> nbool:
                return SGB.CHECK.RESOURCE.accessibility_by_psping_with_port(
                    address_or_ip, WINDOWS.PORT.SMB, host, count, check_all
                )

            @staticmethod
            def accessibility_by_psping(
                address_or_ip: str,
                host: nstr = None,
                count: nint = None,
                check_all: bool = True,
            ) -> nbool:
                return SGB.EXECUTOR.psping(address_or_ip, host, count, check_all)

            @staticmethod
            def accessibility_by_ping(
                address_or_ip: str,
                host: nstr = None,
                count: nint = None,
                timeout: nint = None,
            ) -> nbool:
                return SGB.EXECUTOR.ping(address_or_ip, host, count, timeout)

            @staticmethod
            def accessibility(resource_status_or_address: Any) -> nbool:
                resource_status: ResourceStatus | None = None
                if isinstance(resource_status_or_address, ResourceDescription):
                    resource_status = resource_status_or_address
                else:
                    resource_status = SGB.RESULT.RESOURCES.get_resource_status(
                        resource_status_or_address
                    )
                return (
                    None
                    if n(resource_status)
                    else resource_status.inaccessibility_counter
                    < resource_status.inaccessibility_check_values[0]
                )

            @staticmethod
            def wappi_profile_accessibility(
                value: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | str, cached: bool = False
            ) -> bool:
                return (
                    SGB.CHECK.RESOURCE.accessibility(
                        SGB.RESULT.RESOURCES.get_resource_status(
                            EnumTool.get_value(
                                value,
                                EnumTool.get(
                                    CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT
                                ),
                            )
                        )
                    )
                    if cached
                    else SGB.CHECK.MESSAGE.WHATSAPP.WAPPI.accessibility(value, False)
                )

            @staticmethod
            def ws_accessibility(name: str) -> bool:
                result: Result[Workstation] = SGB.RESULT.WORKSTATION.by_name(name)
                return ne(result) and result.data.accessable

        class EMAIL:
            @staticmethod
            def accessability(
                value: str,
                cached: bool = True,
                verification_method: EmailVerificationMethods | None = None,
            ) -> bool:
                def internal_accessability(
                    value: str, verification_method: EmailVerificationMethods
                ) -> bool:
                    domain: str = value.split(CONST.EMAIL_SPLITTER)[1]
                    if domain == "icloud.com":
                        verification_method = EmailVerificationMethods.NORMAL
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.check_email_accessibility,
                            (value, verification_method, cached),
                        )
                    )

                # if not internal_accessability(value, verification_method):
                verification_method = (
                    verification_method or EmailVerificationMethods.DEFAULT
                )
                return internal_accessability(value, verification_method)
                # return True

        class FILES:


            @staticmethod
            def has_content_by_computer(
                file_path: str, computer: Computer, value: strlist, encoding: str = CHARSETS.UTF8
            ) -> bool:
                file_content: str = A.D_F.read_content_by_computer(
                    file_path,
                    computer,
                    A.CT_CHR.UTF16,
                )
                lines_exists: bool = True
                for line in value:
                    lines_exists = lines_exists and A.D.contains(
                        file_content, line,
                    )
                    if not lines_exists:
                        return False
                return True
            

            @staticmethod
            def excel_file(path: str) -> bool:
                return os.path.isfile(path) and PathTool.get_extension(path) in [
                    FILE.EXTENSION.EXCEL_OLD,
                    FILE.EXTENSION.EXCEL_NEW,
                ]


        class MESSAGE:
            class WHATSAPP:
                class WAPPI:
                    @staticmethod
                    def from_me(value: str) -> bool:
                        value = SGB.DATA.FORMAT.telephone_number(value)
                        return value in [
                            SGB.DATA.TELEPHONE_NUMBER.it_administrator(),
                            SGB.DATA.TELEPHONE_NUMBER.call_centre_administrator(),
                            SGB.DATA.TELEPHONE_NUMBER.marketer_administrator(),
                        ]

                    @staticmethod
                    def accessibility(
                        profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr,
                        cached: bool = True,
                    ) -> bool:
                        def internal_accessibility(
                            profile: (
                                CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr
                            ) = None,
                        ) -> bool:
                            profile, profile_value = (
                                SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                            )
                            url: str = j(
                                (
                                    CONST.MESSAGE.WHATSAPP.WAPPI.URL_GET_STATUS,
                                    profile_value,
                                )
                            )
                            headers: dict = {
                                "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION[
                                    profile
                                ],
                                "Content-Type": "application/json",
                            }
                            response_result: dict = None
                            try:
                                response: Response = requests.get(url, headers=headers)
                                response_result = json.loads(response.text)
                            except Exception:
                                return False
                            if "status" in response_result:
                                if response_result["status"] == "error":
                                    return False
                            return response_result["app_status"] == "open"

                        return (
                            SGB.CHECK.RESOURCE.wappi_profile_accessibility(
                                profile, True
                            )
                            if cached
                            else internal_accessibility(profile)
                        )

        @staticmethod
        def login(value: str) -> bool:
            pattern: str = (
                r"^[a-z]+[a-z_0-9]{"
                + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH - 1)
                + ",}"
            )
            return nn(re.fullmatch(pattern, value, re.IGNORECASE))

        class COMPUTER:

            @staticmethod
            def process_is_running(
                pid_or_name: int | str,
                host: nstr = None,
                login: nstr = None,
                password: nstr = None,
            ) -> bool:
                return SGB.EXECUTOR.check_process_is_running(
                    pid_or_name, host, login, password
                )

            @staticmethod
            def windows_service_running(service_name: str, computer_name: str) -> nbool:
                result: nstr = SGB.EXECUTOR.execute_for_result(
                    SGB.EXECUTOR.create_command_for_psexec(
                        ("sc", "query", service_name), computer_name, interactive=True
                    ),
                    True,
                    True,
                )
                return None if n(result) else result.find("4  RUNNING") != -1

            @staticmethod
            def accessibility(name: str) -> nbool:
                try:
                    return SGB.RESULT.COMPUTER.by_name(name).data.accessable
                except NotFound as _:
                    return None

        class WORKSTATION:

            @staticmethod
            def accessibility(name: str) -> nbool:
                try:
                    return first(SGB.RESULT.WORKSTATION.by_name(name)).accessable
                except NotFound as _:
                    return None

            @staticmethod
            def name(value: str) -> bool:
                value = SGB.DATA.FORMAT.string(value)
                for prefix in AD.WORKSTATION_PREFIX_LIST:
                    if value.startswith(prefix):
                        return True
                return False

            @staticmethod
            def exists(name: str) -> bool:
                name = name.lower()
                return ne(
                    ResultTool.filter(
                        lambda workstation: name == workstation.name.lower(),
                        SGB.RESULT.WORKSTATION.all_description(),
                    )
                )

            @staticmethod
            def property(
                workstation: Computer, property: AD.ComputerProperties
            ) -> bool:
                return BM.has(workstation.properties, property)

            @staticmethod
            def watchable(workstation: Computer) -> bool:
                return SGB.CHECK.WORKSTATION.property(
                    workstation, AD.ComputerProperties.Watchable
                )

            @staticmethod
            def shutdownable(workstation: Computer) -> bool:
                return SGB.CHECK.WORKSTATION.property(
                    workstation, AD.ComputerProperties.Shutdownable
                )

            @staticmethod
            def rebootable(workstation: Computer) -> bool:
                return SGB.CHECK.WORKSTATION.property(
                    workstation, AD.ComputerProperties.Rebootable
                )

        @staticmethod
        def telephone_number(value: str | nint, international: bool = False) -> bool:
            return (
                ne(value)
                and re.fullmatch(
                    ("" if international else r"^\+") + "[0-9]{11,13}$", str(value)
                )
                is not None
            )

        @staticmethod
        def telephone_number_international(value: str) -> bool:
            return SGB.CHECK.telephone_number(value, True)

        @staticmethod
        def email(
            value: str, check_accesability: bool = False, cached: bool = True
        ) -> bool:
            return ne(
                re.fullmatch(
                    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", value
                )
            ) and (
                not check_accesability or SGB.CHECK.EMAIL.accessability(value, cached)
            )

        @staticmethod
        def name(value: str, use_space: bool = False) -> bool:
            pattern = (
                r"[а-яА-ЯёЁ"
                + (" " if use_space else "")
                + "]{"
                + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH)
                + ",}$"
            )
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def full_name(value: str) -> bool:
            pattern = (
                r"[а-яА-ЯёЁ]{"
                + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH)
                + ",} [а-яА-ЯёЁ]{"
                + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH)
                + ",} [а-яА-ЯёЁ]{"
                + str(CONST.NAME_POLICY.PART_ITEM_MIN_LENGTH)
                + ",}$"
            )
            return re.fullmatch(pattern, value) is not None

        @staticmethod
        def password(value: str, settings: PasswordSettings | None = None) -> bool:
            settings = settings or PASSWORD.SETTINGS.DEFAULT
            return PasswordTools.check_password(
                value, settings.length, settings.special_characters
            )

    class LOG:
        executor = ErrorableThreadPoolExecutor(max_workers=1)

        @staticmethod
        def send(
            value: str,
            channel: LogMessageChannels = LogMessageChannels.DEFAULT,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
            image_path: nstr = None,
        ) -> str:
            level = level or LogMessageFlags.DEFAULT

            def internal_send_message(
                message: str,
                channel_name: str,
                level_value: int,
                image_path: nstr = None,
            ) -> None:
                with SGB.ERROR.detect():
                    try:
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.send_log_message,
                            (message, channel_name, level_value, image_path),
                            blocked=False,
                        )
                    except Error as error:
                        SGB.output.error("Log send error")

            SGB.LOG.executor.submit(
                SGB.ERROR.wrap(internal_send_message),
                value,
                channel.name,
                DataTool.as_bitmask_value(level),
                image_path,
            )
            return value

        @staticmethod
        def debug_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.DEBUG_BOT, level)

        @staticmethod
        def debug(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.DEBUG, level)

        @staticmethod
        def journal(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.JOURNAL, level)

        @staticmethod
        def journal_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.JOURNAL_BOT, level)

        @staticmethod
        def new_email_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.NEW_EMAIL_BOT, level)

        @staticmethod
        def new_email(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.NEW_EMAIL, level)

        @staticmethod
        def services(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.SERVICES, level)

        @staticmethod
        def time_tracking(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.TIME_TRACKING, level)

        @staticmethod
        def resources(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.RESOURCES, level)

        @staticmethod
        def printers(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.PRINTER, level)

        @staticmethod
        def services_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.SERVICES_BOT, level)

        @staticmethod
        def backup(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.BACKUP, level)

        @staticmethod
        def polibase_document(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
            image_path: nstr = None,
        ) -> str:
            return SGB.LOG.send(
                message, LogMessageChannels.POLIBASE_DOCUMENT, level, image_path
            )

        @staticmethod
        def polibase_document_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(
                message, LogMessageChannels.POLIBASE_DOCUMENT_BOT, level
            )

        @staticmethod
        def polibase(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.POLIBASE, level)

        @staticmethod
        def polibase_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.POLIBASE_BOT, level)

        @staticmethod
        def card_registry(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.CARD_REGISTRY, level)

        @staticmethod
        def card_registry_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.CARD_REGISTRY_BOT, level)

        @staticmethod
        def polibase_error(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.POLIBASE_ERROR, level)

        @staticmethod
        def polibase_error_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.POLIBASE_ERROR_BOT, level)

        @staticmethod
        def it(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.IT, level)

        @staticmethod
        def it_bot(
            message: str,
            level: int | tuple[Enum, ...] | Enum | list[Enum] | list[int] | None = None,
        ) -> str:
            return SGB.LOG.send(message, LogMessageChannels.IT_BOT, level)

    class MESSAGE:

        class WORKSTATION:

            executor = ErrorableThreadPoolExecutor(max_workers=10)

            @staticmethod
            def to_all_workstations(
                message: str,
                filter_group=None,
                to_all_user_workstation_name_list: strlist | None = None,
                session: Session | None = None,
                test: bool = True,
                timeout: int = 60,
            ) -> None:
                session = session or SGB.session
                filter_user_login_list: strlist = (
                    None
                    if filter_group is None
                    else ResultTool.map(
                        lambda item: item.login.lower(),
                        SGB.RESULT.USER.by_group(filter_group),
                    ).data
                )
                filter_user_login_list_is_empty: bool = e(filter_user_login_list)
                to_all_user_workstation_name_list_is_empty: bool = e(
                    to_all_user_workstation_name_list
                )

                def filter_function(workstation: Workstation) -> bool:
                    workstation_name: str = workstation.name.lower()
                    if test:
                        return workstation_name == CONST.TEST.WORKSTATION_MAME
                    return workstation.accessable and (
                        (
                            filter_user_login_list_is_empty
                            or workstation.login in filter_user_login_list
                        )
                        or (
                            to_all_user_workstation_name_list_is_empty
                            or workstation_name in to_all_user_workstation_name_list
                        )
                    )

                def every_action(workstation: Workstation) -> None:
                    def internal_send_message(
                        user_login: nstr, workstation_name: str, message: str
                    ) -> None:
                        if (
                            ne(to_all_user_workstation_name_list)
                            and workstation_name in to_all_user_workstation_name_list
                        ):
                            if not test:
                                SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                                    None, workstation_name, message, timeout
                                )
                        else:
                            if e(user_login):
                                if test:
                                    SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                                        user_login, workstation_name, message, timeout
                                    )
                                else:
                                    pass
                                # dont send message - cause workstation is on but no one user is logged
                            else:
                                if test:
                                    if workstation_name == CONST.TEST.WORKSTATION_MAME:
                                        SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                                            user_login,
                                            workstation_name,
                                            message,
                                            timeout,
                                        )
                                else:
                                    SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                                        user_login, workstation_name, message, timeout
                                    )

                    result_message: str = (
                        f"Сообщение от {session.user_given_name} ({SGB.DATA.FORMAT.description(session.get_user().description)}):"
                    )
                    result_message += f" День добрый, "
                    user: User | None = (
                        None
                        if e(workstation.login)
                        else SGB.RESULT.USER.by_login(
                            workstation.login, True, True
                        ).data
                    )
                    result_message += DataTool.if_not_empty(
                        user, lambda user: f"{FullNameTool.to_given_name(user)}, ", ""
                    )
                    result_message += message
                    SGB.MESSAGE.WORKSTATION.executor.submit(
                        SGB.ERROR.wrap(internal_send_message),
                        workstation.login,
                        workstation.name.lower(),
                        result_message,
                    )

                ResultTool.every(
                    every_action,
                    ResultTool.filter(filter_function, SGB.RESULT.WORKSTATION.all()),
                )

            @staticmethod
            def to_user(
                value: User | str,
                message: str,
                timeout: int = 60,
                method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE,
            ) -> bool:
                return SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                    value.login if isinstance(value, User) else value,
                    None,
                    message,
                    timeout,
                    method_type,
                )

            @staticmethod
            def to_workstation(
                value: Computer | str,
                message: str,
                timeout: int = 60,
                method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE,
            ) -> bool:
                return SGB.MESSAGE.WORKSTATION.by_workstation_name(
                    value.name if isinstance(value, Computer) else value,
                    message,
                    timeout,
                    method_type,
                )

            @staticmethod
            def by_workstation_name(
                value: str,
                message: str,
                timeout: int = 60,
                method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE,
            ) -> bool:
                user: User | None = None
                try:
                    user = SGB.RESULT.USER.by_workstation_name(value).data
                except NotFound as _:
                    pass
                return SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                    None if n(user) else user.login,
                    value,
                    message,
                    timeout,
                    method_type,
                )

            @staticmethod
            def to_user_or_workstation(
                user_login: str,
                workstation_name: str,
                message: str,
                timeout: int = 60,
                method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE,
            ) -> bool:
                if method_type == WorkstationMessageMethodTypes.REMOTE:
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.send_message_to_user_or_workstation,
                            (user_login, workstation_name, message, timeout),
                        )
                    )

                def internal_send_by_login_and_workstation_name(
                    login: str, workstation_name: str
                ) -> None:
                    if method_type == WorkstationMessageMethodTypes.LOCAL_PSTOOL_MSG:
                        SGB.EXECUTOR.execute(
                            SGB.EXECUTOR.create_command_for_psexec(
                                (
                                    CONST.MSG.EXECUTOR,
                                    j(("/time:", timeout)),
                                    login,
                                    message,
                                ),
                                workstation_name,
                            ),
                            False,
                        )
                    if method_type == WorkstationMessageMethodTypes.LOCAL_MSG:
                        SGB.EXECUTOR.execute(
                            [
                                CONST.MSG.EXECUTOR,
                                j(("/time:", timeout)),
                                login,
                                j(("/server:", workstation_name)),
                                message,
                            ],
                            False,
                        )

                if n(workstation_name):
                    result: Result[list[Workstation]] = SGB.RESULT.WORKSTATION.by_login(
                        user_login
                    )
                    ResultTool.every(
                        lambda workstation: internal_send_by_login_and_workstation_name(
                            user_login, workstation.name
                        ),
                        result,
                    )
                else:
                    if n(user_login):
                        internal_send_by_login_and_workstation_name(
                            "*", workstation_name
                        )
                    else:
                        internal_send_by_login_and_workstation_name(
                            user_login, workstation_name
                        )
                return True

            @staticmethod
            def by_login(
                value: str,
                message: str,
                timeout: int = 60,
                method_type: WorkstationMessageMethodTypes = WorkstationMessageMethodTypes.REMOTE,
            ) -> bool:
                return SGB.MESSAGE.WORKSTATION.to_user_or_workstation(
                    value, None, message, timeout, method_type
                )

        class WHATSAPP:
            class WAPPI:
                class QUEUE:

                    @staticmethod
                    def add(value: Message, high_priority: bool = False) -> bool:
                        value.message = SGB.DATA.FORMAT.whatsapp_message(value.message)
                        return DataTool.rpc_decode(
                            SGB.SERVICE.call_command(
                                SERVICE_COMMAND.add_message_to_queue,
                                (value, high_priority),
                            )
                        )

                WAPPI_PROFILE_MAP: dict | None = None

                @staticmethod
                def _get_header(
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles,
                ) -> strdict:
                    return {
                        "accept": "application/json",
                        "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION[
                            profile
                        ],
                        "Content-Type": "application/json",
                    }

                @staticmethod
                def _get_profile_value(
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles,
                ) -> tuple[CONST.MESSAGE.WHATSAPP.WAPPI.Profiles, str]:
                    return (
                        profile := EnumTool.get_by_value(
                            CONST.MESSAGE.WHATSAPP.WAPPI.Profiles,
                            profile or CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT,
                        ),
                        EnumTool.get_value(
                            profile,
                            EnumTool.get(profile),
                        ),
                    )

                @staticmethod
                def get_wappi_collection() -> dict:
                    WP = CONST.MESSAGE.WHATSAPP.WAPPI
                    result: dict = SGB.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP or {
                        WP.Profiles.IT: SGB.DATA.TELEPHONE_NUMBER.it_administrator(),
                        WP.Profiles.CALL_CENTRE: SGB.DATA.TELEPHONE_NUMBER.call_centre_administrator(),
                        WP.Profiles.MARKETER: SGB.DATA.TELEPHONE_NUMBER.marketer_administrator(),
                    }
                    if SGB.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP is None:
                        SGB.MESSAGE.WHATSAPP.WAPPI.WAPPI_PROFILE_MAP = result
                    return result

                @staticmethod
                def send_to_group(
                    group: CONST.MESSAGE.WHATSAPP.GROUP | str,
                    message: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles = CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.IT,
                ) -> bool:
                    return SGB.MESSAGE.WHATSAPP.WAPPI.send(
                        EnumTool.get(group), message, profile
                    )

                @staticmethod
                def get_profile_id(
                    telephone_number: str,
                ) -> CONST.MESSAGE.WHATSAPP.WAPPI.Profiles:
                    if SGB.CHECK.telephone_number_international(telephone_number):
                        telephone_number = SGB.DATA.FORMAT.telephone_number(
                            telephone_number
                        )
                    profile_id_collection = (
                        SGB.MESSAGE.WHATSAPP.WAPPI.get_wappi_collection()
                    )
                    for item in profile_id_collection:
                        if profile_id_collection[item] == telephone_number:
                            return item
                    return None

                @staticmethod
                def get_message_list(
                    telephone_number: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | None = None,
                ) -> list[WhatsAppMessage]:
                    profile, profile_value = (
                        SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                    )
                    url: str = j(
                        (
                            CONST.MESSAGE.WHATSAPP.WAPPI.URL_GET_MESSAGES,
                            profile_value,
                            "&chat_id=",
                            telephone_number,
                            CONST.MESSAGE.WHATSAPP.WAPPI.CONTACT_SUFFIX,
                        )
                    )
                    headers: dict = {
                        "Authorization": CONST.MESSAGE.WHATSAPP.WAPPI.AUTHORIZATION[
                            profile
                        ],
                        "Content-Type": "application/json",
                    }
                    result: list[WhatsAppMessage] = []
                    try:
                        response: Response = requests.get(url, headers=headers)
                    except Exception:
                        return result
                    response_result: dict = json.loads(response.text)
                    has_error: bool = response_result["status"] == "error" or (
                        "detail" in response_result
                        and response_result["detail"] == "Messages not found"
                    )
                    key: str = "message"
                    if not has_error:
                        if DataTool.is_in(response_result, key):
                            for message_item in response_result[key]:
                                if message_item["type"] == "chat":
                                    result.append(
                                        WhatsAppMessage(
                                            message_item["body"],
                                            message_item["fromMe"],
                                            str(message_item["from"]).split(
                                                CONST.EMAIL_SPLITTER
                                            )[0],
                                            str(message_item["to"]).split(
                                                CONST.EMAIL_SPLITTER
                                            )[0],
                                            profile,
                                            message_item["time"],
                                        )
                                    )
                    return result

                @staticmethod
                def send_location(
                    recipient: str,
                    value: tuple[float, float],
                    address: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    profile, profile_value = (
                        SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                    )
                    payload: strdict = {"recipient": recipient}
                    payload["latitude"] = value[0]
                    payload["longitude"] = value[1]
                    payload["address"] = SGB.DATA.FORMAT.whatsapp_message(address)
                    url: str = j(
                        (CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_LOCATION, profile_value)
                    )
                    try:
                        response: Response = requests.post(
                            url,
                            data=dumps(payload),
                            headers=SGB.MESSAGE.WHATSAPP.WAPPI._get_header(profile),
                        )
                    except ConnectTimeout:
                        return False
                    if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                        SGB.LOG.resources(
                            "Аккаунт Wappi (сервис для отправики сообщений через WhatsApp) не оплачен",
                            LogMessageFlags.ERROR,
                        )
                    return response.status_code == 200

                @staticmethod
                def send(
                    recipient: str,
                    value: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    profile, profile_value = (
                        SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                    )
                    url: nstr = None
                    payload: dict = {
                        "recipient": recipient,
                        "body": SGB.DATA.FORMAT.whatsapp_message(value),
                    }
                    url: str = CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_MESSAGE
                    url = j((url, profile_value))
                    try:
                        response: Response = requests.post(
                            url,
                            data=dumps(payload),
                            headers=SGB.MESSAGE.WHATSAPP.WAPPI._get_header(profile),
                        )
                    except ConnectTimeout:
                        return False
                    if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                        SGB.LOG.resources(
                            "Аккаунт Wappi (сервис для отправики сообщений через WhatsApp) не оплачен",
                            LogMessageFlags.ERROR,
                        )
                    return response.status_code == 200

                @staticmethod
                def get_status(
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> WappiStatus:
                    profile, profile_value = (
                        SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                    )
                    url: str = j((CONST.MESSAGE.WHATSAPP.WAPPI.STATUS, profile_value))
                    try:
                        response: Response = requests.get(
                            url, headers=SGB.MESSAGE.WHATSAPP.WAPPI._get_header(profile)
                        )
                    except ConnectTimeout:
                        return False
                    return DataTool.fill_data_from_source(
                        WappiStatus(), json.loads(response.text)
                    )

                @staticmethod
                def send_base64_file(
                    url: str,
                    recipient: str,
                    caption: str,
                    file_name: nstr,
                    base64_content: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    profile, profile_value = (
                        SGB.MESSAGE.WHATSAPP.WAPPI._get_profile_value(profile)
                    )
                    payload: strdict = {
                        "recipient": recipient,
                        "caption": SGB.DATA.FORMAT.whatsapp_message(caption),
                        "b64_file": base64_content,
                    }
                    if ne(file_name):
                        payload["file_name"] = file_name

                    url = j((url, profile_value))
                    try:
                        response: Response = requests.post(
                            url,
                            data=dumps(payload),
                            headers=SGB.MESSAGE.WHATSAPP.WAPPI._get_header(profile),
                        )
                    except ConnectTimeout:
                        return False
                    if response.status_code == CONST.ERROR.WAPPI.PROFILE_NOT_PAID:
                        SGB.LOG.resources(
                            "Аккаунт Wappi (сервис для отправики сообщений через WhatsApp) не оплачен",
                            LogMessageFlags.ERROR,
                        )
                    return response.status_code == 200

                @staticmethod
                def send_video(
                    recipient: str,
                    caption: str,
                    base64_content: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    return SGB.MESSAGE.WHATSAPP.WAPPI.send_base64_file(
                        CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_VIDEO,
                        recipient,
                        caption,
                        None,
                        base64_content,
                        profile,
                    )

                @staticmethod
                def send_image(
                    recipient: str,
                    caption: str,
                    base64_content: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    return SGB.MESSAGE.WHATSAPP.WAPPI.send_base64_file(
                        CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_IMAGE,
                        recipient,
                        caption,
                        None,
                        base64_content,
                        profile,
                    )

                @staticmethod
                def send_document(
                    recipient: str,
                    caption: str,
                    file_name: str,
                    base64_content: str,
                    profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
                ) -> bool:
                    return SGB.MESSAGE.WHATSAPP.WAPPI.send_base64_file(
                        CONST.MESSAGE.WHATSAPP.WAPPI.URL_SEND_DOCUMENT,
                        recipient,
                        caption,
                        file_name,
                        base64_content,
                        profile,
                    )

            @staticmethod
            def send_via_browser(telephone_number: str, message: str) -> bool:
                pywhatkit_is_exists: bool = (
                    importlib.util.find_spec("pywhatkit") is not None
                )
                if not pywhatkit_is_exists:
                    SGB.output.green(
                        "Установка библиотеки для отправки сообщения. Ожидайте..."
                    )
                    if not SGB.UPDATER.package_operation("pywhatkit"):
                        SGB.output.error(
                            "Ошибка при установке библиотеки для отправки сообщений!"
                        )
                try:
                    import pywhatkit as pwk

                    pwk.sendwhatmsg_instantly(telephone_number, message)
                except Exception as уrror:
                    SGB.output.error("Ошибка при отправке сообщения!")

            @staticmethod
            def send(
                recipient: str,
                message: Any,
                via_wappi: bool = True,
                use_alternative: bool = True,
                wappi_profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
            ) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile,
                    EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT),
                )
                result: bool = False
                recipient = SGB.DATA.FORMAT.telephone_number(recipient)
                if via_wappi:
                    result = SGB.MESSAGE.WHATSAPP.WAPPI.send(
                        recipient, message, wappi_profile
                    )
                if result:
                    return result
                if use_alternative or not via_wappi:
                    return SGB.MESSAGE.WHATSAPP.send_via_browser(recipient, message)
                return False

            @staticmethod
            def send_video(
                recipient: str,
                caption: str,
                base64_value: str,
                wappi_profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
            ) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile,
                    EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT),
                )
                recipient = SGB.DATA.FORMAT.telephone_number(recipient)
                return SGB.MESSAGE.WHATSAPP.WAPPI.send_video(
                    recipient, caption, base64_value, wappi_profile
                )

            @staticmethod
            def send_image(
                recipient: str,
                caption: str,
                base64_value: str,
                wappi_profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
            ) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile,
                    EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT),
                )
                recipient = SGB.DATA.FORMAT.telephone_number(recipient)
                return SGB.MESSAGE.WHATSAPP.WAPPI.send_image(
                    recipient, caption, base64_value, wappi_profile
                )

            @staticmethod
            def send_document(
                recipient: str,
                caption: str,
                base64_value: str,
                wappi_profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
            ) -> bool:
                wappi_profile = EnumTool.get_value(
                    wappi_profile,
                    EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT),
                )
                recipient = SGB.DATA.FORMAT.telephone_number(recipient)
                return SGB.MESSAGE.WHATSAPP.WAPPI.send_document(
                    recipient, caption, base64_value, wappi_profile
                )

            @staticmethod
            def send_to_user(
                user: User,
                message: Any,
                via_wappi: bool = True,
                use_alternative: bool = True,
                wappi_profile: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
            ) -> bool:
                return SGB.MESSAGE.WHATSAPP.send(
                    user.telephoneNumber,
                    message,
                    via_wappi,
                    use_alternative,
                    EnumTool.get_value(
                        wappi_profile,
                        EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.DEFAULT),
                    ),
                )

        class DELAYED:
            @staticmethod
            def register(message: DelayedMessage) -> int:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.register_delayed_message,
                        SGB.ACTION.MESSAGE.DELAYED._prepeare_message(message),
                    )
                )

            @staticmethod
            def send(message: DelayedMessage, high_priority: bool = True) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.send_delayed_message,
                        (
                            SGB.ACTION.MESSAGE.DELAYED._prepeare_message(message),
                            high_priority,
                        ),
                    )
                )

    class ACTION:

        SSH: IActionSSHClient = SSHClient.ACTION()
        FILE: IActionFile = File.ACTION(SSH)
        PASSWORD: IActionPasswordClient = PasswordClient.ACTION()
            
            
        class EMAIL:
            @staticmethod
            def send(recipient: str, subject: str, message: str) -> nbool:
                if not SGB.CHECK.email(recipient):
                    recipient = SGB.DATA.FORMAT.email(
                        recipient, use_default_domain=True
                    )
                if SGB.CHECK.email(recipient, check_accesability=True):
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.send_email,
                            (recipient, j(("Subject:", nl(subject, count=2), message))),
                        )
                    )
                return None

        class PATH:
            @staticmethod
            def listen(value: str) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.listen_for_new_files, (value,)
                    )
                )

        class EVENTS:
            @staticmethod
            def register(
                value: Events,
                parameters: strdict | tuple[Any, ...] | None = None,
                remove_before: bool = False,
            ) -> bool:
                if isinstance(parameters, Tuple):
                    parameters = SGB.EVENT.BUILDER.create_parameters_map(
                        value, parameters
                    )
                event_description: EventDescription = EnumTool.get(value)
                if remove_before:
                    parameters_for_removing: strdict | None = parameters
                    key_name_list: strtuple | None = DataTool.map(
                        lambda item: item.name,
                        DataTool.filter(
                            lambda item: item.key, event_description.params
                        ),
                    )
                    if nn(key_name_list):
                        parameters_for_removing = {}
                        for key_name_item in key_name_list:
                            parameters_for_removing[key_name_item] = parameters[
                                key_name_item
                            ]
                    SGB.ACTION.EVENTS.remove(value, parameters_for_removing)
                visible_parameters: strdict = {}
                for index, parameter_key in enumerate(parameters):
                    if event_description.params[index].saved:
                        visible_parameters[parameter_key] = parameters[parameter_key]
                parameters = visible_parameters
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.register_event,
                        (
                            EventDS(
                                value.name,
                                parameters,
                                DateTimeTool.now(use_microsecond=True),
                            ),
                        ),
                    )
                )

            @staticmethod
            def update(
                value: Events,
                parameter_for_search: tuple[Any, ...],
                parameters_for_set: tuple[Any, ...],
            ) -> bool:
                return SGB.ACTION.EVENTS.remove(
                    value, parameter_for_search
                ) and SGB.ACTION.EVENTS.register(
                    value,
                    SGB.EVENT.BUILDER.create_parameters_map(value, parameters_for_set),
                )

            @staticmethod
            def remove_by_key(
                event_type: Events | None, parameters: tuple[Any, ...] | None = None
            ) -> Result[list[EventDS] | int]:
                return SGB.ACTION.EVENTS.remove(
                    *SGB.EVENT.BUILDER.by_key(event_type, parameters)
                )

            @staticmethod
            def remove(
                value: Events,
                parameters: tuple[Any, ...] | strdict | None = None,
            ) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.remove_event,
                        EventDS(
                            value.name,
                            DataTool.check(
                                isinstance(parameters, dict),
                                parameters,
                                lambda: SGB.EVENT.BUILDER.create_parameters_map(
                                    value, parameters, check_for_parameters_count=False
                                ),
                            ),
                        ),
                    )
                )

        class MOBILE_INPUT_OUTPUT:

            @staticmethod
            def send_outside(value: str, recipient: str, flags: nint = None) -> None:
                SGB.ACTION.MOBILE_INPUT_OUTPUT.send(
                    value,
                    recipient,
                    flags=BM.add(
                        (flags or 0), (SessionFlags.OUTSIDE, SessionFlags.CLI)
                    ),
                    use_command_prefix=False,
                )

            @staticmethod
            def send(
                value: str,
                recipient: str | Enum,
                chat_id: str | Enum | None = None,
                flags: nint = None,
                return_result_key: nstr = None,
                args: tuple[Any, ...] | None = None,
                use_command_prefix: bool = True,
            ) -> None:
                recipient = EnumTool.get(recipient)
                if use_command_prefix and not value.startswith(SGB.NAME):
                    value = j_s((SGB.NAME, value))
                SGB.EVENT.whatsapp_message_received(
                    WhatsAppMessage(
                        value,
                        False,
                        recipient,
                        recipient,
                        EnumTool.get(CONST.MESSAGE.WHATSAPP.WAPPI.Profiles.IT),
                        int(DateTimeTool.now().timestamp()),
                        EnumTool.get(chat_id),
                        flags,
                        return_result_key,
                        args,
                    )
                )

        class BACKUP:
            @staticmethod
            def start_robocopy_job(
                name: nstr = None,
                source: nstr = None,
                destination: nstr = None,
                force: bool = False,
                block: bool = False,
            ) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.robocopy_start_job,
                        (name, source, destination, force, block),
                    )
                )

            @staticmethod
            def start_robocopy_job_by_name(
                value: str, force: bool = False, block: bool = False
            ) -> bool:
                return SGB.ACTION.BACKUP.start_robocopy_job(
                    value, force=force, block=block
                )

        class DATA_STORAGE:
            @staticmethod
            def value(value: Any, name: nstr = None, section: nstr = None) -> bool:
                try:
                    name = name or value.__getattribute__("name")
                except AttributeError as error:
                    pass
                else:
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.set_storage_value, (name, value, section)
                        )
                    )

        class MESSAGE:
            class DELAYED:
                @staticmethod
                def update(
                    value: DelayedMessageDS, search_critery: MessageSearchCritery
                ) -> bool:
                    return DataTool.rpc_decode(
                        SGB.SERVICE.call_command(
                            SERVICE_COMMAND.update_delayed_message,
                            (value, search_critery),
                        )
                    )

                @staticmethod
                def update_status(
                    value: DelayedMessageDS, status: MessageStatuses
                ) -> bool:
                    return SGB.ACTION.MESSAGE.DELAYED.update(
                        DelayedMessageDS(status=status.value),
                        MessageSearchCritery(id=value.id),
                    )

                @staticmethod
                def complete(value: DelayedMessageDS) -> bool:
                    return SGB.ACTION.MESSAGE.DELAYED.update_status(
                        value, MessageStatuses.COMPLETE
                    )

                @staticmethod
                def abort(value: DelayedMessageDS) -> bool:
                    return SGB.ACTION.MESSAGE.DELAYED.update_status(
                        value, MessageStatuses.ABORT
                    )

                @staticmethod
                def _prepeare_message(message: DelayedMessage) -> DelayedMessage:
                    if n(message.type):
                        message.type = MessageTypes.WHATSAPP.value
                    if nn(message.date):
                        if isinstance(message.date, datetime):
                            message.date = DateTimeTool.datetime_to_string(
                                message.date, CONST.ISO_DATETIME_FORMAT
                            )
                    if nn(message.sender):
                        message.sender = EnumTool.get_value(message.sender)
                    if message.type == MessageTypes.WHATSAPP.value and ne(
                        message.recipient
                    ):
                        if SGB.CHECK.telephone_number(message.recipient):
                            # +7 -> 7
                            message.recipient = SGB.DATA.FORMAT.telephone_number(
                                message.recipient,
                                CONST.INTERNATIONAL_TELEPHONE_NUMBER_PREFIX,
                            )
                    return message

        class SETTINGS:
            @staticmethod
            def key(key: str, value: Any) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.set_settings_value, (key, value)
                    )
                )

            @staticmethod
            def set(settings_item: SETTINGS | str, value: Any) -> bool:
                settings_item_value = EnumTool.get(settings_item)
                if isinstance(settings_item_value, VariantableStorageVariable):
                    if value not in settings_item_value.variants:
                        raise NotFound(
                            j_s((value, "not in", settings_item_value.variants))
                        )
                return SGB.ACTION.SETTINGS.key(
                    if_else(
                        isinstance(settings_item, str),
                        settings_item,
                        lambda: settings_item.value.key_name or settings_item.name,
                    ),
                    value,
                )

            @staticmethod
            def set_default(settings_item: SETTINGS) -> bool:
                return SGB.ACTION.SETTINGS.set(
                    settings_item, settings_item.value.default_value
                )

        """
        class USER:
            @staticmethod
            def drop_user_cache() -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(SERVICE_COMMAND.drop_user_cache)
                )

            @staticmethod
            def create_from_template(
                container_dn: str,
                full_name: FullName,
                login: str,
                password: str,
                description: str,
                telephone: str,
                email: str,
            ) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.create_user_by_template,
                        (
                            container_dn,
                            full_name,
                            login,
                            password,
                            description,
                            telephone,
                            email,
                        ),
                    )
                )

            @staticmethod
            def set_telephone_number(user: User, telephone: str) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.set_user_telephone_number,
                        (user.distinguishedName, telephone),
                    )
                )

            @staticmethod
            def set_password(user: User, password: str) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.set_user_password,
                        (user.distinguishedName, password),
                    )
                )

            @staticmethod
            def set_status(user: User, status: str, container: ADContainer) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.set_user_status,
                        (
                            user.distinguishedName,
                            status,
                            DataTool.check(
                                container, lambda: container.distinguishedName
                            ),
                        ),
                    )
                )

            @staticmethod
            def remove(user: User) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.remove_user, user.distinguishedName
                    )
                )
        """
        USER: IActionUserClient = UserClient.ACTION()

        class COMPUTER:

            @staticmethod
            def stop_windows_service(name: str, computer_name: str) -> bool:
                output: str = SGB.EXECUTOR.execute_for_result(
                    SGB.EXECUTOR.create_command_for_psexec(
                        ("sc", "stop", name),
                        computer_name,
                        interactive=True,
                        run_from_system_account=True,
                    ),
                    True,
                    True,
                )
                return output.find("3  STOP_PENDING") != -1

            @staticmethod
            def start_windows_service(name: str, computer_name: str) -> bool:
                output: str = SGB.EXECUTOR.execute_for_result(
                    SGB.EXECUTOR.create_command_for_psexec(
                        ("sc", "start", name),
                        computer_name,
                        interactive=True,
                        run_from_system_account=True,
                    ),
                    True,
                    True,
                )
                return output.find("2  START_PENDING") != -1

        class DOCUMENTS:
            @staticmethod
            def create_statistics_chart(type: STATISTICS.Types) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.create_statistics_chart, (type.name,)
                    )
                )

            @staticmethod
            def save_xlsx(title: str, result: Result[list[strdict]], path: str) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.save_xlsx,
                        (title, result.fields.list, result.data, path),
                    )
                )

            @staticmethod
            def save_base64_as_image(path: str, content: str) -> bool:
                return DataTool.rpc_decode(
                    SGB.SERVICE.call_command(
                        SERVICE_COMMAND.save_base64_as_image, (path, content)
                    )
                )

        WORKSTATION: ActionWorkstationClientExtended = ActionWorkstationClientExtended()


class ActionStack(list):
    def __init__(
        self,
        caption: str = "",
        *argv: Callable[[], ActionValue | None],
        input: InputBase = None,
        output: OutputBase = None,
    ):
        self.input = input or SGB.input
        self.output = output or SGB.output
        self.acion_value_list: list[ActionValue] = []
        self.caption = caption
        for arg in argv:
            self.append(arg)
        self.start()

    def call_actions_by_index(self, index: int = 0, change: bool = False):
        previous_change: bool = False
        while True:
            try:
                action_value: ActionValue = self[index]()
                if action_value:
                    if change or previous_change:
                        previous_change = False
                        if index < len(self.acion_value_list):
                            self.acion_value_list[index] = action_value
                        else:
                            self.acion_value_list.append(action_value)
                    else:
                        self.acion_value_list.append(action_value)
                index = index + 1
                if index == len(self) or change:
                    break
            except KeyboardInterrupt:
                self.output.new_line()
                self.output.error("Повтор предыдущих действия")
                self.output.new_line()
                if index > 0:
                    previous_change = True
                    # self.show_action_values()
                    # index = index - 1
                else:
                    continue

    def show_action_values(self) -> None:
        def label(item: ActionValue, _):
            return item.caption

        self.call_actions_by_index(
            self.input.index(
                "Выберите свойство для изменения, введя индекс",
                self.acion_value_list,
                label,
            ),
            True,
        )

    def start(self):
        self.call_actions_by_index()
        while True:
            self.output.new_line()
            self.output.head2(self.caption)
            for action_value in self.acion_value_list:
                self.output.value(action_value.caption, action_value.value)
            if self.input.confirm("Данные верны", True):
                break
            else:
                self.show_action_values()


def sgb_package_name(standalone_name: str) -> str:
    return SGB.PATH.FACADE.DITRIBUTIVE.NAME(standalone_name)


def import_from(file_name: str, *args) -> list[Any]:
    import_result: strdict = SGB.RESULT.FILES.execute(file_name, stdout_redirect=False)
    result: list[Any] = []
    if n(args):
        return import_result
    for item in args:
        if item in import_result:
            result.append(import_result[item])
    return result


class A:

    root = SGB()

    NAME = SGB.NAME

    IW = root.INPUT_WAIT

    R = root.RESULT
    R()
    R_U = R.USER
    R_SB = R.SKYPE_BUSINESS
    R_WS = R.WORKSTATION
    R_COMP = R.COMPUTER
    R_SSH = R.SSH
    R_P = R.PASSWORD

    D = root.DATA

    D_U = D.USER
    D_COM = D.COMMUNITY
    D_C = D.CHECK
    D_FL = D.FILTER
    D_FRMT = D.FORMAT
    D_F = D.FILE
    D_Ex = D.EXTRACT
    D_Ex_E = D_Ex.EVENT
    D_V = D.VARIABLE
    D_TN = D.TELEPHONE_NUMBER
    D_V_E = D_V.ENVIRONMENT

    C = root.CHECK
    C()
    C_U = C.USER
    C_WS = C.WORKSTATION
    C_COMP = C.COMPUTER

    SRV = root.SERVICE

    I = root.input
    I_U = I.user

    O = root.output

    SYS = root.SYS
    U = root.UPDATER
    EXC = root.EXECUTOR
    ER = root.ERROR
    E = root.EVENT
    E_B = E.BUILDER

    CT = CONST
    CT_COM = COMMUNITY
    CT_COM_SET = COMMUNITY_SETTING_ITEM
    CT_FACADE = FACADE
    CT_PY = PYTHON
    CT_PORT = CONST.PORT
    CT_CMDT = CommandTypes
    CT_CHR = CHARSETS
    CT_LNK = LINK
    CT_WINDOWS = WINDOWS
    CT_RBK = ROBOCOPY
    CT_H = HOSTS
    CT_HM = HOST_MAP
    CT_FNT = FONT
    CT_SVC_R = SERVICE_ROLE
    CT_SRV_R = SERVER_ROLE
    CT_SC = SERVICE_COMMAND
    CT_SubT = SUBSCRIBTION_TYPE
    CT_F = FILE

    CT_F_E = CT_F.EXTENSION
    CT_FC = FIELD_COLLECTION
    CT_S = SETTINGS
    CT_ME = CT.MESSAGE
    CT_ME_WH = CT_ME.WHATSAPP
    CT_ME_WH_G = CT_ME.WHATSAPP.GROUP
    CT_ME_WH_W = CT_ME_WH.WAPPI
    CT_L_ME_F = LogMessageFlags
    CT_L_ME_CH = LogMessageChannels
    CT_V = CT.VISUAL
    CT_E = Events
    CT_J = JournalType
    CT_Tag = Tags
    CT_MRT = MedicalResearchTypes
    CT_FNC = FIELD_NAME_COLLECTION
    CT_FCA = FieldCollectionAliases
    CT_UP = ACTIVE_DIRECTORY_USER_PROPERTIES
    CT_AD = AD
    CT_AD_UP = AD.UserProperies
    CT_T = Tags
    CT_CR = CT.CARD_REGISTRY
    CT_PI = PARAM_ITEMS

    C_V_T_E = D_C.VARIABLE.TIMESTAMP.EXPIRED

    PTH = root.PATH
    PTH_DS = PTH.DATA_STORAGE
    PTH_BUILD = PTH.BUILD
    PTH_FNT = PTH.FONTS
    PTH_FCD = PTH.FACADE
    PTH_FCD_DIST = PTH_FCD.DITRIBUTIVE

    S = root.SETTINGS
    S_U = S.USER

    SE = root.session

    C_R = C.RESOURCE
    C_F = C.FILES

    A = root.ACTION
    A()
    A_WS = A.WORKSTATION
    A_COMP = A.COMPUTER
    A_U = A.USER
    A_F = A.FILE
    A_SSH = A.SSH
    A_P = A.PASSWORD

    V = root.VERSION

    """
   
    R_ME = R.MESSAGE
    R_R = R.RESOURCES
    R_RCG = R.RECOGNIZE
    
    R_IND = R.INDICATIONS
    R_N = R.NOTES
    R_E = R.EVENTS
    R_INV = R.INVENTORY
    
    R_B = R.BACKUP
    R_DS = R.DATA_STORAGE
    
    R_F = R.FILES
    R_TT = R.TIME_TRACKING
    R_PR = R.PRINTER
    R_SRVS = R.SERVER
    R_EM = R.EMAIL
   

    
    D_V = D.VARIABLE
    D_V_T = D_V.TIMESTAMP
    D_V_T_E = D_V_T.EXPIRED
    
    D_TN = D.TELEPHONE_NUMBER
    D_MR = D.MATERIALIZED_RESOURCES
    
    D_STAT = D.STATISTICS
    D_IOT = D.IOTDevices

    
    D_J = D.JOURNAL
    A = root.ACTION

    A_DOC = A.DOCUMENTS
    
    ME = root.MESSAGE
    ME_P = ME.POLIBASE
   
    #
    A_ME = A.MESSAGE
    A_TT = A.TIME_TRACKING
    A_MIO = A.MOBILE_INPUT_OUTPUT
    R_ME_D = R_ME.DELAYED
    A_ME_D = A_ME.DELAYED
    A_E = A.EVENTS
    A_EM = A.EMAIL

    #
    ME_WS = ME.WORKSTATION
    ME_P = ME.POLIBASE
    ME_WH = ME.WHATSAPP
    ME_D = ME.DELAYED
    ME_WH_W = ME_WH.WAPPI
    ME_WH_W_Q = ME_WH_W.QUEUE
    A_ME_WH_W_Q = ME_WH_W.QUEUE
    #
    
    S_P = S.POLIBASE
    S_R = S.RESOURCE
    S_WS = S.WORKSTATION
    S_P_V = S_P.VISIT
    S_P_RN = S_P.REVIEW_NOTIFICATION
    #
   
    
    D_ACT = D.ACTIONS
    
    C_INV = C.INVENTORY
    C_TT = C.TIME_TRACKING
    C_A = C.ACCESS
    C_S = C.SETTINGS
    
    C_ME = C.MESSAGE
    C_ME_WH = C_ME.WHATSAPP
    C_ME_WH_W = C_ME_WH.WAPPI
    C_N = C.NOTES
    C_J = C.JOURNALS
    C_EML = C.EMAIL
    

    C_F = C.FILES
    #
    A_DR = A.DOOR
    
    A_U = A.USER
    C_U = C.USER
    D_F = D.FORMAT
    # D_F_B = D_F.BACKUP
    # D_F_IOT = D_F.IOTDevices
    D_CO = D.CONVERT
    C_E = C.EVENTS

    R_IND_D = R_IND.DEVICE
    
    A_PTH = A.PATH

    C_WS = C.WORKSTATION
    
    A_B = A.BACKUP

    A_DS = A.DATA_STORAGE

    
   
    L = root.LOG

   
    """


def delay(
    action: Callable[[], None], value: float = 1.0, block: bool = False, *args
) -> SGBThread | None:
    def action_support(*agrs) -> None:
        if value > 0:
            sleep(value)
        action(*agrs)

    if block:
        action_support(args)
    else:
        return SGBThread(action_support, args=args)


def checked_threaded(
    value: Callable,
    checker: Callable[[], bool] | None = None,
    *args,
) -> None:
    if n(checker):
        delay(value, 0, False, *args)
    else:

        def internal_value() -> None:
            while_not_do(checker)
            value(*args)

        delay(internal_value, 0)


def thread(value: Callable, *args) -> None:
    checked_threaded(value, None, *args)


def thread_on_accessibility(
    value: Callable,
    service_object: SERVICE_ROLE | ServiceDescriptionBase | None = None,
) -> None:
    checked_threaded(
        value,
        lambda: A.SRV.check_on_availabllity(service_object or RPC.service_description),
    )


def subscribe_on(
    sc: SERVICE_COMMAND,
    type_value: int = SUBSCRIBTION_TYPE.ON_RESULT,
    name: nstr = None,
) -> bool:
    return A.SRV.subscribe_on(sc, type_value, name)


def send_message(
    value: str | Message,
    recipient: str | Enum | None = None,
    sender: CONST.MESSAGE.WHATSAPP.WAPPI.Profiles | nstr = None,
    queued: bool = False,
) -> bool:
    if isinstance(value, Message):
        queued = True
    if nn(recipient):
        recipient = EnumTool.get(recipient)
    if queued:
        return SGB.MESSAGE.WHATSAPP.WAPPI.QUEUE.add(
            value
            if isinstance(value, Message)
            else Message(
                value,
                recipient,
                EnumTool.get(sender),
            )
        )
    return SGB.MESSAGE.WHATSAPP.WAPPI.send(
        recipient, SGB.DATA.FORMAT.whatsapp_message(value), sender
    )


def package_name(value: SERVICE_ROLE | ServiceDescriptionBase) -> nstr:
    standalone_name: nstr = A.D.get(value).standalone_name
    return None if n(standalone_name) else A.PTH_FCD_DIST.NAME(standalone_name)
