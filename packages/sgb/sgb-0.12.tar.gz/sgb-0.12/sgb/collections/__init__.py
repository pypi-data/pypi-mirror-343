import isgb

from enum import Enum
from collections import namedtuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta, date
from typing import Any, Tuple, List, Callable, TypeVar, Generic, TypeAlias

strtuple: TypeAlias = tuple[str, ...]
strlist: TypeAlias = list[str]
strdict: TypeAlias = dict[str, Any]
nbool: TypeAlias = bool | None
nstr: TypeAlias = str | None
nint: TypeAlias = int | None
nfloat: TypeAlias = float | None


@dataclass
class Host:
    name: str
    ip: nstr = None
    description: nstr = None

    @staticmethod
    def name(value: Any) -> str:
        return value.name if isinstance(value, Host) else value

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, another):
        return False if another is None else (self.name == another.name)

@dataclass
class ZabbixHost:
    id: nstr = None
    name: nstr = None
    host: nstr = None


@dataclass
class IOTDevice:
    name: nstr = None
    id: nstr = None
    key: nstr = None
    mac: nstr = None
    uuid: nstr = None
    sn: nstr = None
    category: nstr = None
    product_name: nstr = None
    product_id: nstr = None
    biz_type: nint = None


@dataclass
class IOTDeviceStatusProperty:
    code: nstr = None
    name: nstr = None
    type: nstr = None
    unit: nstr = None


@dataclass
class IOTDeviceStatusIntegerProperty(IOTDeviceStatusProperty):

    min: int | nfloat = None
    max: int | nfloat = None
    scale: int | nfloat = None
    step: int | nfloat = None


@dataclass
class IOTDeviceStatusValue:
    code: nstr = None
    value: Any = None


@dataclass
class IOTDeviceStatus:
    timestamp: int = 0
    values: tuple[IOTDeviceStatusValue, ...] | None = None


@dataclass
class ZabbixMetricsValue:
    value: Any | None = None
    clock: datetime | nint = None


@dataclass
class ZabbixMetrics:
    itemid: nint = None
    type: int = 0
    snmp_oid: nstr = None
    hostid: int = 0
    name: nstr = None
    key_: nstr = None
    delay: nstr = None
    history: nstr = None
    trends: nstr = None
    status: int = 0
    value_type: int = 0
    trapper_hosts: strtuple | None = None
    units: nstr = None
    formula: nstr = None
    logtimefmt: nstr = None
    templateid: int = 0
    valuemapid: int = 0
    params: strtuple | None = None
    ipmi_sensor: nstr = None
    flags: int = 0
    interfaceid: int = 0
    description: nstr = None
    inventory_link: int = 0
    lifetime: nstr = None
    evaltype: int = 0
    jmx_endpoint: nstr = None
    master_itemid: int = 0
    timeout: nstr = None
    url: nstr = None
    query_fields: strtuple | None = None
    posts: nstr = None
    status_codes: int = 0
    follow_redirects: int = 0
    lastclock: datetime | None = None
    lastvalue: Any = None
    prevvalue: Any = None


@dataclass
class PasswordSettings:
    length: int
    special_characters: str
    order_list: strlist
    special_characters_count: int
    alphabets_lowercase_count: int
    alphabets_uppercase_count: int
    digits_count: int = 1
    shuffled: bool = False


@dataclass
class NameCaption:
    name: nstr
    caption: nstr = None


@dataclass
class NameCaptionDescription(NameCaption):
    description: nstr = None


@dataclass
class OrderedNameCaptionDescription(NameCaptionDescription):
    order: nint = None


@dataclass
class IconedOrderedNameCaptionDescription(OrderedNameCaptionDescription):
    icon: nstr = None


@dataclass
class ParamItem(NameCaptionDescription):
    optional: bool = False

    visible: bool = True
    saved: bool = True
    key: bool = False

    def configurate(
        self,
        visible: nbool = None,
        saved: nbool = None,
        key: nbool = None,
    ) -> Any:
        result: ParamItem = ParamItem(
            self.name, self.caption, self.description, self.optional
        )
        if visible is not None:
            result.visible = visible
        if saved is not None:
            result.saved = saved
        if key is not None:
            result.key = key
        return result


