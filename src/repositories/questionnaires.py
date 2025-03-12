from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.models.questionnaires import Questionnaire


class QuestionnaireRepository:
    def __init__(self, session):
        self.session = session

    async def create_questionnaire(self, questionnaire):
        new_questionnaire = Questionnaire(
            questionnaire_version=questionnaire.questionnaire_version,
            questionnaire_name=questionnaire.questionnaire_name,
            wordpress_id=questionnaire.wordpress_id,
            questionnaire_hash=questionnaire.questionnaire_hash
        )
        self.session.add(new_questionnaire)
        await self.session.flush()
        return new_questionnaire

    async def get_all_questionnaires(self):
        query = select(Questionnaire)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_questionnaire(self, questionnaire_id: int, questionnaire_version: int):
        return await self.session.get(Questionnaire, (questionnaire_id, questionnaire_version))

    async def update_questionnaire(self, questionnaire_id: int, questionnaire_version: int, new_data):
        query = (
            update(Questionnaire)
            .where(
                (Questionnaire.questionnaire_id == questionnaire_id) &
                (Questionnaire.questionnaire_version == questionnaire_version)
            )
            .values(
                questionnaire_name=new_data.questionnaire_name,
                wordpress_id=new_data.wordpress_id,
                questionnaire_hash=new_data.questionnaire_hash
            )
            .returning(Questionnaire)
        )
        res = await self.session.execute(query)
        return res.scalar()

    async def delete_questionnaire(self, questionnaire_id: int, questionnaire_version: int):
        questionnaire = await self.get_questionnaire(questionnaire_id, questionnaire_version)
        if questionnaire:
            await self.session.delete(questionnaire)

    async def get_questionnaire_detail(self, questionnaire_id: int, questionnaire_version: int) -> Questionnaire | None:
        query = (
            select(Questionnaire)
            .options(selectinload(Questionnaire.questions))
            .where(
                (Questionnaire.questionnaire_id == questionnaire_id) &
                (Questionnaire.questionnaire_version == questionnaire_version)
            )
        )
        result = await self.session.execute(query)
        return result.scalars().first()
