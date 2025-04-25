import isgb

import grpc

from dataclasses import dataclass
from contextlib import contextmanager
from sgb.consts.rpc import RPC as CONST_RPC
from sgb.collections import nint, nstr, nbool, Any, Callable
from sgb.tools.service import (
    ServiceTool,
    IRootSupporter,
    ServiceRoleTool,
    IServiceCollection,
)
from sgb.tools import (
    e,
    j,
    n,
    nl,
    nn,
    ne,
    j_p,
    OSTool,
    EnumTool,
    DataTool,
    FormatTool,
    BitMask as BM,
    ParameterList,
    ErrorableThreadPoolExecutor,
)

from sgb.service.collections import (
    Subscribtion,
    ServiceDescription,
    ServiceInformation,
    SubscribtionResult,
    SubscriberInformation,
    ServiceDescriptionBase,
    SubscribtionInformation,
)
from sgb.consts.errors import Error, ServiceIsNotStartedError
from sgb.consts import SUBSCRIBTION_TYPE
import sgb.rpc.rpcCommandCall_pb2 as pb2
from sgb.consts.date_time import DATE_TIME
import sgb.rpc.rpcCommandCall_pb2_grpc as pb2_grpc
from sgb.service.consts import SERVICE_COMMAND as SC, SERVICE_ROLE

import grpc
import psutil
import socket
import atexit
import asyncio
from grpc import Server
from grpc import StatusCode
from threading import Thread
from typing import Any, Callable
from collections import defaultdict
from datetime import datetime, timedelta
from zeroconf import ServiceInfo, Zeroconf
from zeroconf import Zeroconf, ServiceBrowser, ServiceListener

DEBUG: bool = False

STUB: ServiceDescription = ServiceDescription(name="Stub")

USE_MDNS_SERVICE_DISCOVERING_DEFAULT_VALUE: bool = True


def cleanup():
    mDNS.close()


atexit.register(cleanup)


class DH:
    ROOT: IRootSupporter | None = None


def GRPC_OPTIONS() -> list[tuple[str, int]]:
    size: int = 20 * 1024 * 1024
    return [
        ("grpc.max_receive_message_length", size),
        ("grpc.max_send_message_length", size),
    ]


class IService:

    def serve(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
        call_handler: Callable[[SC | str, ParameterList, Any], Any] | None = None,
        starts_handler: Callable[[Any], None] | Callable[[], None] | None = None,
        max_workers: nint = None,
        as_standalone: bool = False,
        show_output: bool = True,
        admin_service_available: bool = True,
        use_mdns: nbool = None,
    ) -> None:
        raise NotImplemented()

    def create_subscribtions(
        self, information: ServiceDescriptionBase | None = None
    ) -> None:
        raise NotImplemented()

    @property
    def subscribtions(self) -> list[SubscribtionInformation]:
        raise NotImplemented()

    def stop(self) -> Server:
        raise NotImplemented()

    def subscribe_on(
        self,
        service_object: ServiceDescriptionBase | SERVICE_ROLE | None,
        service_command: SC | str,
        type: int = SUBSCRIBTION_TYPE.ON_RESULT,
        name: nstr = None,
    ) -> bool:
        raise NotImplemented()

    def unsubscribe(
        self, commnad_list: list[SC | str] | None = None, type: nint = None
    ) -> bool:
        raise NotImplemented()

    @property
    def description(self) -> ServiceDescription:
        raise NotImplemented()

    @property
    def information(self) -> ServiceInformation:
        raise NotImplemented()


@dataclass
class SessionInformation:
    start_time: datetime | None = None
    life_time: timedelta | None = None


class mDNSServiceListener(ServiceListener):

    def __init__(self):
        self.block = asyncio.Event()
        self.found_service: dict = None

    def add_service(self, zeroconfig: Zeroconf, service_type: str, name: str) -> None:
        if not self.block.is_set():
            info = zeroconfig.get_service_info(service_type, name)
            if info:
                self.found_service = {
                    "name": name,
                    "ip": socket.inet_ntoa(info.addresses[0]),
                    "port": info.port,
                    "type": service_type,
                    "properties": info.decoded_properties,
                }
                self.block.set()


