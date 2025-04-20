import logging

from src.models.wp_forms import WPForm
from src.models.questionnaires import Questionnaire
from src.extras.wp_adapter import WPToQuestionnaireAdapter
from src.repositories.questionnaires import QuestionnaireRepository
from src.repositories.wp_forms import WPFormRepository

logger = logging.getLogger(__name__)


class SynchronizationService:
    def __init__(self, questionnaire_repository: QuestionnaireRepository, wp_form_repository: WPFormRepository):
        self.questionnaire_repository = questionnaire_repository
        self.wp_form_repository = wp_form_repository
        self.adapter = WPToQuestionnaireAdapter()

    async def sync_questionnaires(self) -> None:
        """
        Синхронизирует анкетные данные:
        1. Получает все формы с предвычисленным хешем.
        2. Получает последние версии анкет.
        3. Определяет, какие анкеты деактивировать, а какие создать/обновить.
        4. Деактивирует устаревшие.
        5. Преобразует новые/изменённые через адаптер и сохраняет их.
        """
        logger.info("sync_questionnaires started")

        forms_with_hash: list[tuple[WPForm, str]] = await self.wp_form_repository.get_all_forms_with_hash()
        forms_map = {form.id: (form, hsh) for form, hsh in forms_with_hash}

        latest_questionnaires: list[Questionnaire] = await self.questionnaire_repository.get_latest_versions()
        questionnaire_map = {q.wordpress_id: q for q in latest_questionnaires}
        to_deactivate = {q.questionnaire_id for q in latest_questionnaires}

        adapt_data: list[tuple[WPForm, Questionnaire | None, str]] = []
        for form_id, (wp_form, hsh) in forms_map.items():
            existing = questionnaire_map.get(form_id)
            if existing and existing.questionnaire_hash == hsh:
                to_deactivate.discard(existing.questionnaire_id)
            else:
                adapt_data.append((wp_form, existing, hsh))

        if to_deactivate:
            logger.info("Deactivating questionnaires: %s", to_deactivate)
            await self.questionnaire_repository.deactivate_all_by_ids(list(to_deactivate))

        if adapt_data:
            logger.info("Adapting %d forms", len(adapt_data))
            adapted = self.adapter.adapt_all(adapt_data)
            logger.info("Creating/updating %d questionnaires", len(adapted))
            await self.questionnaire_repository.create_all_questionnaires_with_questions(adapted)

        logger.info("sync_questionnaires completed")

    async def sync_all(self) -> None:
        """
        Запуск всех синхронизаций.
        """
        logger.info("Full synchronization started")
        await self.sync_questionnaires()
        logger.info("Full synchronization completed")
