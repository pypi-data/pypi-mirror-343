from enum import Enum
from sgb.consts import CONST
from sgb.collections import (
    StorageVariableHolder,
    IntStorageVariableHolder,
    BoolStorageVariableHolder,
    TimeStorageVariableHolder,
    FloatStorageVariableHolder,
    IntListStorageVariableHolder,
    DateListStorageVariableHolder,
    StringListStorageVariableHolder,
    IntVariantableStorageVariableHolder,
)


class SETTINGS(Enum):

    USE_GOOGLE_KEEP = BoolStorageVariableHolder(
        "USE_GOOGLE_KEEP",
        False,
    )


    UNISENDER_API_KEY = StorageVariableHolder(
        "UNISENDER_API_KEY",
        "65ddrin3zh791hxarbkwe4fmah5p44hkg4cjwsuy",
    )

    UNISENDER_API_LIST_IDS = StorageVariableHolder(
        "UNISENDER_API_LIST_IDS",
        "761",
    )

    SGB_CLI_ADMINISTRATOR_LOGIN = StorageVariableHolder(
        "SGB_CLI_ADMINISTRATOR_LOGIN",
        "nak",
    )

    USER_RESPONSIBLE_FOR_PATIENT_MARK = StorageVariableHolder(
        "USER_RESPONSIBLE_FOR_PATIENT_MARK",
        "baa",
    )

    WIFI_VIP_PASSWORD = StorageVariableHolder("WIFI_VIP_PASSWORD", "ilovepacific")

    PLAIN_FORMAT_AS_DEFAULT_LOGIN_LIST = StringListStorageVariableHolder(
        "PLAIN_FORMAT_AS_DEFAULT_LOGIN_LIST", ("bar", "rob", "ptyu")
    )

    CHILLER_RECOGNIZE_LOG_LEVEL = IntStorageVariableHolder(
        "CHILLER_RECOGNIZE_LOG_LEVEL", 0
    )

    HEART_BEAT_IS_ON = BoolStorageVariableHolder("HEART_BEAT_IS_ON", True)

    CT_INDICATIONS_VALUE_TEMPERATURE_CORRECTION = FloatStorageVariableHolder(
        "CT_INDICATIONS_VALUE_TEMPERATURE_CORRECTION", 0.7
    )

    CT_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES = IntStorageVariableHolder(
        "CT_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES", 60
    )

    CHILLER_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES = IntStorageVariableHolder(
        "CHILLER_INDICATIONS_VALUE_SAVE_PERIOD_IN_MINUTES", 60
    )

    HOSPITAL_WORK_DAY_START_TIME = TimeStorageVariableHolder(
        "HOSPITAL_WORK_DAY_START_TIME", "8:00"
    )
    HOSPITAL_WORK_DAY_END_TIME = TimeStorageVariableHolder(
        "HOSPITAL_WORK_DAY_END_TIME", "20:00"
    )
    OFFICE_WORK_DAY_START_TIME = TimeStorageVariableHolder(
        "OFFICE_WORK_DAY_START_TIME", "8:30"
    )
    OFFICE_WORK_DAY_END_TIME = TimeStorageVariableHolder(
        "OFFICE_WORK_DAY_END_TIME", "17:00"
    )

    INDICATION_CT_NOTIFICATION_START_TIME = DateListStorageVariableHolder(
        "INDICATION_CT_NOTIFICATION_START_TIME", None
        #("8:00", "12:00", "15:00", "17:00")
    )

    USER_USE_CACHE = BoolStorageVariableHolder("USER_USE_CACHE", True)

    TIME_TRACKING_FOR_POLYCLINIC = StringListStorageVariableHolder(
        "TIME_TRACKING_FOR_POLYCLINIC",
        (
            "035",
            "045",
            "058",
            "101-0-",
            "124",
            "125",
            "131",
            "137",
            "139",
            #"177",
            "183",
            "190",
        ),
    )

    #
    RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME = TimeStorageVariableHolder(
        "RESOURCE_MANAGER_CHECK_SITE_CERTIFICATE_START_TIME", "8:00"
    )

    #
    RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES = IntStorageVariableHolder(
        "RESOURCE_MANAGER_CHECK_SITE_FREE_SPACE_PERIOD_IN_MINUTES", 15
    )
    #
    PRINTER_REPORT_PERIOD_IN_MINUTES = IntStorageVariableHolder(
        "PRINTER_REPORT_PERIOD_IN_MINUTES", 5
    )

    PRINTER_MINIMAL_REPORT_VALUE = IntStorageVariableHolder(
        "PRINTER_MINIMAL_REPORT_VALUE", 10
    )

    OUTSORCE_PRINTER_REPORT_IS_ON = BoolStorageVariableHolder(
        "OUTSORCE_PRINTER_REPORT_IS_ON", True
    )

    OUTSORCE_PRINTER_REPORT_START_TIME = TimeStorageVariableHolder(
        "OUTSORCE_PRINTER_REPORT_TIME", "9:00"
    )
    #
  

    BONUS_PROGRAM_IS_ON = BoolStorageVariableHolder(
        "BONUS_PROGRAM_IS_ON",
        False,
    )

    BONUS_PROGRAM_DISCOUNT_PERCENT = IntStorageVariableHolder(
        "BONUS_PROGRAM_DISCOUNT_PERCENT",
        50,
    )

    BONUS_PROGRAM_CASHBACK_PERCENT = IntStorageVariableHolder(
        "BONUS_PROGRAM_CASHBACK_PERCENT",
        3,
    )

    BONUS_PROGRAM_BONUS_MINIMUM = IntStorageVariableHolder(
        "BONUS_PROGRAM_BONUS_MINIMUM",
        10,
    )

    BONUS_PROGRAM_NOTIFICATION_COUNT_MAX = IntStorageVariableHolder(
        "BONUS_PROGRAM_NOTIFICATION_COUNT_MAX",
        3,
    )

    WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON = BoolStorageVariableHolder(
        "WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON", True
    )

    WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS = IntStorageVariableHolder(
        "WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS", 6000
    )

    WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS = IntStorageVariableHolder(
        "WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS", 12000
    )

    WHATSAPP_MESSAGE_SENDER_USER_LOGIN = StorageVariableHolder(
        "WHATSAPP_MESSAGE_SENDER_USER_LOGIN", "Administrator"
    )

    WORKSTATION_SHUTDOWN_TIME = TimeStorageVariableHolder(
        "WORKSTATION_SHUTDOWN_TIME", "21:00"
    )

    WORKSTATION_REBOOT_TIME = TimeStorageVariableHolder(
        "WORKSTATION_REBOOT_TIME", "21:00"
    )

    EMAIL_VALIDATION_IS_ON = BoolStorageVariableHolder("EMAIL_VALIDATION_IS_ON", True)
    EMAIL_VALIDATION_TEST = BoolStorageVariableHolder("EMAIL_VALIDATION_TEST", False)

    CHILLER_ALERT_TEMPERATURE = FloatStorageVariableHolder(
        "CHILLER_ALERT_TEMPERATURE", 17.0
    )

    CHILLER_COUNT_DEFAULT = FloatStorageVariableHolder("CHILLER_COUNT_DEFAULT", 3)

    CHILLER_MAX_TEMPERATURE = IntStorageVariableHolder("CHILLER_MAX_TEMPERATURE", 16)

    CHILLER_MIN_TEMPERATURE = IntStorageVariableHolder("CHILLER_MIN_TEMPERATURE", 10)

    CHILLER_ACTION_MAX_TEMPERATURE = FloatStorageVariableHolder(
        "CHILLER_ACTION_MAX_TEMPERATURE", 15.1
    )

    CHILLER_ACTION_MIN_TEMPERATURE = IntStorageVariableHolder(
        "CHILLER_ACTION_MIN_TEMPERATURE", 11
    )

    CT_ROOM_MAX_TEMPERATURE = IntStorageVariableHolder("CT_ROOM_MAX_TEMPERATURE", 24)

    CT_ROOM_MIN_TEMPERATURE = IntStorageVariableHolder("CT_ROOM_MIN_TEMPERATURE", 20)

    CT_ROOM_MAX_HUMIDITY = IntStorageVariableHolder("CT_ROOM_MAX_HUMIDITY", 60)

    CT_ROOM_MIN_HUMIDITY = IntStorageVariableHolder("CT_ROOM_MIN_HUMIDITY", 30)

    CHECK_ALL_RECIPIENT_USER_LOGIN = StorageVariableHolder(
        "CHECK_ALL_RECIPIENT_USER_LOGIN", "nak"
    )

    MAIL_SITE_FREE_MEMORY_PERIOD = IntStorageVariableHolder(
        "MAIL_SITE_FREE_MEMORY_PERIOD", 180
    )

    SITE_FREE_MEMORY_PERIOD = IntStorageVariableHolder("SITE_FREE_MEMORY_PERIOD", 180)
