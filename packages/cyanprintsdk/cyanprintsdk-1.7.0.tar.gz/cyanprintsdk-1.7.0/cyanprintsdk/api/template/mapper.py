from cyanprintsdk.api.core.core_mapper import AnswerMapper, QuestionMapper, CyanMapper
from cyanprintsdk.api.template.req import TemplateAnswerReq, TemplateValidateReq
from cyanprintsdk.api.template.res import TemplateRes, TemplateQnARes, TemplateFinalRes
from cyanprintsdk.domain.template.input import TemplateInput, TemplateValidateInput
from cyanprintsdk.domain.template.output import TemplateOutput, is_qna, is_final


class TemplateInputMapper:
    @staticmethod
    def answer_to_domain(req: TemplateAnswerReq) -> TemplateInput:
        answers = [AnswerMapper.to_domain(x) for x in req.answers]
        return TemplateInput(
            answers=answers,
            deterministic_state=req.deterministic_states,
        )

    @staticmethod
    def validate_to_domain(req: TemplateValidateReq) -> TemplateValidateInput:
        answers = [AnswerMapper.to_domain(x) for x in req.answers]
        return TemplateValidateInput(
            deterministic_state=req.deterministic_states,
            answers=answers,
            validate=req.validate,
        )


class TemplateOutputMapper:
    @staticmethod
    def to_resp(output: TemplateOutput) -> TemplateRes:
        if is_qna(output):
            return TemplateQnARes(
                type="questionnaire",
                deterministic_state=output.deterministic_state,
                question=QuestionMapper.question_to_resp(output.question),
            )
        elif is_final(output):
            return TemplateFinalRes(
                cyan=CyanMapper.cyan_to_resp(output.data), type="final"
            )
        else:
            raise ValueError(f"Invalid output type {output}")