@dataclass
class FieldItem:
    name: nstr = None
    caption: nstr = None
    visible: bool = True
    class_type: Any | None = None
    default_value: nstr = None
    data_formatter: str | Callable[[Any], str] = "{data}"


class FieldItemList:
    list: list[FieldItem]

    def copy_field_item(self, value: FieldItem) -> FieldItem:
        return FieldItem(
            value.name,
            value.caption,
            value.visible,
            value.class_type,
            value.default_value,
            value.data_formatter,
        )

    def __init__(self, *args):
        self.list = []
        arg_list = list(args)
        for arg_item in arg_list:
            if isinstance(arg_item, FieldItem):
                item: FieldItem = self.copy_field_item(arg_item)
                self.list.append(item)
            elif isinstance(arg_item, FieldItemList):
                for item in arg_item.list:
                    self.list.append(self.copy_field_item(item))
            elif isinstance(arg_item, list):
                self.list.extend(arg_item)

    def get_list(self) -> list[FieldItem]:
        return self.list

    def get_item_and_index_by_name(self, value: str) -> Tuple[FieldItem, int]:
        index: int = -1
        result: FieldItem | None = None
        for item in self.list:
            index += 1
            if item.name == value:
                result = item
                break
        return result, -1 if result is None else index

    def get_item_by_name(self, value: str) -> FieldItem:
        result, _ = self.get_item_and_index_by_name(value)
        return result

    def position(self, name: str, position: int):
        _, index = self.get_item_and_index_by_name(name)
        if index != -1:
            self.list.insert(position, self.list.pop(index))
        return self

    def get_name_list(self):
        return list(map(lambda item: str(item.name), self.list))

    def get_caption_list(self):
        return list(
            map(lambda x: str(x.caption), filter(lambda y: y.visible, self.list))
        )

    def visible(self, name: str, value: bool):
        item, _ = self.get_item_and_index_by_name(name)
        if item is not None:
            item.visible = value
        return self

    def caption(self, name: str, value: bool):
        item, _ = self.get_item_and_index_by_name(name)
        if item is not None:
            item.caption = value
        return self

    def length(self) -> int:
        return len(self.list)


T = TypeVar("T")
R = TypeVar("R")


@dataclass
class Result(Generic[T]):
    fields: FieldItemList | None = None
    data: T | None = None

    def __len__(self):
        return len(self.data)

    def sort(self, key: None = None, reverse: bool = False) -> None:
        if key is None and self.data is not None and len(self.data) > 1:
            if isinstance(self.data[0], Uniq):
                key = lambda item: item.get_uniq_field()
        self.data.sort(key=key, reverse=reverse)

    def __eq__(self, value):
        return super().__eq__(value)

    def __operand_plus__(self, value):
        if (
            isinstance(value, Result)
            and isinstance(self.data, list)
            and isinstance(value.data, list)
        ):
            if len(value.data) > 0:
                if isinstance(value.data[0], Uniq):
                    cache: dict[str, bool] = {
                        item.get_uniq_field(): True for item in self.data
                    }
                    for item in value.data:
                        if not cache.get(item.get_uniq_field()):
                            self.data.append(item)
                            cache[item.get_uniq_field()] = True
                else:
                    self.data += value.data

        if self.data is None:
            self.data = value.data
        self.fields = value.fields
        return self

    def __iadd__(self, value):
        # self.data = self.data or []
        return self.__operand_plus__(value)

    def __add__(self, value):
        return self.__operand_plus__(value)


@dataclass
class FullName:
    last_name: str = ""
    first_name: str = ""
    middle_name: str = ""

    def as_list(self) -> strlist:
        return [self.last_name, self.first_name, self.middle_name]


@dataclass
class ADContainer:
    name: nstr = None
    description: nstr = None
    distinguishedName: nstr = None


@dataclass
class User(ADContainer):
    samAccountName: nstr = None
    mail: nstr = None
    telephoneNumber: nstr = None
    userAccountControl: nint = None

    @property
    def login(self) -> str:
        return self.samAccountName


