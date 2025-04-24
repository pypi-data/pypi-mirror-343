from typing import List, Union, Optional

from cyanprintsdk.domain.core.answer import (
    Answer,
    is_string_array_answer,
    is_bool_answer,
    is_string_answer,
)
from cyanprintsdk.domain.core.inquirer import IInquirer
from cyanprintsdk.domain.core.question import (
    Question,
    CheckboxQ,
    ConfirmQ,
    PasswordQ,
    SelectQ,
    TextQ,
    DateQ,
)
from cyanprintsdk.domain.service.out_of_answer_error import OutOfAnswerException


class StatelessInquirer(IInquirer):
    def __init__(self, answers: List[Answer], pointer: int):
        self._answers = answers
        self._pointer = pointer

    def _get_answer(self, q: Question) -> Answer:
        if self._pointer == len(self._answers) - 1:
            raise OutOfAnswerException("", q)

        self._pointer += 1
        return self._answers[self._pointer]

    async def checkbox(
        self,
        q: Union[CheckboxQ, str],
        options: Optional[List[str]] = None,
        desc: Optional[str] = None,
    ) -> List[str]:
        if isinstance(q, str):
            if options is None:
                raise ValueError("options cannot be null")
            return await self.checkbox(CheckboxQ(message=q, options=options, desc=desc))

        answer = self._get_answer(q)
        if is_string_array_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: StringArrayAnswer. Got: "
            + str(type(answer))
        )

    async def confirm(
        self, q: Union[ConfirmQ, str], desc: Optional[str] = None
    ) -> bool:
        if isinstance(q, str):
            return await self.confirm(ConfirmQ(message=q, desc=desc))

        answer = self._get_answer(q)
        if is_bool_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: BoolAnswer. Got: " + str(type(answer))
        )

    async def password(
        self, q: Union[PasswordQ, str], desc: Optional[str] = None
    ) -> str:
        if isinstance(q, str):
            return await self.password(PasswordQ(message=q, desc=desc))

        answer = self._get_answer(q)
        if is_string_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: StringAnswer. Got: " + str(type(answer))
        )

    async def select(
        self,
        q: Union[SelectQ, str],
        options: Optional[List[str]] = None,
        desc: Optional[str] = None,
    ) -> str:
        if isinstance(q, str):
            if options is None:
                raise ValueError("options cannot be null")
            return await self.select(SelectQ(message=q, options=options, desc=desc))

        answer = self._get_answer(q)
        if is_string_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: StringAnswer. Got: " + str(type(answer))
        )

    async def text(self, q: Union[TextQ, str], desc: Optional[str] = None) -> str:
        if isinstance(q, str):
            return await self.text(
                TextQ(
                    message=q,
                    desc=desc,
                    validate=None,
                )
            )

        answer = self._get_answer(q)
        if is_string_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: StringAnswer. Got: " + str(type(answer))
        )

    async def date_select(
        self, q: Union[DateQ, str], desc: Optional[str] = None
    ) -> str:
        if isinstance(q, str):
            return await self.date_select(DateQ(message=q, desc=desc))

        answer = self._get_answer(q)
        if is_string_answer(answer):
            return answer.answer

        raise TypeError(
            "Incorrect answer type. Expected: StringAnswer. Got: " + str(type(answer))
        )
