from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.questions import Question
from src.schemas.questions import QuestionCreate, QuestionUpdate

from .base import BaseRepository


class QuestionRepository(BaseRepository):
    entity_name = "question"

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def create_question(self, question: QuestionCreate) -> Question:
        new_question = Question(
            questionnaire_id=question.questionnaire_id,
            questionnaire_version=question.questionnaire_version,
            question=question.question,
            question_order=question.question_order,
            answer_options=[option.model_dump(mode="json") for option in question.answer_options],
            answer_type=question.answer_type,
            dependencies=question.dependencies.model_dump(),
            wordpress_id=question.wordpress_id,
        )
        self.session.add(new_question)
        await self._flush(operation="create")
        return new_question

    async def create_all_questions(self, questions: list[QuestionCreate]) -> list[Question]:
        new_questions = []
        for question in questions:
            new_question = Question(
                questionnaire_id=question.questionnaire_id,
                questionnaire_version=question.questionnaire_version,
                question=question.question,
                question_order=question.question_order,
                answer_options=[option.model_dump(mode="json") for option in question.answer_options],
                answer_type=question.answer_type,
                dependencies=question.dependencies.model_dump(),
                wordpress_id=question.wordpress_id,
            )
            new_questions.append(new_question)
        self.session.add_all(new_questions)
        await self._flush(operation="create")
        return new_questions

    async def get_all_questions(self) -> list[Question]:
        query = select(Question)
        result = await self._execute(query, operation="list")
        return list(result.scalars().all())

    async def get_question(self, question_id: int) -> Question | None:
        return await self._get(Question, question_id)

    async def update_question(self, question_id: int, new_data: QuestionUpdate) -> Question | None:
        values = new_data.model_dump(exclude_unset=True, exclude_none=True)
        if "answer_options" in values:
            values["answer_options"] = [option.model_dump(mode="json") for option in new_data.answer_options or []]
        if "dependencies" in values and new_data.dependencies is not None:
            values["dependencies"] = new_data.dependencies.model_dump(mode="json")
        if not values:
            return await self.get_question(question_id)

        query = update(Question).where(Question.question_id == question_id).values(**values).returning(Question)
        result = await self._execute(query, operation="update")
        return result.scalar_one_or_none()

    async def delete_question(self, question_id: int) -> bool:
        question = await self.get_question(question_id)
        if question is None:
            return False
        await self._delete(question)
        return True
