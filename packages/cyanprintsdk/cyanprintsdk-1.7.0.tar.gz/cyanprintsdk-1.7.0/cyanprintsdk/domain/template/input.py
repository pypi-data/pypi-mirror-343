from dataclasses import dataclass
from typing import List, Dict

from cyanprintsdk.domain.core.answer import Answer


@dataclass
class TemplateInput:
    answers: List[Answer]
    deterministic_state: List[Dict[str, str]]


@dataclass
class TemplateValidateInput:
    answers: List[Answer]
    deterministic_state: List[Dict[str, str]]
    validate: str