Rect = namedtuple("Rect", ["left", "top", "width", "height"])


@dataclass
class IndicationDevice:
    name: nstr = None
    description: nstr = None
    ip_address: tuple[str, int] | None = None


@dataclass
class MailboxInfo:
    timestamp: datetime | None = None
    last_uid: nstr = None


@dataclass
class NewMailMessage:
    mailbox_address: nstr = None
    subject: nstr = None
    text: nstr = None
    from_: nstr = None


@dataclass
class RecipientWaitingForInput:
    group_name: nstr = None
    timeout: nint = None
    recipient: nstr = None
    timestamp: datetime | None = None


@dataclass
class BarcodeInformation:
    data: nstr = None
    type: nstr = None
    rect: Rect | None = None


@dataclass
class EmailInformation:
    email: nstr = None
    person_pin: int = 0
    person_name: nstr = None


@dataclass
class InaccesableEmailInformation(EmailInformation):
    workstation_name: nstr = None
    registrator_person_name: nstr = None


@dataclass
class CardRegistryFolderPosition:
    ChartFolder: nstr = None
    p_a: int = 0
    p_b: int = 0
    p_c: int = 0


@dataclass
class ActionValue:
    caption: str
    value: str


@dataclass
class LoginPasswordPair:
    login: nstr = None
    password: nstr = None


@dataclass
class OGRN:
    name: nstr = None
    code: nstr = None
    data: dict | None = None


from abc import ABC, abstractmethod


class Uniq(ABC):

    @abstractmethod
    def get_uniq_field(self) -> Any:
        pass


@dataclass
class ComputerDescription(Host, Uniq):
    #name: nstr = None
    properties: int = 0
    #description: nstr = None
    distinguishedName: nstr = None

    def get_uniq_field(self) -> str:
        return self.name


@dataclass
class Computer(ComputerDescription):
    samAccountName: nstr = None
    accessable: bool = False

    @property
    def login(self) -> str:
        return self.samAccountName


@dataclass
class Server(Computer):
    pass


@dataclass
class Workstation(Computer):
    pass


@dataclass
class ResourceDescription:
    address: nstr = None
    name: nstr = None
    inaccessibility_check_values: tuple[int, ...] = (2, 20, 15)


@dataclass
class ResourceDescriptionDelegated(ResourceDescription):
    delegator: nstr = None


@dataclass
class ZabbixResourceDescription(ResourceDescription):
    zabbix_host_name: nstr = None

    def get_zabbix_host_name(self) -> str:
        return self.zabbix_host_name or self.address


@dataclass
class ZabbixResourceDescriptionDelegated(
    ZabbixResourceDescription, ResourceDescriptionDelegated
):
    pass


@dataclass
class SiteResourceDescription(ResourceDescription):
    check_certificate_status: bool = False
    check_free_space_status: bool = False
    driver_name: nstr = None
    internal: bool = False


class IResourceStatus:
    pass


@dataclass
class ResourceStatus(ResourceDescription, IResourceStatus):
    accessable: nbool = None
    inaccessibility_counter: int = 0
    inaccessibility_counter_total: int = 0


@dataclass
class WSResourceStatus(ResourceStatus):
    pass


@dataclass
class ServerResourceStatus(ResourceStatus):
    pass


@dataclass
class DiskStatistics:
    name: nstr = None
    free_space: nint = None
    size: nint = None


@dataclass
class DisksStatisticsStatus(IResourceStatus):
    host: nstr = None
    disk_list: list[DiskStatistics] = field(default_factory=list)


@dataclass
class SiteResourceStatus(ResourceStatus, SiteResourceDescription):
    certificate_status: nstr = None
    free_space_status: nstr = None


@dataclass
class MarkPerson:
    FullName: nstr = None
    TabNumber: nstr = None


@dataclass
class MarkPersonDivision(MarkPerson):
    DivisionName: nstr = None
    DivisionID: nint = None


@dataclass
class TemporaryMark(MarkPerson):
    OwnerTabNumber: nstr = None


