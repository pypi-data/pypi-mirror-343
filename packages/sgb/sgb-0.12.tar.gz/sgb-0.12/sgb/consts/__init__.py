from enum import Enum, auto, IntEnum

from sgb.tools import j
from sgb.consts import *
from sgb.consts.names import *
from sgb.consts.paths import *
from sgb.collections import (
    MedicalResearchType,
    MinIntStorageVariableHolder,
    OrderedNameCaptionDescription,
    IconedOrderedNameCaptionDescription,
)
from sgb.consts.password import *
from sgb.consts.date_time import *

VERSION: str = "0.12"


class DATA:
    # deprecated
    class EXTRACTOR:
        USER_NAME_FULL: str = "user_name_full"
        USER_NAME: str = "user_name"
        AS_IS: str = "as_is"

    class FORMATTER(Enum):
        MY_DATETIME = "my_datetime"
        MY_DATE = "my_date"


class BARCODE:
    CODE128: str = "code128"
    I25: str = "i25"


class FONT:
    pass


class SessionFlags(IntEnum):
    CLI = 512
    OUTSIDE = 8192


class SESSION_TYPE:
    MOBILE: str = "mobile"
    OUTSIDE: str = "outside"
    WEB: str = "web"


class POWERSHELL:
    NAME: str = "powershell"
    EXECUTOR: str = NAME


class PSTOOLS:
    NAME: str = "pstools"
    PS_EXECUTOR: str = "psexec"
    PS_KILL_EXECUTOR: str = "pskill"
    PS_PING: str = "psping"

    COMMAND_LIST: list[str] = [
        PS_KILL_EXECUTOR,
        "psfile",
        "psgetsid",
        "psinfo",
        "pslist",
        "psloggedon",
        "psloglist",
        "pspasswd",
        PS_PING,
        "psservice",
        "psshutdown",
        "pssuspend",
    ]

    NO_BANNER: str = "-nobanner"
    ACCEPTEULA: str = "-accepteula"


class WINDOWS_MSG:
    NAME: str = "msg"
    EXECUTOR: str = NAME


class EmailVerificationMethods(IntEnum):
    NORMAL = auto()
    ABSTRACT_API = auto()
    DEFAULT = ABSTRACT_API


class ROBOCOPY:

    NAME: str = "robocopy"

    ERROR_CODE_START: int = 8

    STATUS_CODE: dict[int, str] = {
        0: "No errors occurred, and no copying was done. The source and destination directory trees are completely synchronized.",
        1: "One or more files were copied successfully (that is, new files have arrived).",
        2: "Some Extra files or directories were detected. No files were copied Examine the output log for details.",
        4: "Some Mismatched files or directories were detected. Examine the output log. Housekeeping might be required.",
        8: "Some files or directories could not be copied (copy errors occurred and the retry limit was exceeded). Check these errors further.",
        16: "Serious error. Robocopy did not copy any files. Either a usage error or an error due to insufficient access privileges on the source or destination directories.",
        3: "Some files were copied. Additional files were present. No failure was encountered.",
        5: "Some files were copied. Some files were mismatched. No failure was encountered.",
        6: "Additional files and mismatched files exist. No files were copied and no failures were encountered. This means that the files already exist in the destination directory",
        7: "Files were copied, a file mismatch was present, and additional files were present.",
    }


class CHARSETS:
    WINDOWS: str = "cp1251"
    WINDOWS_ALTERNATIVE: str = "cp866"
    UTF8: str = "utf-8"
    UTF16: str = "utf-16-le"


class INPUT_TYPE:
    NO: int = -1
    NORMAL: int = 0
    INDEX: int = 1
    QUESTION: int = 2


class WINDOWS:

    NAME: str = "Windows"

    PATH_SPLITTER: str = "\\"

    class ENVIROMENT_VARIABLES:
        PATH: str = "PATH"

    ENVIROMENT_COMMAND: str = "$Env"

    class CHARSETS:
        ALTERNATIVE: str = CHARSETS.WINDOWS_ALTERNATIVE

    class SERVICES:
        WIA: str = (
            "stisvc"  # Обеспечивает службы получения изображений со сканеров и цифровых камер
        )
        TASK_SCHEDULER: str = "schtasks"

    class PROCESSES:
        POWER_SHELL_REMOTE_SESSION: str = "wsmprovhost.exe"

    class PORT:
        SMB: int = 445
        SMB_UNTRUST: int = 139
        MSTSC: int = 3389


