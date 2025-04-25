import isgb


from sgb.collections import nstr

import enum


class COMMUNITY(enum.Enum):

    SPHERE = "Сфера"

    GAS = "Грин-Агро Сахалин"

    PK = "Приморский кондитер"

    AGMZ = "Артёмоский гормолокозавод"

    GAK = "Грин Агро-Кировский"

    HAPK = "Грин-Агро «Ханкайский агро-промышленный комплекс»"

    TD = "ТД «Дальневосточные Продукты»"

    MKUS = "Молочный комбинат Южно-Сахалинский"

    ANT = "Охранное агенство «АНТ»"

    DP = "СПССК 'Доступные продукты'"


class COMMUNITY_SETTING_ITEM(enum.Enum):
    SIP_TELEPHONELESS: int = 1


COMMUNITY_SETTINGS: dict[
    COMMUNITY, COMMUNITY_SETTING_ITEM | tuple[COMMUNITY_SETTING_ITEM] | None
] = {
    COMMUNITY.SPHERE: None,
    COMMUNITY.GAS: None,
    COMMUNITY.PK: None,
    COMMUNITY.AGMZ: None,
    COMMUNITY.HAPK: None,
    COMMUNITY.TD: None,
    COMMUNITY.MKUS: None,
    COMMUNITY.ANT: COMMUNITY_SETTING_ITEM.SIP_TELEPHONELESS,
    COMMUNITY.DP: COMMUNITY_SETTING_ITEM.SIP_TELEPHONELESS,
    COMMUNITY.GAK: COMMUNITY_SETTING_ITEM.SIP_TELEPHONELESS
}


COMMUNITY_USER_CONTAINER_NAME: dict[COMMUNITY, nstr] = {
    COMMUNITY.SPHERE: None,
    COMMUNITY.GAS: "greeangro",
    COMMUNITY.PK: "primkon",
    COMMUNITY.AGMZ: None,
    COMMUNITY.HAPK: None,
    COMMUNITY.TD: None,
    COMMUNITY.MKUS: None,
    COMMUNITY.ANT: None,
    COMMUNITY.DP: None,
    COMMUNITY.GAK: None
}
