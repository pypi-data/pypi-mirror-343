from dataclasses import dataclass
from typing import List, Dict, Union

from cyanprintsdk.domain.core.cyan import Cyan
from cyanprintsdk.domain.core.question import Question


@dataclass
class ExtensionQnAOutput:
    deterministic_state: List[Dict[str, str]]
    question: Question


@dataclass
class ExtensionFinalOutput:
    data: Cyan


# Union type to represent either ExtensionQnAOutput or ExtensionFinalOutput
ExtensionOutput = Union[ExtensionQnAOutput, ExtensionFinalOutput]


def is_final(output: ExtensionOutput) -> bool:
    return isinstance(output, ExtensionFinalOutput) and output.data is not None


def is_qna(output: ExtensionOutput) -> bool:
    return isinstance(output, ExtensionQnAOutput) and output.question is not None