class CONST(DATE_TIME):

    EMAIL_SPLITTER: str = "@"
    DOMAIN_SPLITTER: str = EMAIL_SPLITTER

    SPLITTER: str = ":"
    NAME_SPLITTER: str = "_"
    UNKNOWN_VALUE: str = "?"

    class PORT:
        HTTP: int = 80
        HTTPS: int = 443
        SMTP: int = 587
        IMAP: int = 993
        SNMP: int = 161

    # in seconds
    HEART_BEAT_PERIOD: int = 60

    NEW_LINE: str = "\n"

    GROUP_PREFIX: str = "group:"
    TELEPHONE_PREFIX: str = "tel:"

    SITE_PROTOCOL: str = "https://"
    UNTRUST_SITE_PROTOCOL: str = "http://"

    INTERNATIONAL_TELEPHONE_NUMBER_PREFIX: str = "7"
    TELEPHONE_NUMBER_PREFIX: str = j(("+", INTERNATIONAL_TELEPHONE_NUMBER_PREFIX))
    INTERNAL_TELEPHONE_NUMBER_PREFIX: str = "тел."

    class CACHE:
        class TTL:
            # in seconds
            WORKSTATIONS: int = 60
            USERS: int = 300

    class ERROR:
        class WAPPI:
            PROFILE_NOT_PAID: int = 402

    class TIME_TRACKING:
        REPORT_DAY_PERIOD_DEFAULT: int = 15

    class MESSAGE:
        class WHATSAPP:
            SITE_NAME: str = "https://wa.me/"
            SEND_MESSAGE_TO_TEMPLATE: str = SITE_NAME + "{}?text={}"
            GROUP_SUFFIX: str = "@g.us"
            OUTSIDE_SUFFIX: str = "@outside"
            CLI_SUFFIX: str = "@cli"

            class GROUP(Enum):
                SGB_CLI = "120363163438805316@g.us"
                REGISTRATOR_CLI = "120363212130686795@g.us"
                RD = "79146947050-1595848245@g.us"
                MAIN = "79644300470-1447044803@g.us"
                EMAIL_CONTROL = "120363159605715569@g.us"
                CT_INDICATIONS = "120363084280723039@g.us"
                DOCUMENTS_WORK_STACK = "120363115241877592@g.us"
                REGISTRATION_AND_CALL = "79242332784-1447983812@g.us"
                DOCUMENTS_WORK_STACK_TEST = "120363128816931482@g.us"
                CONTROL_SERVICE_INDICATIONS = "120363159210756301@g.us"
                SCANNED_DOCUMENT_HELPER_CLI = "120363220286578760@g.us"

            class WAPPI:

                DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%SZ"
                NAME: str = "Wappi"
                DESCRIPTION: str = "Сервис по отправке сообщений"
                SEND: str = "send?"

                PROFILE_SUFFIX: str = "profile_id="
                URL_API: str = "https://wappi.pro/api"
                URL_API_SYNC: str = j((URL_API, "/sync"))
                URL_MESSAGE: str = j((URL_API_SYNC, "/message"))
                STATUS: str = j(
                    (j((URL_API_SYNC, "get", "status"), "/"), "?", PROFILE_SUFFIX)
                )
                URL_SEND_MESSAGE: str = j((URL_MESSAGE, "/", SEND, PROFILE_SUFFIX))
                URL_SEND_LOCATION: str = j(
                    (URL_MESSAGE, "/location/", SEND, PROFILE_SUFFIX)
                )
                URL_SEND_VIDEO: str = j((URL_MESSAGE, "/video/", SEND, PROFILE_SUFFIX))
                URL_SEND_IMAGE: str = j((URL_MESSAGE, "/img/", SEND, PROFILE_SUFFIX))
                URL_SEND_DOCUMENT: str = j(
                    (URL_MESSAGE, "/document/", SEND, PROFILE_SUFFIX)
                )
                URL_SEND_LIST_MESSAGE: str = j(
                    (URL_MESSAGE, "/list/", SEND, PROFILE_SUFFIX)
                )
                URL_SEND_BUTTONS_MESSAGE: str = j(
                    (URL_MESSAGE, "/buttons/", SEND, PROFILE_SUFFIX)
                )
                URL_GET_MESSAGES: str = j((URL_MESSAGE, "s/get?", PROFILE_SUFFIX))
                URL_GET_STATUS: str = j((URL_API_SYNC, "/get/status?", PROFILE_SUFFIX))
                CONTACT_SUFFIX: str = "@c.us"

                class Profiles(Enum):
                    IT = "e6706eaf-ae17"
                    CALL_CENTRE = "285c71a4-05f7"
                    MARKETER = "c31db01c-b6d6"
                    DEFAULT = CALL_CENTRE

                AUTHORIZATION: dict[Profiles, str] = {
                    Profiles.IT: "6b356d3f53124af3078707163fdaebca3580dc38",
                    Profiles.MARKETER: "6b356d3f53124af3078707163fdaebca3580dc38",
                    Profiles.CALL_CENTRE: "7d453de6fc17d3e6816b0abc46f2b192822130f5",
                }

    class SERVICE:
        NAME: str = "service"

    """
    class VALENTA:
        NAME: str = "valenta"
        PROCESS_NAME: str = "Vlwin"
    """

    class BARCODE_READER:
        PREFIX: str = "("
        SUFFIX: str = ")"

    class NAME_POLICY:
        PARTS_LIST_MIN_LENGTH: int = 3
        PART_ITEM_MIN_LENGTH: int = 3

    class CARD_REGISTRY:
        PLACE_NAME: dict[str, str] = {"Т": "Приёмное отделение", "П": "Поликлиника"}
        PLACE_CARD_HOLDER_MAPPER: dict[str, str] = {"Т": "М-Я", "П": "А-Л"}
        MAX_CARD_PER_FOLDER: int = 60
        SUITABLE_FOLDER_NAME_SYMBOL = ("!", " ")

    class VISUAL:
        YES: str = "✅"
        NO: str = "❌"
        WARNING: str = "⚠️"
        WAIT: str = "⏳"
        NOTIFICATION: str = "🔔"
        ROBOT: str = "🤖"
        SAD: str = "😔"
        GOOD: str = YES
        ERROR: str = NO
        ORANGE_ROMB: str = "🔸"
        BLUE_ROMB: str = "🔹"
        TASK: str = "✳️"
        EYE: str = "👁️"
        HAND_INDICATE: str = "👉"
        HAND_DOWN: str = "👇"
        HAND_UP: str = "☝️"
        INFORMATION: str = "ℹ️"
        QUESTION: str = "❔"

        NUMBER_SYMBOLS: list[str] = [
            "0️⃣",
            "1️⃣",
            "2️⃣",
            "3️⃣",
            "4️⃣",
            "5️⃣",
            "6️⃣",
            "7️⃣",
            "8️⃣",
            "9️⃣",
            "🔟",
        ]

        TEMPERATURE_SYMBOL: str = "°C"

        ARROW: str = "➜"

        BULLET: str = "•"


