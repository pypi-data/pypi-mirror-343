import isgb

from abc import ABC, abstractmethod


from sgb.consts.ad import AD
from sgb.consts import PYTHON
from sgb.service.client import ServiceClient
from sgb.consts.errors import NotFound, ERROR
from sgb.service.interface import ClientBase, IClientBase
from sgb.consts.service import SERVICE_ROLE, SERVICE_COMMAND as SC
from sgb.tools import (
    n,
    ne,
    e,
    nn,
    j_s,
    one,
    DataTool,
    CheckTool,
    ResultTool,
    FormatTool,
    StringTool,
)

from sgb.collections import (
    Any,
    nstr,
    User,
    nint,
    nbool,
    Result,
    strlist,
    Callable,
    FullName,
    Computer,
    Workstation,
    ADContainer,
    ComputerDescription,
)

SR = SERVICE_ROLE.AD


class IResultUserClient(IClientBase, ABC):

    @abstractmethod
    def admins(self) -> Result[list[User]]:
        pass

    @abstractmethod
    def by_dn(self, value: str) -> Result[list[User]]:
        pass

    @abstractmethod
    def by_login(
        self,
        value: str,
        active: nbool = None,
        cached: nbool = None,
        raise_on_empty_result: bool = True,
    ) -> Result[User]:
        pass

    @abstractmethod
    def by_login_pattern(
        self,
        value: str,
        active: nbool = None,
        cached: nbool = None,
        raise_on_empty_result: bool = True,
    ) -> Result[list[User]]:
        pass

    @abstractmethod
    def by_internal_telephone_number(
        self,
        value: str,
        active: nbool = None,
        raise_on_empty_result: bool = True,
    ) -> Result[list[User]]:
        pass

    @abstractmethod
    def by_workstation_name(
        self,
        value: str,
        raise_on_empty_result: bool = True,
    ) -> Result[User]:
        pass

    @abstractmethod
    def by_any(
        self, value: Any, active: nbool = None, raise_on_empty_result: bool = True
    ) -> Result[list[User]]:
        pass

    @abstractmethod
    def by_group_name(self, value: str) -> Result[list[User]]:
        pass

    @abstractmethod
    def template_list(self) -> Result[list[User]]:
        pass

    @abstractmethod
    def containers(self) -> Result[list[ADContainer]]:
        pass

    @abstractmethod
    def by_full_name(
        self, value: FullName, get_first: bool = False, active: nbool = None
    ) -> Result[list[User] | User]:
        pass

    @abstractmethod
    def by_name(
        self,
        value: str,
        active: nbool = None,
        cached: nbool = None,
        strict_comparison: bool = False,
        raise_on_empty_result: bool = True,
    ) -> Result[list[User]]:
        pass

    @abstractmethod
    def all(self, active: nbool = None) -> Result[list[User]]:
        pass

    @abstractmethod
    def list_with_telephone_number(
        self,
        active: nbool = None,
    ) -> Result[list[User]]:
        pass

    """
    @abstractmethod
    def by_tab_number(self, value: str | int) -> Result[User]:
        pass

    @abstractmethod
    def by_mark(self, value: Mark) -> Result[User]:
        pass"
    """


class ICheckUserClient(IClientBase, ABC):

    @abstractmethod
    def authenticated(login: str, timeout: nint = None) -> bool:
        pass

    @abstractmethod
    def exists_by_login(self, value: str) -> bool:
        pass


class IActionUserClient(IClientBase, ABC):

    @abstractmethod
    def authenticate(login: str, password: str) -> bool:
        pass


class IResultComputerClient(IClientBase, ABC):

    @abstractmethod
    def by_container_dn(
        self, value: nstr = None, class_type: Any = Computer
    ) -> Result[list[Computer]]:
        pass

    @abstractmethod
    def all_description_by_container_dn(
        self,
        value: str,
    ) -> Result[list[ComputerDescription]]:
        pass

    @abstractmethod
    def by_parameter(
        self,
        value: str,
        parameter_getter: Callable[[Computer], str],
        parameter_name: str,
        container_dn: nstr = None,
        class_type: Any = Computer,
        raise_on_empty_result: bool = True,
    ) -> Result[Computer]:
        pass

    @abstractmethod
    def by_name(
        self,
        value: str,
        container_dn: nstr = None,
        class_type: Any = Computer,
        raise_on_empty_result: bool = True,
    ) -> Result[Computer]:
        pass

    @abstractmethod
    def by_description(
        self,
        value: str,
        container_dn: nstr = None,
        class_type: Any = Computer,
        raise_on_empty_result: bool = True,
    ) -> Result[Computer]:
        pass


