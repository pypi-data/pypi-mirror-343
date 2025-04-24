from typing import List, Dict

from cyanprintsdk.api.base_model import CyanBaseModel

from cyanprintsdk.api.core.answer_req import AnswerReq
from cyanprintsdk.api.core.cyan_req import CyanReq


class ExtensionValidateReq(CyanBaseModel):
    answers: List[AnswerReq]
    deterministic_states: List[Dict[str, str]]
    prev_answers: List[AnswerReq]
    prev_cyan: CyanReq
    prev_extension_answers: Dict[str, List[AnswerReq]]
    prev_extension_cyans: Dict[str, CyanReq]
    validate: str


class ExtensionAnswerReq(CyanBaseModel):
    answers: List[AnswerReq]
    deterministic_states: List[Dict[str, str]]
    prev_answers: List[AnswerReq]
    prev_cyan: CyanReq
    prev_extension_answers: Dict[str, List[AnswerReq]]
    prev_extension_cyans: Dict[str, CyanReq]