class MATERIALIZED_RESOURCES:
    NAME: str = "MATERIALIZED_RESOURCES"
    ALIAS: str = "MR"

    class Types(Enum):

        CHILLER_FILTER = MinIntStorageVariableHolder(
            "CHF", description="Фильтры для чиллера", min_value=2
        )

        """
        OPTICAL_DISK_IN_STOCK = MinIntStorageVariableHolder(
            "ODS",
            description="Оптические диски для записи исследований на складе",
            min_value=50,
        )

        OPTICAL_DISK_IN_USE = MinIntStorageVariableHolder(
            "ODU",
            description="Оптические диски для записи исследований в пользовании",
            min_value=10,
        )
        """


class MedicalResearchTypes(Enum):
    MRI = MedicalResearchType(("Магнитно-резонансная томография",), "МРТ")
    CT = MedicalResearchType(("Компьютерная томография",), "КТ")
    ULTRASOUND = MedicalResearchType(("ультразвуковая допплерография",), "УЗИ")


class CheckableSections(IntEnum):
    RESOURCES = auto()
    WS = auto()
    PRINTERS = auto()
    INDICATIONS = auto()
    BACKUPS = auto()
    VALENTA = auto()
    SERVERS = auto()
    MATERIALIZED_RESOURCES = auto()
    TIMESTAMPS = auto()
    DISKS = auto()
    POLIBASE = auto()

    @staticmethod
    def all():
        return [item for item in CheckableSections]


class MarkType(IntEnum):
    NORMAL = auto()
    FREE = auto()
    GUEST = auto()
    TEMPORARY = auto()


class MARK_VARIANT:
    BRACELET: str = "-0-"
    CARD: str = ""


class PolibasePersonInformationQuestStatus(IntEnum):
    UNKNOWN = -1
    GOOD = 0
    EMAIL_IS_EMPTY = 1
    EMAIL_IS_WRONG = 2
    EMAIL_IS_NOT_ACCESSABLE = 4


class ResourceInaccessableReasons(Enum):
    CERTIFICATE_ERROR = "Ошибка проверки сертификата"
    SERVICE_UNAVAILABLE = "Ошибка 503: Сервис недоступен"


class PolibasePersonReviewQuestStep(IntEnum):
    BEGIN = auto()
    #
    ASK_GRADE = auto()
    ASK_FEEDBACK_CALL = auto()
    ASK_INFORMATION_WAY = auto()
    #
    COMPLETE = auto()