@dataclass
class PolibasePersonBase:
    pin: nint = None
    FullName: nstr = None
    telephoneNumber: nstr = None


@dataclass
class PolibasePerson(PolibasePersonBase):
    Birth: datetime | None = None
    Comment: nstr = None
    ChartFolder: nstr = None
    email: nstr = None
    barcode: nstr = None
    registrationDate: datetime | None = None
    telephoneNumber2: nstr = None
    telephoneNumber3: nstr = None
    telephoneNumber4: nstr = None


@dataclass
class PolibaseNote:
    emailed: nstr = None


@dataclass
class PolibasePersonVisitDS(PolibasePersonBase):
    id: nint = None
    registrationDate: nstr = None
    beginDate: str | datetime | None = None
    completeDate: str | datetime | None = None
    status: nint = None
    cabinetID: nint = None
    doctorID: nint = None
    doctorFullName: nstr = None
    serviceGroupID: nint = None
    comment: nstr = None


@dataclass
class CardRegistryFolderStatistics:
    name: nstr = None
    count: int = 0


@dataclass
class PolibasePersonVisitSearchCritery:
    vis_no: Any | None = None
    vis_pat_no: Any | None = None
    vis_pat_name: Any | None = None
    vis_place: Any | None = None
    vis_reg_date: Any | None = None
    vis_date_ps: Any | None = None
    vis_date_pf: Any | None = None
    vis_date_fs: Any | None = None
    vis_date_ff: Any | None = None


@dataclass
class PolibasePersonVisitNotificationDS:
    visitID: nint = None
    messageID: nint = None
    type: nint = None


@dataclass
class EventDS:
    name: nstr = None
    parameters: strdict | None = None
    timestamp: datetime | date | str | nint = None
    id: int = 0


@dataclass
class Message:
    message: nstr = None
    recipient: nstr = None
    sender: nstr = None
    image_url: nstr = None
    location: tuple[float, float] | None = None


@dataclass
class DelayedMessage(Message):
    date: Any | None = None
    type: nint = None


@dataclass
class DelayedMessageDS(DelayedMessage):
    id: nint = None
    status: nint = None


@dataclass
class MessageSearchCritery:
    id: Any | None = None
    recipient: nstr = None
    date: datetime | nstr = None
    type: Any | None = None
    status: nint = None
    sender: nstr = None


@dataclass
class PolibasePersonNotificationConfirmation:
    recipient: nstr = None
    sender: nstr = None
    status: int = 0


@dataclass
class PolibasePersonVisitNotification(
    PolibasePersonVisitDS, PolibasePersonVisitNotificationDS
):
    pass


@dataclass
class PolibasePersonVisit(PolibasePersonVisitDS):
    registrationDate: datetime | None = None
    beginDate: datetime | None = None
    completeDate: datetime | None = None
    beginDate2: datetime | None = None
    completeDate2: datetime | None = None
    Comment: nstr = None


@dataclass
class PolibasePersonQuest:
    step: nint = None
    stepConfirmed: nbool = None
    timestamp: nint = None


@dataclass
class PolibasePersonInformationQuest(PolibasePersonBase):
    confirmed: nint = None
    errors: nint = None


@dataclass
class PolibasePersonReviewQuest(PolibasePersonQuest):
    beginDate: nstr = None
    completeDate: nstr = None
    grade: nint = None
    message: nstr = None
    informationWay: nint = None
    feedbackCallStatus: nint = None


@dataclass
class MarkGroup:
    GroupName: nstr = None
    GroupID: nint = None


@dataclass
class Mark(MarkPersonDivision, MarkGroup):
    pID: nint = None
    mID: nint = None
    Comment: nstr = None
    telephoneNumber: nstr = None
    type: nint = None


@dataclass
class PersonDivision:
    id: nint = None
    name: nstr = None


@dataclass
class TimeTrackingEntity(MarkPersonDivision):
    TimeVal: nstr = None
    Mode: nint = None


@dataclass
class TimeTrackingResultByDate:
    date: nstr = None
    enter_time: nstr = None
    exit_time: nstr = None
    duration: nint = None