class mDNS:

    zeroconf: Zeroconf | None = None

    @staticmethod
    def find_service(
        service_description: ServiceDescription,
    ) -> ServiceDescription | None:

        async def discover_first_service(service_type, timeout=10):
            zeroconf = Zeroconf()
            listener: mDNSServiceListener = mDNSServiceListener()
            browser: ServiceBrowser = ServiceBrowser(zeroconf, service_type, listener)
            try:
                await asyncio.wait_for(listener.block.wait(), timeout)
                return listener.found_service
            except asyncio.TimeoutError:
                return None
            finally:
                zeroconf.close()

        async def discover_service(
            service_description: ServiceDescription,
        ) -> ServiceDescription | None:
            service_role: SERVICE_ROLE = ServiceRoleTool.get(service_description)
            service_type: str = j_p(
                (
                    j(
                        (
                            "_",
                            OSTool.domain(),
                            "-",
                            service_role.name.lower(),
                        )
                    ),
                    "_tcp",
                    "local",
                    "",
                )
            )
            service = await discover_first_service(service_type)
            if service:
                return DataTool.fill_data_from_source(
                    ServiceDescription(),
                    service["properties"],
                    skip_not_none=True,
                )
            else:
                return None

        return asyncio.run(discover_service(service_description))

    @staticmethod
    def close() -> None:
        if nn(mDNS.zeroconf):
            mDNS.zeroconf.unregister_all_services()
            mDNS.zeroconf.close()

    @staticmethod
    def register_service(service_description: ServiceDescription) -> None:
        service_type: str = j_p(
            (
                j(
                    (
                        "_",
                        OSTool.domain(),
                        "-",
                        service_description.standalone_name,
                    )
                ),
                "_tcp",
                "local",
                "",
            )
        )
        service_info = ServiceInfo(
            service_type,
            j_p(
                (
                    service_description.description,
                    service_type,
                )
            ),
            addresses=[socket.inet_aton(OSTool.host_ip())],
            port=service_description.port,
            properties=DataTool.to_data(service_description) or {},
            server=OSTool.host(),
        )

        # Регистрируем сервис
        mDNS.zeroconf = Zeroconf()
        mDNS.zeroconf.register_service(service_info)


