import os

from sgb.consts.facade import *
from sgb.consts.file import FILE
from isgb import ROOT_MODULE_NAME
from sgb.consts.python import PYTHON
from sgb.tools import j, n, PathTool, nn


from setuptools.dist import Distribution

PATH_SPLITTER: str = "/"
PATH_DOUBLE_SPLITTER: str = "//"


class PATH_FACADE:
    LINUX_MOUNT_POINT: str = j((PATH_SPLITTER, "mnt"))
    LINUX_MOUNT_POINT_PATH: str = j((LINUX_MOUNT_POINT, FACADE.NAME), PATH_SPLITTER)
    FILES_NAME: str = ".files"
    TOOLS_NAME: str = ".tools"
    SCRIPTS_NAME: str = "scripts"

    VALUE: str = "C:\\facade\\"

    """
    j(
        (
            PATH_DOUBLE_SPLITTER,
            AD.DOMAIN,
            PATH_SPLITTER,
            FACADE.NAME,
            PATH_SPLITTER,
        )
    )
    """

    @staticmethod
    def SERVICE(service_name: str) -> str:
        return os.path.join(
            PATH_FACADE.VALUE,
            FACADE.SERVICE_NAME(service_name),
        )

    @staticmethod
    def SERVICE_FILES(standalone_name: str) -> str:
        return os.path.join(PATH_FACADE.FILES(), standalone_name)

    @staticmethod
    def SERVICE_TOOLS(standalone_name: str) -> str:
        return os.path.join(PATH_FACADE.TOOLS(), standalone_name)

    @staticmethod
    def FILES() -> str:
        return os.path.join(PATH_FACADE.VALUE, PATH_FACADE.FILES_NAME)

    @staticmethod
    def TOOLS() -> str:
        return os.path.join(PATH_FACADE.VALUE, PATH_FACADE.TOOLS_NAME)


    class DITRIBUTIVE:

        SPLITTER: str = "-"
        FOLDER_NAME: str = ".distr"
        PACKAGE_FOLDER_NAME: str = "all"
        DEFAULT_PACKAGE_TAG: str = "py3-none-any"

        @staticmethod
        def NAME(value: str, version: str | None = None) -> str:
            return j(
                (ROOT_MODULE_NAME, value, None if n(version) else j(("==", version))),
                PATH_FACADE.DITRIBUTIVE.SPLITTER,
            )

        @staticmethod
        def VALUE() -> str:
            return os.path.join(PATH_FACADE.VALUE, PATH_FACADE.DITRIBUTIVE.FOLDER_NAME)

        @staticmethod
        def PACKAGE_FOLDER(name: str, version: str | None = None) -> str:
            path_list: list[str] = [PATH_FACADE.DITRIBUTIVE.VALUE(), name]
            if nn(version):
                path_list.insert(1, PATH_FACADE.DITRIBUTIVE.PACKAGE_FOLDER_NAME)
            return os.path.join(*path_list)

        @staticmethod
        def PACKAGE(name: str, version: str | None) -> str:
            def wheel_name(name: str, version: str | None) -> str:
                tag: str = ""
                dist_name: str = ""
                try:
                    dist: Distribution = Distribution(
                        attrs={"name": name, "version": version}
                    )
                    bdist_wheel_cmd = dist.get_command_obj("bdist_wheel")
                    bdist_wheel_cmd.ensure_finalized()
                    dist_name = bdist_wheel_cmd.wheel_dist_name
                    tag = PATH_FACADE.DITRIBUTIVE.SPLITTER.join(
                        bdist_wheel_cmd.get_tag()
                    )
                except BaseException as _:
                    dist_name = PATH_FACADE.DITRIBUTIVE.SPLITTER.join((name, version))
                    tag = PATH_FACADE.DITRIBUTIVE.DEFAULT_PACKAGE_TAG
                return PathTool.add_extension(
                    j((dist_name, PATH_FACADE.DITRIBUTIVE.SPLITTER, tag)),
                    PYTHON.PACKAGE_EXTENSION,
                )

            return os.path.join(
                *[
                    PATH_FACADE.DITRIBUTIVE.PACKAGE_FOLDER(name, version),
                    wheel_name(
                        j((ROOT_MODULE_NAME, name), "_"),
                        version,
                    ),
                ]
            )

    class VIRTUAL_ENVIRONMENT:

        NAME_PREFIX: str = ".venv"


class PATH_DATA_STORAGE:
    NAME: str = ".data"
    VALUE: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_BUILD:
    NAME: str = ".build"
    VALUE: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_APP:
    NAME: str = "apps"
    FOLDER: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_DOCS:
    NAME: str = f"Docs{FACADE.SERVICE_FOLDER_SUFFIX}"
    FOLDER: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATH_FONTS:
    NAME: str = "fonts"
    FOLDER: str = os.path.join(PATH_DOCS.FOLDER, NAME)

    @staticmethod
    def get(name: str) -> str:
        from sgb.tools import PathTool

        return os.path.join(
            PATH_FONTS.FOLDER,
            PathTool.add_extension(name, FILE.EXTENSION.TRUE_TYPE_FONT),
        )



class PATH_WS:
    NAME: str = j(("WS", FACADE.SERVICE_FOLDER_SUFFIX))
    PATH: str = os.path.join(PATH_FACADE.VALUE, NAME)


class PATHS:
    WS: PATH_WS = PATH_WS()
    DOCS: PATH_DOCS = PATH_DOCS()
    FONTS: PATH_FONTS = PATH_FONTS()
    FACADE: PATH_FACADE = PATH_FACADE()
    DATA_STORAGE: PATH_DATA_STORAGE = PATH_DATA_STORAGE()
    BUILD: PATH_BUILD = PATH_BUILD()
