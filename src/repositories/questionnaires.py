from sqlalchemy import CursorResult, and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models import Question
from src.models.questionnaires import Questionnaire
from src.schemas.questionnaires import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireCreateWithQuestions,
    QuestionnaireCreateWithQuestionsNew,
)
from .base import BaseRepository


class QuestionnaireRepository(BaseRepository):
    entity_name = "questionnaire"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_questionnaire(self, questionnaire: QuestionnaireCreate) -> Questionnaire:
        new_questionnaire = Questionnaire(
            questionnaire_id=questionnaire.questionnaire_id,
            questionnaire_version=questionnaire.questionnaire_version,
            questionnaire_name=questionnaire.questionnaire_name,
            wordpress_id=questionnaire.wordpress_id,
            is_active=questionnaire.is_active,
            tags=questionnaire.tags,
            questionnaire_hash=questionnaire.questionnaire_hash,
        )
        self.session.add(new_questionnaire)
        await self._flush(operation="create")
        return new_questionnaire

    async def create_all_questionnaires_with_questions(
        self, questionnaires: list[QuestionnaireCreateWithQuestions | QuestionnaireCreateWithQuestionsNew]
    ) -> list[Questionnaire]:
        new_questionnaires: list[Questionnaire] = []
        for questionnaire in questionnaires:
            questions: list[Question] = []
            for question_data in questionnaire.questions:
                new_question = Question(
                    question=question_data.question,
                    question_order=question_data.question_order,
                    answer_options=[option.model_dump(mode="json") for option in question_data.answer_options],
                    answer_type=question_data.answer_type,
                    dependencies=question_data.dependencies.model_dump(),
                    wordpress_id=question_data.wordpress_id,
                )
                questions.append(new_question)
            if isinstance(questionnaire, QuestionnaireCreateWithQuestions):
                new_questionnaire = Questionnaire(
                    questionnaire_id=questionnaire.questionnaire_id,
                    questionnaire_version=questionnaire.questionnaire_version,
                    questionnaire_name=questionnaire.questionnaire_name,
                    wordpress_id=questionnaire.wordpress_id,
                    is_active=questionnaire.is_active,
                    tags=questionnaire.tags,
                    questionnaire_hash=questionnaire.questionnaire_hash,
                    questions=questions,
                )
            else:
                new_questionnaire = Questionnaire(
                    questionnaire_name=questionnaire.questionnaire_name,
                    wordpress_id=questionnaire.wordpress_id,
                    is_active=questionnaire.is_active,
                    tags=questionnaire.tags,
                    questionnaire_hash=questionnaire.questionnaire_hash,
                    questions=questions,
                )
            new_questionnaires.append(new_questionnaire)
        self.session.add_all(new_questionnaires)
        await self._flush(operation="create")
        return new_questionnaires

    async def create_all_questionnaires(self, questionnaires: list[QuestionnaireCreate]) -> list[Questionnaire]:
        new_questionnaires: list[Questionnaire] = []
        for questionnaire in questionnaires:
            new_questionnaire = Questionnaire(
                questionnaire_id=questionnaire.questionnaire_id,
                questionnaire_version=questionnaire.questionnaire_version,
                questionnaire_name=questionnaire.questionnaire_name,
                wordpress_id=questionnaire.wordpress_id,
                is_active=questionnaire.is_active,
                tags=questionnaire.tags,
                questionnaire_hash=questionnaire.questionnaire_hash,
            )
            new_questionnaires.append(new_questionnaire)
        self.session.add_all(new_questionnaires)
        await self._flush(operation="create")
        return new_questionnaires

    async def get_all_questionnaires(self) -> list[Questionnaire]:
        query = select(Questionnaire)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> Questionnaire | None:
        return await self._get(Questionnaire, (questionnaire_id, questionnaire_version))

    async def update_questionnaire(
        self, questionnaire_id: int, questionnaire_version: int, new_data: QuestionnaireUpdate
    ) -> Questionnaire | None:
        values = new_data.model_dump(exclude_unset=True, exclude_none=True)
        if not values:
            return await self.get_questionnaire(questionnaire_id, questionnaire_version)
        query = (
            update(Questionnaire)
            .where(
                and_(
                    Questionnaire.questionnaire_id == questionnaire_id,
                    Questionnaire.questionnaire_version == questionnaire_version,
                )
            )
            .values(**values)
            .returning(Questionnaire)
        )
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> bool:
        questionnaire = await self.get_questionnaire(questionnaire_id, questionnaire_version)
        if questionnaire is None:
            return False
        await self._delete(questionnaire)
        return True

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int) -> Questionnaire | None:
        query = (
            select(Questionnaire)
            .options(selectinload(Questionnaire.questions))
            .where(
                and_(
                    Questionnaire.questionnaire_id == questionnaire_id,
                    Questionnaire.questionnaire_version == questionnaire_version,
                )
            )
        )
        result = await self._execute(query, operation="read")
        return result.scalars().first()

    async def get_latest_versions(self) -> list[Questionnaire]:
        """
        Returns a list of Questionnaires, each corresponding to the latest version for a given questionnaire_id.
        """
        subq = (
            select(Questionnaire.questionnaire_id, func.max(Questionnaire.questionnaire_version).label("max_version"))
            .group_by(Questionnaire.questionnaire_id)
            .subquery()
        )

        query = select(Questionnaire).join(
            subq,
            and_(
                Questionnaire.questionnaire_id == subq.c.questionnaire_id,
                Questionnaire.questionnaire_version == subq.c.max_version,
            ),
        )
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def deactivate_all_by_ids(self, questionnaire_ids: list[int]) -> int:
        """
        Set is_active = False for all questionnaires with questionnaire_id in the provided list.
        """
        query = (
            update(Questionnaire).where(Questionnaire.questionnaire_id.in_(questionnaire_ids)).values(is_active=False)
        )
        result = await self._execute(query, operation="update")
        if not isinstance(result, CursorResult):
            return 0
        return max(result.rowcount, 0)

    async def activate_version(self, questionnaire_id: int, questionnaire_version: int) -> None:
        """Make exactly one existing version active for a questionnaire."""

        await self._execute(
            update(Questionnaire).where(Questionnaire.questionnaire_id == questionnaire_id).values(is_active=False),
            operation="update",
        )
        await self._execute(
            update(Questionnaire)
            .where(
                and_(
                    Questionnaire.questionnaire_id == questionnaire_id,
                    Questionnaire.questionnaire_version == questionnaire_version,
                )
            )
            .values(is_active=True),
            operation="update",
        )
