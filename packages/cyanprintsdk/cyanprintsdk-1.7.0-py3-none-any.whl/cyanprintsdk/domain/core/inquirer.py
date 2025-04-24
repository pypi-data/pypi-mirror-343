from abc import ABC, abstractmethod
from typing import List, Union, Optional

from cyanprintsdk.domain.core.question import (
    CheckboxQ,
    ConfirmQ,
    PasswordQ,
    SelectQ,
    TextQ,
    DateQ,
)


class IInquirer(ABC):

    @abstractmethod
    async def checkbox(
        self,
        q: Union[CheckboxQ, str],
        options: Optional[List[str]] = None,
        desc: Optional[str] = None,
    ) -> List[str]:
        pass

    @abstractmethod
    async def confirm(
        self, q: Union[ConfirmQ, str], desc: Optional[str] = None
    ) -> bool:
        pass

    @abstractmethod
    async def password(
        self, q: Union[PasswordQ, str], desc: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    async def select(
        self,
        q: Union[SelectQ, str],
        options: Optional[List[str]] = None,
        desc: Optional[str] = None,
    ) -> str:
        pass

    @abstractmethod
    async def text(self, q: Union[TextQ, str], desc: Optional[str] = None) -> str:
        pass

    @abstractmethod
    async def date_select(
        self, q: Union[DateQ, str], desc: Optional[str] = None
    ) -> str:
        pass