@dataclass
class TimeTrackingResultByPerson:
    tab_number: nstr = None
    full_name: nstr = None
    duration: int = 0
    list: List[TimeTrackingResultByDate] = field(default_factory=list)


@dataclass
class WhatsAppMessage:
    message: nstr = None
    from_me: nbool = None
    sender: nstr = None
    recipient: nstr = None
    profile_id: nstr = None
    time: nint = None
    chatId: nstr = None
    flags: nint = None
    return_result_key: nstr = None
    args: tuple[Any, ...] | None = None


@dataclass
class WhatsAppMessagePayload:
    title: str
    body: str


@dataclass
class WhatsAppMessageListPayload(WhatsAppMessagePayload):
    btn_text: str
    list: dict


@dataclass
class WhatsAppMessagebButton:
    body: nstr = None
    id: nstr = None


@dataclass
class WhatsAppMessageButtonsPayload(WhatsAppMessagePayload):
    buttons: list[WhatsAppMessagebButton] | None = None


@dataclass
class TimeTrackingResultByDivision:
    name: str
    list: List[TimeTrackingResultByPerson] = field(default_factory=list)


@dataclass
class RobocopyJobDescription:
    name: nstr = None
    start_cron_string: nstr = None
    host: nstr = None
    run_from_system_account: bool = False
    run_with_elevetion: bool = False
    live: bool = False
    exclude: bool = False

    def clone(
        self,
        job_name: str,
        start_cron_string: nstr = None,
        host: nstr = None,
        live: nbool = None,
        exclude: bool = False,
    ):
        return RobocopyJobDescription(
            job_name,
            start_cron_string,
            host or self.host,
            self.run_from_system_account,
            self.run_with_elevetion,
            self.live if live is None else live,
            self.exclude if exclude is None else exclude,
        )


@dataclass
class RobocopyJobItem(RobocopyJobDescription):
    source: nstr = None
    destination: nstr = None


@dataclass
class RobocopyJobStatus:
    name: nstr = None
    source: nstr = None
    destination: nstr = None
    active: bool = False
    last_started: nstr = None
    last_created: nstr = None
    last_status: nint = None
    live: bool = False
    pid: int = -1
    exclude: bool = False


@dataclass
class PrinterADInformation:
    driverName: nstr = None
    adminDescription: nstr = None
    description: nstr = None
    portName: nstr = None
    serverName: nstr = None
    name: nstr = None


@dataclass
class IndicationsContainer:
    timestamp: datetime | None = None


@dataclass
class HumidityIndicationsValue:
    humidity: nfloat = None


@dataclass
class TemparatureIndicationsValue:
    temperature: nfloat = None


@dataclass
class TemperatureAndHumidityIndicationsValue(
    HumidityIndicationsValue, TemparatureIndicationsValue
):
    pass


@dataclass
class ChillerIndicationsValue(TemparatureIndicationsValue):
    indicators: int = 0


@dataclass
class ChillerIndicationsValueContainer(ChillerIndicationsValue, IndicationsContainer):
    pass


@dataclass
class CTIndicationsValue(TemperatureAndHumidityIndicationsValue):
    pass


@dataclass
class CTIndicationsValueContainer(CTIndicationsValue, IndicationsContainer):
    pass


@dataclass
class GKeepItem:
    name: nstr = None
    title: nstr = None
    id: nstr = None


@dataclass
class File:
    title: nstr = None
    text: nstr = None
    id: nstr = None


@dataclass
class Note(File):
    images: strlist | None = None


@dataclass
class InventoryReportItem:
    name: str | nint = None
    inventory_number: nstr = None
    row: nstr = None
    quantity: nint = None
    name_column: nint = None
    inventory_number_column: nint = None
    quantity_column: nint = None


@dataclass
class PrinterStatus:
    ip: nstr = None
    description: nstr = None
    variant: nstr = None
    port: nint = None
    community: nstr = None
    accessable: nbool = None


@dataclass
class TimeSeriesStatistics:
    count: int = 0
    values: list[datetime] | None = None
    distance: list[timedelta] | None = None
    min: nint = None
    max: nint = None
    avg: nint = None