class CommandTypes(Enum):
    POLIBASE = (
        "Запрос к базе данный Polibase (Oracle)",
        "polibase",
        "полибейс",
        "oracle",
    )
    DATA_SOURCE = ("Запрос к базе данных DataSource (DS)", "ds")
    CMD = ("Консольную команду", "cmd")
    POWERSHELL = ("Powershell команду", "powershell")
    PYTHON = ("Скрипт Python", "py", "python")
    SSH = ("Команда SSH", "ssh")


class LogMessageChannels(IntEnum):
    BACKUP = auto()
    POLIBASE = auto()
    POLIBASE_BOT = auto()
    DEBUG = auto()
    DEBUG_BOT = auto()
    SERVICES = auto()
    SERVICES_BOT = auto()
    HR = auto()
    HR_BOT = auto()
    IT = auto()
    IT_BOT = auto()
    RESOURCES = auto()
    RESOURCES_BOT = auto()
    PRINTER = auto()
    POLIBASE_ERROR = auto()
    POLIBASE_ERROR_BOT = auto()
    CARD_REGISTRY = auto()
    CARD_REGISTRY_BOT = auto()
    NEW_EMAIL = auto()
    NEW_EMAIL_BOT = auto()
    TIME_TRACKING = auto()
    JOURNAL = auto()
    JOURNAL_BOT = auto()
    POLIBASE_DOCUMENT = auto()
    POLIBASE_DOCUMENT_BOT = auto()
    DEFAULT = DEBUG


class LogMessageFlags(IntEnum):
    NORMAL = 1
    ERROR = 2
    NOTIFICATION = 4
    DEBUG = 8
    SAVE = 16
    SILENCE = 32
    RESULT = 64
    WHATSAPP = 128
    ALERT = 256
    TASK = 512
    SAVE_ONCE = 1024
    SEND_ONCE = SAVE_ONCE | 2048
    DEFAULT = NORMAL


class SUBSCRIBTION_TYPE:
    ON_CALL: int = 1
    ON_RESULT: int = 2
    ON_RESULT_SEQUENTIALLY: int = 4


class WorkstationMessageMethodTypes(IntEnum):
    REMOTE = auto()
    LOCAL_MSG = auto()
    LOCAL_PSTOOL_MSG = auto()


class MessageTypes(IntEnum):
    WHATSAPP = auto()
    TELEGRAM = auto()
    WORKSTATION = auto()


class MessageStatuses(IntEnum):
    REGISTERED = 0
    COMPLETE = 1
    AT_WORK = 2
    ERROR = 3
    ABORT = 4


'''
class Actions(Enum):

    CHILLER_FILTER_CHANGING = ActionDescription(
        "CHILLER_FILTER_CHANGING",
        ("filter",),
        "Замена фильтра очистки воды",
        "Заменить фильтр очистки воды",
    )

    SWITCH_TO_EXTERNAL_WATER_SOURCE = ActionDescription(
        "SWITCH_TO_EXTERNAL_WATER_SOURCE",
        ("external_ws",),
        "Переход на внешнее (городское) водоснабжение",
        "Перейти на внешнее (городское) водоснабжение",
    )

    SWITCH_TO_INTERNAL_WATER_SOURCE = ActionDescription(
        "SWITCH_TO_INTERNAL_WATER_SOURCE",
        ("internal_ws",),
        "Переход на внутреннее водоснабжение",
        "Перейти на внутреннее водоснабжение",
    )

    """
    VALENTA_SYNCHRONIZATION = ActionDescription(
        "VALENTA_SYNCHRONIZATION",
        (CONST.VALENTA.NAME, "валента"),
        "Синхронизация Валенты",
        "Совершить синхронизацию для Валенты",
        False,
        True,
        forcable=True,
    )"
    """

    TIME_TRACKING_REPORT = ActionDescription(
        "TIME_TRACKING_REPORT",
        ("tt", "урв"),
        "Отчеты по учёту рабочего времени",
        "Создать",
        False,
        False,
    )

    DOOR_OPEN = ActionDescription(
        "DOOR_OPEN",
        ("door_open",),
        "Открыть {name} дверь",
        "Открыть",
        False,
        False,
    )

    DOOR_CLOSE = ActionDescription(
        "DOOR_CLOSE",
        ("door_close",),
        "Закрыть {name} дверь",
        "Закрыть",
        False,
        False,
    )

    ATTACH_SHARED_DISKS = ActionDescription(
        "ATTACH_SHARED_DISKS",
        ("attach",),
        "Присоединить сетевые диски",
        "Присоединить",
        False,
        True,
    )

    ACTION = ActionDescription(
        "ACTION",
        ("action",),
        "Неспециализированное действие",
        None,
        False,
        True,
        forcable=False,
    )

'''


