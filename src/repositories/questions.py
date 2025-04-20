from sqlalchemy import select, update

from src.models.questions import Question
from src.schemas.questions import QuestionCreate, QuestionUpdate


class QuestionRepository:
    def __init__(self, session):
        self.session = session

    async def create_question(self, question: QuestionCreate) -> Question:
        new_question = Question(
            questionnaire_id=question.questionnaire_id,
            questionnaire_version=question.questionnaire_version,
            question=question.question,
            question_order=question.question_order,
            answers=question.answers,
            answer_type=question.answer_type,
            dependencies=question.dependencies.model_dump(),
            wordpress_id=question.wordpress_id
        )
        self.session.add(new_question)
        await self.session.flush()
        return new_question

    async def create_all_questions(self, questions: list[QuestionCreate]) -> list[Question]:
        new_questions = []
        for question in questions:
            new_question = Question(
                questionnaire_id=question.questionnaire_id,
                questionnaire_version=question.questionnaire_version,
                question=question.question,
                question_order=question.question_order,
                answers=question.answers,
                answer_type=question.answer_type,
                dependencies=question.dependencies.model_dump(),
                wordpress_id=question.wordpress_id
            )
            new_questions.append(new_question)
        self.session.add_all(new_questions)
        await self.session.flush()
        return new_questions

    async def get_all_questions(self) -> list[Question]:
        query = select(Question)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_question(self, question_id: int) -> Question | None:
        return await self.session.get(Question, question_id)

    async def update_question(self, question_id: int, new_data: QuestionUpdate) -> Question | None:
        query = (
            update(Question)
            .where(Question.question_id == question_id)
            .values(
                question=new_data.question,
                question_order=new_data.question_order,
                answers=new_data.answers,
                answer_type=new_data.answer_type,
                dependencies=new_data.dependencies.model_dump(),
                wordpress_id=new_data.wordpress_id
            )
            .returning(Question)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_question(self, question_id: int) -> None:
        question = await self.get_question(question_id)
        if question:
            await self.session.delete(question)
