from cyanprintsdk.api.core.core_mapper import AnswerMapper, CyanMapper, QuestionMapper
from cyanprintsdk.api.extension.req import ExtensionAnswerReq, ExtensionValidateReq
from cyanprintsdk.api.extension.res import (
    ExtensionRes,
    ExtensionQnARes,
    ExtensionFinalRes,
)
from cyanprintsdk.domain.extension.input import (
    ExtensionAnswerInput,
    ExtensionValidateInput,
)
from cyanprintsdk.domain.extension.output import ExtensionOutput, is_final


class ExtensionInputMapper:
    @staticmethod
    def extension_answer_to_domain(req: ExtensionAnswerReq) -> ExtensionAnswerInput:
        answers = [AnswerMapper.to_domain(x) for x in req.answers]
        prev_answers = [AnswerMapper.to_domain(x) for x in req.prev_answers]
        prev_cyan = CyanMapper.cyan_req_to_domain(req.prev_cyan)
        prev_extension_answers = {
            key: [AnswerMapper.to_domain(a) for a in value]
            for key, value in req.prev_extension_answers.items()
        }
        prev_extension_cyans = {
            key: CyanMapper.cyan_req_to_domain(value)
            for key, value in req.prev_extension_cyans.items()
        }

        return ExtensionAnswerInput(
            answers=answers,
            prev_answers=prev_answers,
            deterministic_state=req.deterministic_states,
            prev_cyan=prev_cyan,
            prev_extension_answers=prev_extension_answers,
            prev_extension_cyans=prev_extension_cyans,
        )

    @staticmethod
    def extension_validate_to_domain(
        req: ExtensionValidateReq,
    ) -> ExtensionValidateInput:
        return ExtensionValidateInput(
            answers=[AnswerMapper.to_domain(x) for x in req.answers],
            deterministic_state=req.deterministic_states,
            prev_answers=[AnswerMapper.to_domain(x) for x in req.prev_answers],
            prev_cyan=CyanMapper.cyan_req_to_domain(req.prev_cyan),
            prev_extension_answers={
                key: [AnswerMapper.to_domain(a) for a in value]
                for key, value in req.prev_extension_answers.items()
            },
            prev_extension_cyans={
                key: CyanMapper.cyan_req_to_domain(value)
                for key, value in req.prev_extension_cyans.items()
            },
            validate=req.validate,
        )


class ExtensionOutputMapper:
    @staticmethod
    def to_resp(output: ExtensionOutput) -> ExtensionRes:
        if is_final(output):
            return ExtensionQnARes(
                cyan=CyanMapper.cyan_to_resp(output.data), type="final"
            )
        else:
            return ExtensionFinalRes(
                deterministic_state=output.deterministic_state,
                question=QuestionMapper.question_to_resp(output.question),
                type="questionnaire",
            )
