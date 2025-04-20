from sqlalchemy import select, update, func, and_
from sqlalchemy.orm import selectinload

from src.models import Question
from src.models.questionnaires import Questionnaire
from src.schemas.questionnaires import QuestionnaireCreate, QuestionnaireUpdate, QuestionnaireCreateWithQuestions, \
    QuestionnaireCreateWithQuestionsNew


class QuestionnaireRepository:
    def __init__(self, session):
        self.session = session

    async def create_questionnaire(self, questionnaire: QuestionnaireCreate) -> Questionnaire:
        new_questionnaire = Questionnaire(
            questionnaire_id=questionnaire.questionnaire_id,
            questionnaire_version=questionnaire.questionnaire_version,
            questionnaire_name=questionnaire.questionnaire_name,
            wordpress_id=questionnaire.wordpress_id,
            is_active=questionnaire.is_active,
            questionnaire_hash=questionnaire.questionnaire_hash
        )
        self.session.add(new_questionnaire)
        await self.session.flush()
        return new_questionnaire

    async def create_all_questionnaires_with_questions(self, questionnaires: list[
        QuestionnaireCreateWithQuestions | QuestionnaireCreateWithQuestionsNew]) -> \
            list[Questionnaire]:
        new_questionnaires = []
        for questionnaire in questionnaires:
            # Предполагается, что q.questions - список объектов типа QuestionCreate
            # Конвертируем каждый QuestionCreate в объект модели Question
            questions = []
            for question_data in questionnaire.questions:
                new_question = Question(
                    question=question_data.question,
                    question_order=question_data.question_order,
                    answers=question_data.answers,
                    answer_type=question_data.answer_type,
                    dependencies=question_data.dependencies.model_dump(),
                    wordpress_id=question_data.wordpress_id,
                    # Предполагается, что time_created устанавливается автоматически, либо можно явно указать, если требуется
                )
                questions.append(new_question)
            # Связываем вопросы с анкетой через relationship (cascade="all, delete-orphan" должен быть настроен в модели Questionnaire)
            # Создаем объект анкеты с вложенными вопросами
            questionnaire_kwargs = {
                "questionnaire_name": questionnaire.questionnaire_name,
                "wordpress_id": questionnaire.wordpress_id,
                "is_active": questionnaire.is_active,
                "questionnaire_hash": questionnaire.questionnaire_hash,
                "questions": questions,
            }

            # Если у схемы есть id и version — сразу их добавляем
            if isinstance(questionnaire, QuestionnaireCreateWithQuestions):
                questionnaire_kwargs["questionnaire_id"] = questionnaire.questionnaire_id
                questionnaire_kwargs["questionnaire_version"] = questionnaire.questionnaire_version

            new_questionnaires.append(Questionnaire(**questionnaire_kwargs))
        self.session.add_all(new_questionnaires)
        await self.session.flush()
        return new_questionnaires

    async def create_all_questionnaires(self, questionnaires: list[QuestionnaireCreate]) -> list[Questionnaire]:
        new_questionnaires = []
        for questionnaire in questionnaires:
            new_questionnaire = Questionnaire(
                questionnaire_id=questionnaire.questionnaire_id,
                questionnaire_version=questionnaire.questionnaire_version,
                questionnaire_name=questionnaire.questionnaire_name,
                wordpress_id=questionnaire.wordpress_id,
                is_active=questionnaire.is_active,
                questionnaire_hash=questionnaire.questionnaire_hash
            )
            new_questionnaires.append(new_questionnaire)
        self.session.add_all(new_questionnaires)
        await self.session.flush()
        return new_questionnaires

    async def get_all_questionnaires(self) -> list[Questionnaire]:
        query = select(Questionnaire)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> Questionnaire | None:
        return await self.session.get(Questionnaire, (questionnaire_id, questionnaire_version))

    async def update_questionnaire(self, questionnaire_id: int, questionnaire_version: int,
                                   new_data: QuestionnaireUpdate) -> Questionnaire | None:
        query = (
            update(Questionnaire)
            .where(
                and_(
                    Questionnaire.questionnaire_id == questionnaire_id,
                    Questionnaire.questionnaire_version == questionnaire_version
                )
            )
            .values(
                questionnaire_name=new_data.questionnaire_name,
                wordpress_id=new_data.wordpress_id,
                is_active=new_data.is_active,
                questionnaire_hash=new_data.questionnaire_hash
            )
            .returning(Questionnaire)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int) -> None:
        questionnaire = await self.get_questionnaire(questionnaire_id, questionnaire_version)
        if questionnaire:
            await self.session.delete(questionnaire)

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int) -> Questionnaire | None:
        query = (
            select(Questionnaire)
            .options(selectinload(Questionnaire.questions))
            .where(
                and_(
                    Questionnaire.questionnaire_id == questionnaire_id,
                    Questionnaire.questionnaire_version == questionnaire_version
                )
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_latest_versions(self) -> list[Questionnaire]:
        """
        Returns a list of Questionnaires, each corresponding to the latest version for a given questionnaire_id.
        """
        subq = (
            select(
                Questionnaire.questionnaire_id,
                func.max(Questionnaire.questionnaire_version).label("max_version")
            )
            .group_by(Questionnaire.questionnaire_id)
            .subquery()
        )

        query = (
            select(Questionnaire)
            .join(subq, and_(
                Questionnaire.questionnaire_id == subq.c.questionnaire_id,
                Questionnaire.questionnaire_version == subq.c.max_version
            ))
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def deactivate_all_by_ids(self, questionnaire_ids: list[int]) -> None:
        """
        Set is_active = False for all questionnaires with questionnaire_id in the provided list.
        """
        query = (
            update(Questionnaire)
            .where(Questionnaire.questionnaire_id.in_(questionnaire_ids))
            .values(is_active=False)
        )
        await self.session.execute(query)