class ServiceClient:

    server: Server | None = None

    context: grpc.RpcContext | None = None

    service: IService | None = None

    service_description: ServiceDescription | None = None

    service_information: ServiceInformation | None = None

    session_information: SessionInformation = SessionInformation()

    def __init__(
        self,
        root: IRootSupporter | None = None,
        use_mdns_service_discovering: bool = USE_MDNS_SERVICE_DISCOVERING_DEFAULT_VALUE,
    ):
        self.service_collection: IServiceCollection = ServiceCollection()
        self.use_mdns_service_discovering = use_mdns_service_discovering
        if nn(root):
            DH.ROOT = root
        self.admin_service_available: nbool = None

    
    def create_error(self, context, message: str = "", code: Any = None) -> Any:
        context.set_details(message)
        context.set_code(code)
        return pb2.rpcCommandResult()

    def get_host(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> nstr:
        service_description: ServiceDescriptionBase | None = (
            ServiceRoleTool.service_description(service_object)
        )
        if isinstance(service_description, ServiceDescription):
            if ne(service_description.port):
                return FormatTool.domain(OSTool.domain_dns(), service_description.host)
        value: nstr = (
            self.get_information(service_object) or ServiceDescriptionBase()
        ).host or service_description.host
        if n(value):
            return value
        return value  # FormatTool.domain(DH.ROOT.domain_dns, value)

    
    def check_on_availability(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
        cached: bool = False,
    ) -> bool:
        return ne(self.get_information(service_object, cached))

    def get_information_from_cache(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> ServiceInformation | None:
        return self.service_collection.get(
            ServiceRoleTool.service_description(service_object)
        )

    def get_port(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> nint:
        service_description: ServiceDescriptionBase | None = (
            ServiceRoleTool.service_description(service_object)
        )
        if isinstance(service_description, ServiceDescription):
            if ne(service_description.port):
                return service_description.port
        return (
            self.get_information(service_object) or ServiceDescriptionBase()
        ).port or service_description.port

    def get_information(
        self, service_object: SERVICE_ROLE | ServiceDescriptionBase, cached: bool = True
    ) -> ServiceInformation | None:
        service_description: ServiceDescriptionBase | None = (
            ServiceRoleTool.service_description(service_object)
        )
        if e(self.service_collection.get()):
            self.service_collection.request(self)
        service_description = self.get_information_from_cache(service_description)
        if cached:
            return service_description
        # if e(service_description):
        #    return None
        return self.ping(service_object)

    def get_service_information_list(self) -> list[ServiceInformation]:
        return DataTool.map(
            ServiceTool.extract_service_information,
            DataTool.rpc_decode(
                self.call_service(
                    None,
                    SC.get_service_information_list,
                    ((self.service_information or STUB).name),
                )
            )
            or [],
        )

    def ping(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
    ) -> ServiceInformation | None:
        try:
            service_information: ServiceDescriptionBase = (
                ServiceRoleTool.service_description(service_object)
            )
            value = DataTool.fill_data_from_rpc_str(
                ServiceInformation(),
                self.call_service(
                    service_information,
                    SC.ping,
                    ((self.service_information or STUB).name),
                ),
            )
            return value
        except Error:
            return None

    def call_service_command(
        self, command: SC | str, parameters: Any = None, timeout: nint = None
    ) -> nstr:
        return self.call_service(None, command, parameters, timeout)

    def call_service(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase | None,
        command: SC | str,
        parameters: Any = None,
        timeout: nint = None,
    ) -> nstr:

        service_description: ServiceDescriptionBase = (
            (ServiceRoleTool.service_description(service_object))
            if nn(service_object)
            else DH.ROOT.description_by_service_command(command)
        )
        try:
            service_host: nstr = self.get_host(service_description)
            if n(service_host):
                if self.use_mdns_service_discovering:
                    mdns_service_description: ServiceDescription | None = (
                        mDNS.find_service(service_description)
                    )
                    if nn(mdns_service_description):
                        service_description = mdns_service_description
                        self.service_collection.update(service_description, add=True)
                        service_host = service_description.host
                if n(service_host):
                    error: ServiceIsNotStartedError = ServiceIsNotStartedError(
                        "Service is not started"
                    )
                    code: StatusCode = StatusCode.UNAVAILABLE
                    details: str = j(
                        (
                            "Service role name: ",
                            service_description.name,
                            nl(),
                            "Command: ",
                            command,
                            nl(),
                            "Details: ",
                            error.details,
                            nl(),
                            "Code: ",
                            code,
                        )
                    )
                    DH.ROOT.error_handler(
                        service_description, error, code, details, command
                    )
                    raise error
            service_port: nint = self.get_port(service_description)
            if e(timeout):
                if (
                    e(self.service_information)
                    or self.service_information.isolated
                    or service_description.isolated
                ):
                    if command == SC.ping:
                        timeout = CONST_RPC.TIMEOUT_FOR_PING
                    else:
                        timeout = CONST_RPC.TIMEOUT
            return (
                CommandClient(service_host, service_port)
                .call_command(
                    command.name if isinstance(command, SC) else command,
                    DataTool.rpc_encode(parameters),
                    timeout,
                )
                .data
            )
        except grpc.RpcError as error:
            code: tuple = error.code()
            details: str = j(
                (
                    "Service role name: ",
                    service_description.name,
                    nl(),
                    "Host: ",
                    service_host,
                    ":",
                    service_port,
                    nl(),
                    "Command: ",
                    command,
                    nl(),
                    "Details: ",
                    error.details(),
                    nl(),
                    "Code: ",
                    code,
                )
            )
            DH.ROOT.error_handler(service_description, error, code, details, command)
            # raise Error(error.details(), code)

    def create_service(self) -> IService:
        return Service(self)


class UnaryServicer(pb2_grpc.UnaryServicer):
    def __init__(
        self,
        service: IService,
        client: ServiceClient,
        description: ServiceDescription,
        call_handler: Callable[[str, ParameterList, Any], Any] | None = None,
        *args,
        **kwargs,
    ):
        self.service_information = description
        self.call_handler = call_handler
        self.service = service
        self.client = client
        self.subscriber_information_map: dict[str, dict[str, SubscriberInformation]] = (
            defaultdict(dict)
        )

    def internal_call_handler(self, sc: SC | str, parameters: Any, context) -> Any:
        try:
            parameter_list: ParameterList = ParameterList(parameters)
            if ne(sc):
                if sc == SC.stop_service:
                    is_subscriber: bool = ServiceTool.is_service_as_listener(
                        self.service_information
                    )
                    if not is_subscriber:
                        self.client.call_service(
                            SC.on_service_stops, self.service_information
                        )
                    self.service.stop()
                    if not is_subscriber:
                        pid: int = OSTool.pid()
                        parent = psutil.Process(pid)
                        for child in parent.children(recursive=True):
                            child.kill()
                    return
                if sc == SC.ping:
                    return DataTool.fill_data_from_source(
                        ServiceInformation(), self.service_information
                    )
                if sc == SC.subscribe:
                    return self.subscribe_with_parameter_list(parameter_list)
                if sc == SC.unsubscribe:
                    return self.unsubscribe_with_parameter_list(parameter_list)
                if sc == SC.create_subscribtions:
                    self.service.create_subscribtions(
                        parameter_list.next(ServiceDescriptionBase())
                    )
                    return True
                if sc == SC.update_service_information:
                    self.client.service_collection.update(
                        parameter_list.next_as_list(ServiceInformation),
                        parameter_list.next(),
                    )
                    return True
                if sc == SC.heart_beat:
                    date_string: str = ServiceTool.extract_parameter_list(
                        parameter_list
                    ).get()
                    date: datetime = datetime.strptime(
                        date_string, DATE_TIME.ISO_DATETIME_FORMAT
                    )
                    parameter_list.set(0, date)
                    self.client.session_information.life_time = (
                        date - self.client.session_information.start_time
                    )
            return (
                None
                if e(self.call_handler)
                else self.call_subscribers_after(
                    sc,
                    parameter_list,
                    self.call_handler(
                        sc,
                        self.call_subscribers_before(sc, parameter_list),
                        context,
                    ),
                )
            )
        except Exception as exception:
            DH.ROOT.error_detect_handler(exception)

    def unsubscribe_all(self) -> None:

        def unsubscribe_all_internal() -> None:
            for sc in self.subscriber_information_map:
                for service_information_name in self.subscriber_information_map[sc]:
                    subscriber_information: SubscriberInformation = (
                        self.subscriber_information_map[sc][service_information_name]
                    )
                    DataTool.rpc_decode(
                        self.client.call_service(
                            subscriber_information.service_information,
                            SC.unsubscribe,
                            (sc, subscriber_information.name),
                        )
                    )
            self.subscriber_information_map = defaultdict(dict)

        Thread(target=unsubscribe_all_internal).start()

    def unsubscribe_with_parameter_list(self, value: ParameterList) -> None:
        description: ServiceDescription = value.next(ServiceDescription())
        role_description_name: str = description.name
        for service_command in self.subscriber_information_map:
            if (
                role_description_name
                in self.subscriber_information_map[service_command]
            ):
                del self.subscriber_information_map[service_command][
                    role_description_name
                ]

    def subscribe_with_parameter_list(self, pl: ParameterList) -> bool:
        service_information: ServiceDescriptionBase = pl.next(ServiceDescriptionBase())
        subscribtion_information: SubscribtionInformation = pl.next(
            SubscribtionInformation()
        )
        subscribtion_information.service_command = EnumTool.get(
            SC, subscribtion_information.service_command
        ) or subscribtion_information.service_command
        return self.subscribe(service_information, subscribtion_information)

    def subscribe(
        self,
        service_description: ServiceDescription,
        subscribtion_information: SubscribtionInformation,
    ) -> bool:
        sc: SC | str = subscribtion_information.service_command
        name: nstr = subscribtion_information.name
        type: int = subscribtion_information.type
        if sc in self.subscriber_information_map:
            if service_description.name in self.subscriber_information_map[sc]:
                subscriber_information: SubscriberInformation = (
                    self.subscriber_information_map[sc][service_description.name]
                )
                if (
                    subscriber_information.service_information == service_description
                    and BM.has(subscriber_information.type, type)
                ):
                    self.subscriber_information_map[sc][service_description.name] = (
                        SubscriberInformation(
                            type, name, service_information=service_description
                        )
                    )
            else:
                self.subscriber_information_map[sc][service_description.name] = (
                    SubscriberInformation(
                        type, name, service_information=service_description
                    )
                )
        else:
            self.subscriber_information_map[sc][service_description.name] = (
                SubscriberInformation(
                    type, name, service_information=service_description
                )
            )
        return True

    def call_subscribers_before(self, sc: SC | str, in_result: ParameterList):
        out_result: ParameterList = in_result
        if sc in self.subscriber_information_map:
            for service_information_name in list(self.subscriber_information_map[sc]):
                subscriber_information: SubscriberInformation = (
                    self.subscriber_information_map[sc][service_information_name]
                )
                service_information: ServiceInformation = (
                    subscriber_information.service_information
                )
                if (
                    BM.has(subscriber_information.type, SUBSCRIBTION_TYPE.ON_CALL)
                    and subscriber_information.enabled
                ):
                    subscriber_information.available = self.client.check_on_availability(
                        service_information
                    )
                    if subscriber_information.available:
                        out_result = ParameterList(
                            DataTool.rpc_decode(
                                self.client.call_service(
                                    service_information,
                                    sc,
                                    (
                                        in_result,
                                        SubscribtionResult(
                                            None,
                                            SUBSCRIBTION_TYPE.ON_CALL,
                                            True,
                                        ),
                                    ),
                                )
                            )
                        )
                    else:
                        del self.subscriber_information_map[sc][
                            service_information_name
                        ]
        return out_result

    def call_subscribers_after(
        self, sc: SC | str, parameter_list: ParameterList, result: Any
    ) -> Any:

        def internal_call_subscribers_after_sequentially(
            command: SC | str,
            subscriber_list: list[SubscriberInformation],
            parameter_list: ParameterList,
            result: Any,
        ):
            for subscriber in subscriber_list:
                role_description_item: ServiceDescription = (
                    subscriber.service_information
                )
                subscriber.available = self.client.check_on_availability(
                    role_description_item
                )
                if subscriber.available:
                    result = self.client.call_service(
                        role_description_item,
                        command,
                        (
                            parameter_list,
                            SubscribtionResult(
                                result,
                                SUBSCRIBTION_TYPE.ON_RESULT_SEQUENTIALLY,
                                True,
                            ),
                        ),
                    )
                else:
                    if DataTool.if_is_in(
                        self.subscriber_information_map[command],
                        role_description_item.name,
                    ):
                        del self.subscriber_information_map[command][
                            role_description_item.name
                        ]

        def internal_call_subscribers_after(
            sc: SC | str,
            subscriber_information: SubscriberInformation,
            parameter_list: ParameterList,
            result: Any,
        ):
            service_information: ServiceDescriptionBase = (
                subscriber_information.service_information
            )
            subscriber_information.available = self.client.check_on_availability(
                service_information
            )
            if subscriber_information.available:
                self.client.call_service(
                    service_information,
                    sc,
                    (
                        parameter_list,
                        SubscribtionResult(result, SUBSCRIBTION_TYPE.ON_RESULT, True),
                    ),
                )
            else:
                if service_information.name in self.subscriber_information_map[sc]:
                    del self.subscriber_information_map[sc][service_information.name]

        if sc in self.subscriber_information_map:
            after_sequentially_subscriber_information_list: list[
                SubscriberInformation
            ] = []
            for servce_information_name in list(self.subscriber_information_map[sc]):
                subscriber_information: SubscriberInformation = (
                    self.subscriber_information_map[sc][servce_information_name]
                )
                if subscriber_information.enabled:
                    if BM.has(subscriber_information.type, SUBSCRIBTION_TYPE.ON_RESULT):
                        Thread(
                            target=internal_call_subscribers_after,
                            args=(
                                sc,
                                subscriber_information,
                                parameter_list,
                                result,
                            ),
                        ).start()
                    elif BM.has(
                        subscriber_information.type,
                        SUBSCRIBTION_TYPE.ON_RESULT_SEQUENTIALLY,
                    ):
                        after_sequentially_subscriber_information_list.append(
                            subscriber_information
                        )
            if ne(after_sequentially_subscriber_information_list):
                Thread(
                    target=internal_call_subscribers_after_sequentially,
                    args=(
                        sc,
                        after_sequentially_subscriber_information_list,
                        parameter_list,
                        result,
                    ),
                ).start()

        return result

    def rpcCallCommand(self, command_object, context):

        parameters: Any = command_object.parameters

        if ne(parameters):
            parameters = DataTool.rpc_decode(parameters)
        ServiceClient.context = context

        command: SC | nstr = EnumTool.get(SC, command_object.name)
        if n(command):
            command = command_object.name
        result: Any = self.internal_call_handler(command, parameters, context)
        if n(context.code()):
            return pb2.rpcCommandResult(data=DataTool.rpc_encode(result))
        return result


class CommandClient:
    def __init__(self, host: str, port: int):
        self.stub = pb2_grpc.UnaryStub(
            grpc.insecure_channel(
                j((host, port), ":"),
                options=GRPC_OPTIONS(),
                # compression=grpc.Compression.Gzip,
            )
        )

    def call_command(self, name: str, parameters: nstr = None, timeout: nint = None):
        return self.stub.rpcCallCommand(
            pb2.rpcCommand(name=name, parameters=parameters), timeout=timeout
        )


class ServiceCollection(IServiceCollection):

    service_collection: dict[ServiceDescriptionBase, ServiceInformation] = {}

    def request(self, client: ServiceClient) -> None:
        self.update(
            client.get_service_information_list(),
            True,
            True,
        )

    def remove_service(self, value: ServiceDescriptionBase) -> None:
        if value in self.service_collection:
            del self.service_collection[value]

    def clear(self) -> None:
        self.service_collection = {}

    def get(
        self,
        key_description: ServiceDescription | None = None,
    ) -> dict[ServiceDescriptionBase, ServiceInformation] | ServiceInformation | None:
        return (
            (
                self.service_collection[key_description]
                if key_description in self.service_collection
                else None
            )
            if nn(key_description)
            else self.service_collection
        )

    def update(
        self,
        value: ServiceDescriptionBase | list[ServiceDescriptionBase],
        add: bool = True,
        overwrite: bool = False,
    ) -> None:
        if not isinstance(value, list):
            value = [value]
        if overwrite:
            if ne(value):
                self.service_collection = {}
        for item in value:
            if add:
                self.service_collection[item] = item
            else:
                if item in self.service_collection:
                    del self.service_collection[item]


class Service(IService):

    MAX_WORKERS: int = 10

    def __init__(self, client: ServiceClient) -> None:
        self.client = client
        self._description: ServiceDescription | None = None
        self._information: ServiceInformation | None = None
        self.subscribtions_map: dict[
            ServiceDescriptionBase, dict[str, Subscribtion]
        ] = defaultdict(dict)
        self.server: Server | None = None

    @property
    def description(self) -> ServiceDescription:
        return self._description

    @property
    def information(self) -> ServiceInformation:
        return self._information

    @contextmanager
    def detect_error(self):
        try:
            yield True
        except Exception as exception:
            DH.ROOT.error_detect_handler(exception)
        finally:
            pass

    def serve(
        self,
        service_object: SERVICE_ROLE | ServiceDescriptionBase,
        call_handler: Callable[[SC | str, ParameterList, Any], Any] | None = None,
        starts_handler: Callable[[IService], None] | Callable[[], None] | None = None,
        max_workers: nint = None,
        as_standalone: bool = False,
        show_output: bool = True,
        admin_service_available: bool = True,
        use_mdns: nbool = None,
    ) -> None:
        self.client.admin_service_available = admin_service_available
        max_workers = max_workers or Service.MAX_WORKERS
        service_description: ServiceDescription = (
            service_object
            if isinstance(service_object, ServiceDescriptionBase)
            else ServiceRoleTool.service_description(service_object)
        )
        self._description = service_description
        with self.detect_error():
            if not ServiceTool.is_service_as_listener(service_description):
                DH.ROOT.add_isolated_arg()
                isolate_arg: nstr = None
                try:
                    isolated_arg_value: nstr = DH.ROOT.isolated_arg()
                    if nn(isolated_arg_value):
                        isolate_arg = str(isolated_arg_value).lower()
                except AttributeError as error:
                    pass
                if nn(isolate_arg):
                    if n(self.description.isolated):
                        self.description.isolated = isolate_arg not in [
                            "0",
                            "no",
                            "false",
                        ]
                    elif self.description.isolated:
                        self.description.isolated = isolate_arg not in [
                            "0",
                            "no",
                            "false",
                        ]
        self.description.host = ServiceTool.create_host(self.description)
        self.description.port = ServiceTool.create_port(self.description)
        self._information = DataTool.fill_data_from_source(
            ServiceInformation(standalone=as_standalone),
            self.description,
            skip_not_none=True,
        )
        self.information.pid = OSTool.pid()
        if e(self.client.service):
            self.client.service_description = self.description
            self.client.service_information = self.information
            self.client.service = self
        self.server = grpc.server(
            ErrorableThreadPoolExecutor(max_workers=max_workers),
            options=GRPC_OPTIONS(),
            # compression=grpc.Compression.Gzip,
        )
        if show_output:
            DH.ROOT.service_header(self.information)
        pb2_grpc.add_UnaryServicer_to_server(
            UnaryServicer(self, self.client, self.description, call_handler),
            self.server,
        )
        try:
            self.server.add_insecure_port(
                j((self.description.host, self.description.port), ":")
            )

            self.server.start()
            self.client.session_information.start_time = datetime.now().replace(
                second=0, microsecond=0
            )
            if nn(starts_handler):
                starts_handler(self)
            self.information.subscribtions = self.subscribtions
            if admin_service_available:
                self.client.call_service_command(
                    SC.on_service_starts, (self.information,)
                )
            else:
                self.create_subscribtions()
            if not admin_service_available or use_mdns:
                mDNS.register_service(self.description)
            self.server.wait_for_termination()
        except RuntimeError as error:
            DH.ROOT.service_was_not_started(self.description, j(error.args))

    def create_subscribtions(
        self, information: ServiceDescriptionBase | None = None
    ) -> None:
        def internal_create_subscribtion(
            subscribtions: dict[ServiceDescriptionBase, dict[SC | str, Subscribtion]],
            information: ServiceDescriptionBase,
        ):
            for sc in subscribtions[information]:
                subscription: Subscribtion = subscribtions[information][sc]
                self.client.call_service(
                    information,
                    SC.subscribe,
                    (
                        DataTool.fill_data_from_source(
                            ServiceDescriptionBase(), self.information
                        ),
                        DataTool.fill_data_from_source(
                            SubscribtionInformation(), subscription
                        ),
                    ),
                )
                subscription.available = True
                subscription.enabled = True

        for description_item in (
            self.subscribtions_map if e(information) else [information]
        ):
            if self.client.check_on_availability(description_item):
                internal_create_subscribtion(self.subscribtions_map, description_item)

    @property
    def subscribtions(self) -> list[Subscribtion]:
        result: list[Subscribtion] = []
        for description_item in self.subscribtions_map:
            for sc in self.subscribtions_map[description_item]:
                result.append(self.subscribtions_map[description_item][sc])
        return result

    def subscribe_on(
        self,
        service_object: ServiceDescriptionBase | SERVICE_ROLE | None,
        service_command: SC | str,
        type: int = SUBSCRIBTION_TYPE.ON_RESULT,
        name: nstr = None,
    ) -> bool:
        service_description: ServiceDescription | None = (ServiceRoleTool.service_description(service_object) if nn(service_object) else None) or (
            DH.ROOT.description_by_service_command(service_command)
        ) or ServiceRoleTool.service_description(SERVICE_ROLE.ROUTER)
        if ne(service_description):
            if service_description != self.description:
                subscribtion: Subscribtion | None = None
                if service_command not in self.subscribtions_map[service_description]:
                    subscribtion = Subscribtion(service_description.name, service_command, type, name)
                    self.subscribtions_map[service_description][
                        service_command
                    ] = subscribtion
                else:
                    subscribtion = self.subscribtions_map[service_description][
                        service_command
                    ]
                    subscribtion.type |= type
                subscribtion.available = self.client.check_on_availability(
                    service_description
                )
                if self.client.admin_service_available:
                    return subscribtion.available
                else:
                    return subscribtion.available
        return False

    def unsubscribe(
        self, command_list: list[SC | str] | None = None, type: nint = None
    ) -> None:

        for service_description in self.subscribtions_map:
            for sc in self.subscribtions_map[service_description]:
                if sc in command_list:
                    DataTool.rpc_decode(
                        self.client.call_service(
                            service_description, "unsubscribe", (self.description,)
                        )
                    )

    def unsubscribe_all(
        self, service_object: SERVICE_ROLE | ServiceDescriptionBase
    ) -> bool:
        pass
        # return self.unsubscribe(service_object)

    def stop(self) -> None:
        self.server.stop(0)