class STATISTICS:
    class Types(Enum):
        CT = "CT"
        CT_DAY = "CT_DAY"
        CT_WEEK = "CT_WEEK"
        CT_MONTH = "CT_MONTH"
        CHILLER_FILTER = MATERIALIZED_RESOURCES.Types.CHILLER_FILTER.name
        MRI_COLDHEAD = "MRI_COLDHEAD"
        POLIBASE_DATABASE_DUMP = "POLIBASE_DATABASE_DUMP"
        POLIBASE_PERSON_REVIEW_NOTIFICATION = "POLIBASE_PERSON_REVIEW_NOTIFICATION"


class JournalType(tuple[int, OrderedNameCaptionDescription], Enum):
    GENERAL = (
        0,
        OrderedNameCaptionDescription("general", "Общий", order=1),
    )
    COMPUTER = (
        1,
        OrderedNameCaptionDescription("computer", "Компьютер", order=2),
    )
    MRI_CHILLER = (
        2,
        OrderedNameCaptionDescription("mri_chiller", "Чиллер МРТ", order=4),
    )
    MRI_GRADIENT_CHILLER = (
        3,
        OrderedNameCaptionDescription(
            "mri_gradient_chiller", "Чиллер градиентов МРТ", order=5
        ),
    )
    MRI_CLOSET_CHILLER = (
        4,
        OrderedNameCaptionDescription(
            "mri_closet_chiller", "Чиллер кабинета МРТ", order=6
        ),
    )
    CHILLER = (5, OrderedNameCaptionDescription("chiller", "Чиллер", order=3))
    COMMUNICATION_ROOM = (
        6,
        OrderedNameCaptionDescription(
            "communication_room", "Коммутационная комната", order=10
        ),
    )
    SERVER_ROOM = (
        7,
        OrderedNameCaptionDescription("server_room", "Серверная комната", order=9),
    )
    MRI_TECHNICAL_ROOM = (
        8,
        OrderedNameCaptionDescription(
            "mri_technical_room", "Техническая комната МРТ", order=7
        ),
    )
    MRI_PROCEDURAL_ROOM = (
        9,
        OrderedNameCaptionDescription(
            "mri_procedural_room", "Процедурная комната МРТ", order=9
        ),
    )
    PRINTER = (
        10,
        OrderedNameCaptionDescription("printer", "Принтер", order=11),
    )
    SERVER = (
        11,
        OrderedNameCaptionDescription("server", "Сервер", order=12),
    )
    OUTSIDE_SERVER = (
        12,
        OrderedNameCaptionDescription("outside_server", "Внешний сервер", order=13),
    )
    AGREEMENT = (
        13,
        OrderedNameCaptionDescription("agreement", "Договор и счет", order=14),
    )
    XRAY = (
        14,
        OrderedNameCaptionDescription("xray", "Рентген", order=15),
    )
    CASH_REGISTER = (
        15,
        OrderedNameCaptionDescription("cash_register", "Касса", order=16),
    )
    CT = (
        16,
        OrderedNameCaptionDescription("ct", "КТ", order=2),
    )


class Tags(tuple[int, IconedOrderedNameCaptionDescription], Enum):
    SERVICE = (
        1,
        IconedOrderedNameCaptionDescription(
            None, "Обслуживание", None, 4, CONST.VISUAL.GOOD
        ),
    )
    ERROR = (
        2,
        IconedOrderedNameCaptionDescription(
            None, "Ошибка", None, 2, CONST.VISUAL.ERROR
        ),
    )
    WARNING = (
        3,
        IconedOrderedNameCaptionDescription(
            None, "Внимание", None, 3, CONST.VISUAL.WARNING
        ),
    )
    NOTIFICATION = (
        4,
        IconedOrderedNameCaptionDescription(
            None, "Уведомление", None, 1, CONST.VISUAL.NOTIFICATION
        ),
    )
    TASK = (
        5,
        IconedOrderedNameCaptionDescription(
            None,
            "Задача",
            None,
            6,
            CONST.VISUAL.TASK,
        ),
    )
    INSPECTION = (
        6,
        IconedOrderedNameCaptionDescription(
            None,
            "Осмотр",
            None,
            5,
            CONST.VISUAL.EYE,
        ),
    )
    INFORMATION = (
        7,
        IconedOrderedNameCaptionDescription(
            None,
            "Информация",
            None,
            0,
            CONST.VISUAL.INFORMATION,
        ),
    )
