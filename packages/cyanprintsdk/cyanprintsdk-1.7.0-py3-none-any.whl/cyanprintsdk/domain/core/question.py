from dataclasses import dataclass
from datetime import date
from typing import Optional, List, Union, Callable


@dataclass
class CheckboxQ:
    message: str
    options: List[str]
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None


@dataclass
class ConfirmQ:
    message: str
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None
    default: Optional[str] = None
    error_message: Optional[str] = None


@dataclass
class DateQ:
    message: str
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None
    default: Optional[date] = None
    min_date: Optional[date] = None
    max_date: Optional[date] = None


@dataclass
class PasswordQ:
    message: str
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None
    confirmation: Optional[bool] = None


@dataclass
class SelectQ:
    message: str
    options: List[str]
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None


@dataclass
class TextQ:
    message: str
    desc: Optional[str] = None
    validate: Optional[Callable[[str], Optional[str]]] = None
    default: Optional[str] = None
    initial: Optional[str] = None


# Type hint for a generic question
Question = Union[TextQ, SelectQ, PasswordQ, DateQ, ConfirmQ, CheckboxQ]
