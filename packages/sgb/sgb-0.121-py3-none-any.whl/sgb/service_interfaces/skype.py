import isgb

from abc import ABC, abstractmethod

from sgb.consts.community import COMMUNITY
from sgb.collections import Any, Result, Callable
from sgb.service.interface import ClientBase, IClientBase
from sgb.consts.service import SERVICE_ROLE as SR, SERVICE_COMMAND as SC

class IResultSkypeBusinessClient(ABC, IClientBase):

    @abstractmethod
    def get_next_free_telephone(self, community: COMMUNITY) -> Result[int]:
        pass


class SkypeBusinessClient(ClientBase):

    class RESULT(IResultSkypeBusinessClient, ClientBase):

        def call(
            self,
            command: SC | str,
            parameters: tuple[
                Any,
                ...,
            ],
        ) -> Result:
            return super().call(SR.SKYPE, command, parameters)

        def call_for_result(
            self,
            command: SC | str,
            parameters: tuple[
                Any,
                ...,
            ],
            class_type_holder: Any | Callable[[Any], Any] | None = None,
        ) -> Result:
            return super().call_for_result(SR.SKYPE, command, parameters, class_type_holder)

        def get_next_free_telephone(self, community: COMMUNITY) -> Result[int]:
            return self.call_for_result("get_next_free_telephone", (community,), int)
