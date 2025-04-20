import logging
from src.extras.PhpSerializer import decode_php_serialized
from src.models.custom_types import AnswerTypeEnum
from src.models.wp_forms import WPForm
from src.models.wp_fields import WPField
from src.models.questionnaires import Questionnaire
from src.schemas.dependencies import Dependencies, ShowHideEnum, AllAnyEnum, Condition, ConditionOperatorEnum
from src.schemas.questions import QuestionBase
from src.schemas.questionnaires import QuestionnaireCreateWithQuestions, QuestionnaireCreateWithQuestionsNew

logger = logging.getLogger(__name__)


class WPToQuestionnaireAdapter:
    """
    Преобразует WPForm + вложенные WPField + optional MainQuestionnaire + новый хеш
    в одну из схем:
      - QuestionnaireCreateWithQuestions, если existing_questionnaire передан
      - QuestionnaireCreateWithQuestionsNew, если existing_questionnaire == None
    """

    def adapt(self,
              wp_form: WPForm,
              existing_questionnaire: Questionnaire | None,
              new_hash: str) -> QuestionnaireCreateWithQuestions | QuestionnaireCreateWithQuestionsNew:

        questionnaire_kwargs = {
            "questionnaire_name": wp_form.name,
            "wordpress_id": wp_form.id,
            "is_active": True,
            "questionnaire_hash": new_hash,
        }

        if existing_questionnaire:
            questionnaire_kwargs["questionnaire_id"] = existing_questionnaire.questionnaire_id
            questionnaire_kwargs["questionnaire_version"] = existing_questionnaire.questionnaire_version + 1

        # Составляем список вопросов
        questions: list[QuestionBase] = []
        for field in wp_form.fields:
            question = QuestionBase(
                question=field.name or "",
                question_order=field.field_order,
                answers=self._decode_answers(field),
                answer_type=self._decode_answer_type(field),
                dependencies=self._decode_dependencies(field),
                wordpress_id=field.id,
            )
            questions.append(question)

        questionnaire_kwargs["questions"] = questions

        if existing_questionnaire:
            return QuestionnaireCreateWithQuestions(**questionnaire_kwargs)
        else:
            return QuestionnaireCreateWithQuestionsNew(**questionnaire_kwargs)

    def adapt_all(self, data: list[tuple[WPForm, Questionnaire | None, str]]
                  ) -> list[QuestionnaireCreateWithQuestions | QuestionnaireCreateWithQuestionsNew]:
        return [self.adapt(wp_form, existing_questionnaire, new_hash)
                for wp_form, existing_questionnaire, new_hash in data]

    @staticmethod
    def _decode_answers(field: WPField) -> list[str] | None:
        """Парсим field.options через PhpSerializer, возвращаем список value."""

        raw = field.options
        if not raw:
            return None

        try:
            options = decode_php_serialized(raw)
            if isinstance(options, dict):
                options = list(options.values())
            # Ожидаем список словарей с ключом 'value'
            return [item.get("value", "") for item in options if item.get("value", "")]

        except Exception as error:
            logger.error("Failed to decode answers for field %s: %s", field.id, error)
            return None

    @staticmethod
    def _decode_answer_type(field: WPField) -> AnswerTypeEnum:
        """
        Преобразуем field.type в AnswerTypeEnum.
        Если тип неизвестен — логируем и ставим 'text' по умолчанию.
        """
        # Приводим к верхнему регистру, чтобы совпадало с Enum
        t = (field.type or "").upper()
        if t not in AnswerTypeEnum.__members__:
            logger.warning("Unknown field.type '%s' for field %s, defaulting to TEXTAREA", t, field.id)
            t = "TEXTAREA"
        return AnswerTypeEnum(t)

    @staticmethod
    def _decode_dependencies(field: WPField) -> Dependencies:
        """
        Декодируем field.field_options через PhpSerializer -> dict,
        затем собираем Dependencies(show_hide, all_any, conditions).
        """
        raw = field.field_options or ""
        try:
            data = decode_php_serialized(raw)
        except Exception as error:
            logger.error("Failed to decode dependencies for field %s: %s", field.id, error)
            # Если не получилось, возвращаем пустые зависимости
            return Dependencies(show_hide=ShowHideEnum.SHOW, all_any=AllAnyEnum.ALL, conditions=[])

        # show_hide и all_any
        show_hide = ShowHideEnum(data.get("show_hide", "").upper())
        all_any = AllAnyEnum(data.get("any_all", "").upper())

        # Три параллельных списка: hide_field, hide_field_cond, hide_opt
        flds = data.get("hide_field", [])
        conds = data.get("hide_field_cond", [])
        opts = data.get("hide_opt", [])

        conditions: list[Condition] = []
        for fld, cond, val in zip(flds, conds, opts):
            try:
                cond_enum = ConditionOperatorEnum(cond.upper())
            except ValueError:
                logger.warning("Unknown condition operator '%s' in field %s", cond, field.id)
                cond_enum = ConditionOperatorEnum.EQUAL
            conditions.append(
                Condition(
                    field_id=int(fld),
                    condition=cond_enum,
                    value=str(val),
                )
            )

        return Dependencies(show_hide=show_hide, all_any=all_any, conditions=conditions)
