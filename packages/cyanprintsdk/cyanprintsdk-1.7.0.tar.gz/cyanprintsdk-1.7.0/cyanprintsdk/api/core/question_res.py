from typing import Optional, List, Union

from cyanprintsdk.api.base_model import CyanBaseModel


class ConfirmQuestionRes(CyanBaseModel):
    message: str
    desc: Optional[str] = None
    default: Optional[str] = None
    error_message: Optional[str] = None
    type: str = "confirm"


class DateQuestionRes(CyanBaseModel):
    message: str
    default: Optional[str] = None
    desc: Optional[str] = None
    min_date: Optional[str] = None
    max_date: Optional[str] = None
    type: str = "date"


class CheckboxQuestionRes(CyanBaseModel):
    message: str
    desc: Optional[str] = None
    options: List[str]
    type: str = "checkbox"


class PasswordQuestionRes(CyanBaseModel):
    message: str
    desc: Optional[str] = None
    confirmation: Optional[bool] = None
    type: str = "password"


class SelectQuestionRes(CyanBaseModel):
    message: str
    options: List[str]
    desc: Optional[str] = None
    type: str = "select"


class TextQuestionRes(CyanBaseModel):
    message: str
    default: Optional[str] = None
    desc: Optional[str] = None
    initial: Optional[str] = None
    type: str = "text"


QuestionRes = Union[
    ConfirmQuestionRes,
    DateQuestionRes,
    CheckboxQuestionRes,
    PasswordQuestionRes,
    SelectQuestionRes,
    TextQuestionRes,
]