@dataclass
class PrinterReport(PrinterStatus):
    name: nstr = None
    model: nstr = None
    serial: nint = None
    adminDescription: nstr = None
    meta: nstr = None
    printsOverall: nint = None
    printsColor: nint = None
    printsMonochrome: nint = None
    fuserType: nint = None
    fuserCapacity: nint = None
    fuserRemaining: nint = None
    wasteType: nint = None
    wasteCapacity: nint = None
    wasteRemaining: nint = None
    cleanerType: nint = None
    cleanerCapacity: nint = None
    cleanerRemaining: nint = None
    transferType: nint = None
    transferCapacity: nint = None
    transferRemaining: nint = None
    blackTonerType: nstr = None
    blackTonerCapacity: nint = None
    blackTonerRemaining: nint = None
    cyanTonerType: nint = None
    cyanTonerCapacity: nint = None
    cyanTonerRemaining: nint = None
    magentaTonerType: nint = None
    magentaTonerCapacity: nint = None
    magentaTonerRemaining: nint = None
    yellowTonerType: nint = None
    yellowTonerCapacity: nint = None
    yellowTonerRemaining: nint = None
    blackDrumType: nstr = None
    blackDrumCapacity: nint = None
    blackDrumRemaining: nint = None
    cyanDrumType: nint = None
    cyanDrumCapacity: nint = None
    cyanDrumRemaining: nint = None
    magentaDrumType: nint = None
    magentaDrumCapacity: nint = None
    magentaDrumRemaining: nint = None
    yellowDrumType: nint = None
    yellowDrumCapacity: nint = None
    yellowDrumRemaining: nint = None

    def get_toner(self, color: str) -> int:
        color = color.lower()
        remaining: int
        capacity: int
        if color == "c":
            remaining = self.cyanTonerRemaining
            capacity = self.cyanTonerCapacity
        if color == "m":
            remaining = self.magentaTonerRemaining
            capacity = self.magentaTonerCapacity
        if color == "y":
            remaining = self.yellowTonerRemaining
            capacity = self.yellowTonerCapacity
        if color == "k":
            remaining = self.blackTonerRemaining
            capacity = self.blackTonerCapacity
        try:
            if remaining == -1 or capacity == -1:
                return -1
            if remaining == -404 or capacity == -404:
                return -404
            if remaining == -401 or capacity == -401:
                return -401
            return int(round((int(remaining) / int(capacity)) * 100))
        except:
            return -1

    def get_drum(self, color: str) -> int:
        color = color.lower()
        if color == "c":
            remaining = self.cyanDrumRemaining
            capacity = self.cyanDrumCapacity
        if color == "m":
            remaining = self.magentaDrumRemaining
            capacity = self.magentaDrumCapacity
        if color == "y":
            remaining = self.yellowDrumRemaining
            capacity = self.yellowDrumCapacity
        if color == "k":
            remaining = self.blackDrumRemaining
            capacity = self.blackDrumCapacity
        try:
            if remaining == -1 or capacity == -1:
                return -1
            if remaining == -404 or capacity == -404:
                return -404
            if remaining == -401 or capacity == -401:
                return -401
            return int(round((int(remaining) / int(capacity)) * 100))
        except:
            return -1


@dataclass
class MarkGroupStatistics(MarkGroup):
    Comment: nstr = None
    Count: nint = None


@dataclass
class EventDescription:
    message: str | Callable[[tuple[Any, ...] | list[Any]], str] | None = None
    channel: Enum | None = None
    flags: int | tuple[Enum, ...] | Enum | None = None
    params: tuple[ParamItem, ...] | None = None


@dataclass
class ActionDescription:
    name: nstr = None
    alias: strtuple | None = None
    description: nstr = None
    question: nstr = None
    confirm: bool = True
    silence: bool = False
    parameters_description: nstr = None
    # parameters_default: tuple[str] | None = None
    forcable: bool = False
    forced_description: nstr = None


@dataclass
class ActionWasDone:
    action_description: nstr = None
    action: Enum | nstr = None
    user_name: nstr = None
    user_login: nstr = None
    parameters: list[Any] | None = None
    forced: bool = False