class IResultWorkstationClient(IClientBase, ABC):

    @abstractmethod
    def all_description(self) -> Result[list[ComputerDescription]]:
        pass

    @abstractmethod
    def by_login(
        self, value: str, raise_on_empty_result: bool = True
    ) -> Result[list[Workstation]]:
        pass

    @abstractmethod
    def any(self, value: int | str | User | None) -> Result[list[Workstation]]:
        pass

    @abstractmethod
    def by_user_name(self, value: str) -> Result[list[Workstation]]:
        pass

    @abstractmethod
    def by_name(
        self,
        value: str,
        raise_on_empty_result: bool = True,
    ) -> Result[Workstation]:
        pass

    @abstractmethod
    def all(self) -> Result[list[Workstation]]:
        pass


class IActionWorkstationClient(IClientBase, ABC):

    @abstractmethod
    def reboot(self, host: nstr = None, force: bool = False) -> bool:
        pass

    @abstractmethod
    def shutdown(self, host: nstr = None, force: bool = False) -> bool:
        pass

    @abstractmethod
    def kill_process(
        self, name_or_pid: str | int, host: str, via_standart_tools: bool = True
    ) -> bool:
        pass

    @abstractmethod
    def kill_python_process(self, host: str, via_standart_tools: bool = False) -> bool:
        pass


class IChecWorkstationClient(ABC):

    pass


class ADAction(ClientBase):

    def call(
        self,
        command: SC | str,
        parameters: tuple[
            Any,
            ...,
        ],
    ) -> Any:
        return super().call(SR, command, parameters)


class ADResult(ClientBase):

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


class ComputerClient(ClientBase):

    class RESULT(IResultComputerClient, ADResult, ADAction):

        def by_container_dn(
            self, value: nstr = None, class_type: Any = Computer
        ) -> Result[list[Computer]]:
            return self.call_for_result("get_computer_list", (value,), class_type)

        def all_description_by_container_dn(
            self, value: str
        ) -> Result[list[ComputerDescription]]:
            return self.call_for_result(
                "get_computer_description_list", (value,), ComputerDescription
            )

        def by_parameter(
            self,
            value: str,
            parameter_getter: Callable[[Computer], str],
            parameter_name: str,
            container_dn: nstr = None,
            class_type: Any = Computer,
            raise_on_empty_result: bool = True,
        ) -> Result[Computer]:
            value = FormatTool.string(value).lower().split(".")[0]
            result: Result[Workstation] = ResultTool.filter(
                lambda item: StringTool.full_intersection_by_tokens(
                    parameter_getter(item), value
                ),
                self.by_container_dn(container_dn, class_type),
            )
            if raise_on_empty_result and e(result):
                raise ERROR.WORKSTATION.create_not_found_error(parameter_name, value)
            return result

        def by_name(
            self,
            value: str,
            container_dn: nstr = None,
            class_type: Any = Computer,
            raise_on_empty_result: bool = True,
        ) -> Result[Computer]:
            return self.by_parameter(
                value,
                lambda computer: computer.name,
                "именем",
                container_dn,
                class_type,
                raise_on_empty_result,
            )

        def by_description(
            self,
            value: str,
            container_dn: nstr = None,
            class_type: Any = Computer,
            raise_on_empty_result: bool = True,
        ) -> Result[Computer]:
            return self.by_parameter(
                value,
                lambda computer: computer.description,
                "описанием",
                container_dn,
                class_type,
                raise_on_empty_result,
            )


