from typing import Optional, List, Dict, Union

from cyanprintsdk.api.base_model import CyanBaseModel

from cyanprintsdk.api.core.cyan_res import CyanRes
from cyanprintsdk.api.core.question_res import QuestionRes


class ExtensionValidRes(CyanBaseModel):
    valid: Optional[str]


class ExtensionFinalRes(CyanBaseModel):
    cyan: CyanRes
    type: str = "final"


class ExtensionQnARes(CyanBaseModel):
    deterministic_state: List[Dict[str, str]]
    question: QuestionRes
    type: str = "questionnaire"


ExtensionRes = Union[ExtensionQnARes, ExtensionFinalRes]