@dataclass
class ServerRoleItem:
    name: nstr = None
    alias: nstr = None


@dataclass
class StorageVariableHolder:
    key_name: nstr = None
    default_value: nstr = None
    description: nstr = None
    auto_init: bool = True
    # only for get
    section: nstr = None


@dataclass
class ExpiredTimestampVariableHolder:
    timestamp: nstr = None
    life_time: nstr = None
    resolver_note: nstr = None


@dataclass
class IntStorageVariableHolder(StorageVariableHolder):
    default_value: int = 0


@dataclass
class VariantableStorageVariable:
    variants: tuple[Any, ...] | None = None


@dataclass
class IntVariantableStorageVariableHolder(
    VariantableStorageVariable, IntStorageVariableHolder
):
    variants: tuple[int, ...] | None = None


@dataclass
class MinIntStorageVariableHolder(IntStorageVariableHolder):
    min_value: int = 0


@dataclass
class IntStorageVariableHolderWithMin(IntStorageVariableHolder):
    min_value: int = 0


@dataclass
class IntListStorageVariableHolder(StorageVariableHolder):
    default_value: list[int] | None = None


@dataclass
class FloatStorageVariableHolder(StorageVariableHolder):
    default_value: nfloat = None


@dataclass
class BoolStorageVariableHolder(StorageVariableHolder):
    default_value: nbool = None


@dataclass
class TimeStorageVariableHolder(StorageVariableHolder):
    default_value: nstr = None


@dataclass
class DateListStorageVariableHolder(StorageVariableHolder):
    default_value: strtuple | None = None


@dataclass
class StringListStorageVariableHolder(StorageVariableHolder):
    default_value: strtuple | None = None


@dataclass
class PolibaseDocument:
    file_path: nstr = None
    polibase_person_pin: nint = None
    document_type: nstr = None


@dataclass
class MedicalDirectionDocument:
    number: nint = None
    date: datetime | None = None
    person_name: nstr = None
    person_ensurence_number: nstr = None
    person_ensurence_agent: nstr = None
    person_birthday: datetime | nstr = None
    research_type: Enum | nstr = None
    research_code: nstr = None
    ogrn_number: nstr = None


@dataclass
class Titled:
    title: str


@dataclass
class ThresholdedText(Titled):
    threshold: float


@dataclass
class PolibaseDocumentDescription(ThresholdedText):
    title_top: int = 0
    title_height: int = 0
    page_count: int = 1


@dataclass
class DocumentDescription(ThresholdedText):
    left: float
    top: float
    right: float
    bottom: float


@dataclass
class MedicalResearchType:
    title_list: strtuple | None = None
    alias: nstr = None


@dataclass
class DirectoryInfo:
    value: nstr = None
    confirmed_file_list: list[tuple[str, float]] | None = None
    last_created_file_timestamp: nfloat = None


@dataclass
class JournalRecord:
    # from sgb.const import JournalType, Tags
    timestamp: datetime | None = None
    applicant_user: User | None = None
    type: Any | None = None
    tag: Any | None = None
    title: nstr = None
    text: nstr = None
    parameters: strdict | None = None


@dataclass
class BonusInformation:
    bonus_all: float = 0
    money_all: float = 0
    bonus_spent_all: float = 0
    bonus_active: float = 0
    money_last: float = 0
    bonus_last_spent: float = 0
    bonus_last: float = 0


@dataclass
class WappiStatus:

    app_status: nstr = None
    authorized: bool = False
    authorized_at: nstr = None
    checked_at: nstr = None
    last_activity: float = 0
    logouted_at: nstr = None
    message_count: int = 0
    name: nstr = None
    payment_expired_at: nstr = None
    payment_notification: bool = False
    phone: nstr = None
    profile_id: nstr = None
    proxy: nstr = None
    uuid: nstr = None
    webhook_types: strtuple = ()
    webhook_url: nstr = None
    worked_days: int = 0


class IClosable:
    def close(self) -> None:
        raise NotImplemented()
    
@dataclass
class UsernameAndPassword:

    username: nstr = None
    password: nstr = None