class WorkstationClient(ClientBase):

    class CHECK:

        pass

    class ACTION(IActionWorkstationClient, ADAction):

        def reboot(self, host: nstr = None, force: bool = False) -> bool:
            return self.call("reboot", (host, force))

        def shutdown(self, host: nstr = None, force: bool = False) -> bool:
            return self.call("shutdown", (host, force))

        def kill_process(
            self, name_or_pid: str | int, host: str, via_standart_tools: bool = True
        ) -> bool:
            return self.call(
                "kill_process",
                (name_or_pid, host, via_standart_tools),
            )

        def kill_python_process(
            self, host: str, via_standart_tools: bool = False
        ) -> bool:
            return self.kill_process(PYTHON.EXECUTOR, host, via_standart_tools)

        def connect(self, client_ip: str, host: nstr = None) -> bool:
            return self.call("connect", (client_ip, host))

    class RESULT(IResultWorkstationClient, ADResult):

        def __init__(
            self,
            dn: str,
            user_result_client: IResultUserClient,
            user_check_client: ICheckUserClient,
            computer_client: IResultComputerClient,
            service_client: ServiceClient | None = None,
        ):
            super().__init__(service_client)
            self.dn = dn
            self.user_result_client = user_result_client
            self.user_check_client = user_check_client
            self.computer_result = computer_client

        def all_description(self) -> Result[list[ComputerDescription]]:
            return self.computer_result.all_description_by_container_dn(self.dn)

        def by_login(
            self, value: str, raise_on_empty_result: bool = True
        ) -> Result[list[Workstation]]:
            if self.user_check_client.exists_by_login(value):
                workstation_list_result: Result[list[Workstation]] = (
                    self.call_for_result(
                        "get_workstation_list_by_user_login", value, Workstation
                    )
                )
                workstation_name_collection: strlist = []

                def filter_function(worksatation: Workstation) -> bool:
                    worksatation_name: str = worksatation.name
                    if worksatation_name not in workstation_name_collection:
                        workstation_name_collection.append(worksatation_name)
                        return True
                    return False

                return ResultTool.filter(filter_function, workstation_list_result)
            else:
                if raise_on_empty_result:
                    raise ERROR.USER.create_not_found_error("логином", True, value)
                return Result(None, None)

        def any(
            self, value: int | str | User | None
        ) -> Result[list[Workstation]] | None:
            if n(value):
                return self.all()
            user_result: Result[list[User]] = self.user_result_client.by_any(
                value, True, raise_on_empty_result=False
            )
            result: Result[list[Workstation]] = Result()
            if ne(user_result):
                result += ResultTool.map(
                    lambda user: self.by_login(user.login, raise_on_empty_result=False),
                    user_result,
                )
            result += self.by_name(value, False)
            result += self.by_description(value, False)
            return result

        def by_user_name(self, value: str) -> Result[list[Workstation]]:
            return ResultTool.map(
                lambda user: self.by_login(user.login),
                self.user_result_client.by_name(value),
            )

        def by_name(
            self, value: str, raise_on_empty_result: bool = True
        ) -> Result[Workstation]:
            try:
                return self.computer_result.by_name(
                    value, self.dn, Workstation, raise_on_empty_result
                )
            except NotFound as _:
                raise ERROR.WORKSTATION.create_not_found_error("именем", value)

        def by_description(
            self, value: str, raise_on_empty_result: bool = True
        ) -> Result[Workstation]:
            try:
                return self.computer_result.by_description(
                    value, self.dn, Workstation, raise_on_empty_result
                )
            except NotFound as _:
                raise ERROR.WORKSTATION.create_not_found_error("описанием", value)

        def all(self) -> Result[list[Workstation]]:
            return self.computer_result.by_container_dn(self.dn, Workstation)


