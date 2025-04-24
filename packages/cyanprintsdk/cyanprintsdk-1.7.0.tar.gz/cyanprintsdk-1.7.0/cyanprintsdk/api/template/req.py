from typing import Dict, List

from cyanprintsdk.api.base_model import CyanBaseModel

from cyanprintsdk.api.core.answer_req import AnswerReq


class TemplateValidateReq(CyanBaseModel):
    answers: List[AnswerReq]
    deterministic_states: List[Dict[str, str]]
    validate: str


class TemplateAnswerReq(CyanBaseModel):
    answers: List[AnswerReq]
    deterministic_states: List[Dict[str, str]]
