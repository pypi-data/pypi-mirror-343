import isgb
from sgb.consts.community import COMMUNITY
"""
trc-ml-pbx	192.168.202.8	1XXX	ООО «Грин Агро-Сахалин»	11xx	-
trc-ml-pbx	192.168.202.8	1XXX	ООО ТД «Дальневосточные Продукты»	13xx	-
vld-np-pbx	192.168.2.8	2XXX	Грин Агро Нижнепортовая\ООО «ХАПК «Грин Агро»	21xx	-
vld-np-pbx	192.168.2.8	2XXX	ООО «Сфера Менеджмент»	22xx	-
vld-np-pbx	192.168.2.8	2XXX	ООО «Грин Агро-Кировский»	29xx	-
vld-np-pbx	192.168.2.8	2XXX	ООО ТД «Дальневосточные Продукты»	28xx	-
art-kr-pbx	192.168.1.9	3XXX	АО ГМЗ «Артёмовский»	31xx	-
art-kr-pbx	192.168.1.9	3XXX	ООО ТД «Дальневосточные Продукты»	33xx	-
krb-nv-pbx	192.168.102.9	4XXX	ООО «ХАПК «Грин Агро»	41xx	В перспективе
us-mir-pbx	192.168.205.11	5XXX	ОАО «Молочный комбинат «Южно-Сахалинский»	52xx	54хх - телефоны операторов (заявки)
-	-	6XXX	-	61xx	Свободно
vld-al-pbx	192.168.0.5	7XXX	ООО «Приморский кондитер» Руднева	71xx-78xx	-
"""

TELEPHONE_POOL: dict[COMMUNITY, tuple[dict[COMMUNITY, tuple[int, int]], ...]] = {
    COMMUNITY.SPHERE: {
        COMMUNITY.SPHERE: (2200, 2299),
        COMMUNITY.TD: (2800, 2899),
        COMMUNITY.GAS: (2100, 2199),
        COMMUNITY.HAPK: (2100, 2199),
        COMMUNITY.GAK: (2900, 2999),
    },
    COMMUNITY.GAS: {COMMUNITY.GAS: (1100, 1199), COMMUNITY.TD: (1300, 1399)},
    COMMUNITY.PK: {COMMUNITY.PK: (7000, 7899)},
    COMMUNITY.AGMZ: {COMMUNITY.AGMZ: (3100, 3199), COMMUNITY.TD: (3300, 3399)},
    COMMUNITY.HAPK: {COMMUNITY.HAPK: (4100, 4199)},
    COMMUNITY.MKUS: {COMMUNITY.MKUS: (5000, 5999)},
}