class UserClient(ClientBase):

    class ACTION(IActionUserClient, ADAction):

        def authenticate(self, login: str, password: str):
            return self.call("authenticate", (login, password))

    class CHECK(ADAction):

        def authenticated(self, login: str, timeout: nint = None) -> bool:
            return self.call("is_authenticated", (login, timeout))

        def exists_by_login(self, value: str) -> bool:
            return self.call("check_user_exists_by_login", value)

    class RESULT(IResultUserClient, ADResult):

        def admins(self) -> Result[list[User]]:
            return self.by_dn(AD.ADMINS_CONTAINER_DN)

        def by_dn(self, value: str) -> Result[list[User]]:
            return self.call_for_result("get_user_list_by_dn", (value,), User)

        def by_property(self, value: AD.UserProperies) -> Result[list[User]]:
            return self.call_for_result(
                "get_user_list_by_property", (value.name,), User
            )

        def by_login(
            self,
            value: str,
            active: nbool = None,
            cached: nbool = None,
            raise_on_empty_result: bool = True,
        ) -> Result[User]:
            try:
                return ResultTool.with_first_item(
                    self.by_login_pattern(value, active, cached, raise_on_empty_result)
                )
            except NotFound as _:
                raise ERROR.USER.create_not_found_error("логином", active, value)

        def by_login_pattern(
            self,
            value: str,
            active: nbool = None,
            cached: nbool = None,
            raise_on_empty_result: bool = True,
        ) -> Result[list[User]]:
            result: Result[list[User]] = self.call_for_result(
                "get_user_by_login", (value, active, cached), User
            )
            if raise_on_empty_result and e(result, not_none=True):
                raise ERROR.USER.create_not_found_error(
                    "шаблоном логина", active, value
                )
            return result

        def by_internal_telephone_number(
            self,
            value: str,
            active: nbool = None,
            raise_on_empty_result: bool = True,
        ) -> Result[list[User]]:
            result: Result[User] = self.call_for_result(
                "get_user_by_telephone_number", (value, active), User
            )
            if raise_on_empty_result and e(result):
                raise ERROR.USER.create_not_found_error(
                    "номером телефона", active, value
                )
            return result

        def by_workstation_name(
            self,
            value: str,
            raise_on_empty_result: bool = True,
        ) -> Result[User]:
            value = value.lower()
            user_workstation: Workstation = one(
                self.call_for_result(
                    "get_user_by_workstation",
                    (value,),
                    Workstation,
                )
            )
            if e(user_workstation):
                if raise_on_empty_result:
                    raise ERROR.WORKSTATION.create_not_found_error("именем", value)
                else:
                    return Result()
            if e(user_workstation.login):
                if raise_on_empty_result:
                    raise NotFound(
                        j_s(
                            ("За компьютером", value, "нет залогиненного пользователя")
                        ),
                        value,
                    )
                else:
                    return Result()
            return self.by_login(user_workstation.login)

        def by_any(
            self, value: Any, active: nbool = None, raise_on_empty_result: bool = True
        ) -> Result[list[User]]:
            if isinstance(value, FullName):
                return self.by_full_name(value, False, active)
            elif isinstance(value, (ComputerDescription, Workstation)):
                return self.by_any(value.name, active)
            elif isinstance(value, str):

                class DH:
                    result: Result[list[User]] | None = None

                def init_or_add(
                    value_getter: Callable[[], Result[list[User]]],
                ) -> None:
                    value: Result[list[User]] = value_getter()
                    if nn(value):
                        if n(DH.result):
                            DH.result = value
                        else:
                            DH.result += value

                if CheckTool.decimal(value):
                    init_or_add(
                        lambda: self.by_internal_telephone_number(
                            value, raise_on_empty_result=False
                        )
                    )
                init_or_add(
                    lambda: self.by_login_pattern(
                        value, active, raise_on_empty_result=False
                    )
                )
                init_or_add(
                    lambda: self.by_name(value, active, raise_on_empty_result=False)
                )
            if raise_on_empty_result and e(DH.result):
                raise ERROR.USER.create_not_found_error(
                    "поисковым значением", active, value
                )
            return DH.result

        def by_group_name(self, value: str) -> Result[list[User]]:
            return DataTool.to_result(
                self.call("get_user_list_by_group", value),
                User,
            )

        def template_list(self) -> Result[list[User]]:
            return DataTool.to_result(self.call("get_template_users"), User)

        def containers(self) -> Result[list[ADContainer]]:
            return DataTool.to_result(self.call("get_containers"), ADContainer)

        def by_full_name(
            self, value: FullName, get_first: bool = False, active: nbool = None
        ) -> Result[list[User] | User]:
            return DataTool.to_result(
                self.call("get_user_by_full_name", (value, active)),
                User,
                get_first,
            )

        def by_name(
            self,
            value: str,
            active: nbool = None,
            cached: nbool = None,
            strict_comparison: bool = False,
            raise_on_empty_result: bool = True,
        ) -> Result[list[User]]:
            result: Result[list[User]] = self.call_for_result(
                "get_user_list_by_name",
                (value, active, cached, strict_comparison),
                User,
            )
            if raise_on_empty_result and e(result):
                raise ERROR.USER.create_not_found_error("именем", active, value)
            return result

        def all(self, active: nbool = None) -> Result[list[User]]:
            return self.by_name(None, active)

        def list_with_telephone_number(
            self,
            active: nbool = None,
        ) -> Result[list[User]]:
            def user_with_telephone_number(user: User) -> bool:
                return SGB.CHECK.telephone_number(user.telephoneNumber)

            return ResultTool.filter(
                lambda user: user_with_telephone_number(user),
                self.all(active),
            )

        """
        def by_tab_number(self, value: str | int) -> Result[User]:
            result: Result[Mark] = SGB.RESULT.MARK.by_tab_number(value)
            if e(result):
                raise NotFound(j_s(("Карта доступа с номером", value, "не найдена")))
            return self.by_mark(result.data)

        def by_mark(self, value: Mark) -> Result[User]:
            return Result(
                FIELD_COLLECTION.AD.USER,
                DataTool.check(
                    value,
                    lambda: DataTool.get_first_item(
                        self.by_full_name(
                            FullNameTool.fullname_from_string(value.FullName)
                        ).data
                    ),
                ),
            )
        """
