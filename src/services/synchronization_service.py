import logging
from collections import defaultdict

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
        2. Получает сохранённые версии анкет.
        3. Реактивирует совпавшую версию либо готовит новую.
        4. Деактивирует отсутствующие и устаревшие версии.
        5. Преобразует новые/изменённые формы через адаптер и сохраняет их.
        """
        logger.info("sync_questionnaires started")

        forms_with_hash: list[tuple[WPForm, str]] = await self.wp_form_repository.get_all_forms_with_hash()
        forms_map = {form.id: (form, hsh) for form, hsh in forms_with_hash}

        questionnaires = await self.questionnaire_repository.get_all_questionnaires()
        versions_by_wordpress_id: dict[int, list[Questionnaire]] = defaultdict(list)
        for questionnaire in questionnaires:
            versions_by_wordpress_id[questionnaire.wordpress_id].append(questionnaire)

        to_deactivate = {questionnaire.questionnaire_id for questionnaire in questionnaires}
        to_activate: list[Questionnaire] = []

        adapt_data: list[tuple[WPForm, Questionnaire | None, str]] = []
        for form_id, (wp_form, hsh) in forms_map.items():
            versions = versions_by_wordpress_id.get(form_id, [])
            matching_version = next(
                (version for version in versions if version.questionnaire_hash == hsh),
                None,
            )
            if matching_version is not None:
                to_deactivate.discard(matching_version.questionnaire_id)
                if not matching_version.is_active:
                    to_activate.append(matching_version)
                continue

            latest_version = max(
                versions,
                key=lambda version: version.questionnaire_version,
                default=None,
            )
            adapt_data.append((wp_form, latest_version, hsh))

        if to_deactivate:
            logger.info("Deactivating questionnaires: %s", to_deactivate)
            await self.questionnaire_repository.deactivate_all_by_ids(list(to_deactivate))

        for questionnaire in to_activate:
            logger.info(
                "Reactivating questionnaire %s version %s",
                questionnaire.questionnaire_id,
                questionnaire.questionnaire_version,
            )
            await self.questionnaire_repository.activate_version(
                questionnaire.questionnaire_id,
                questionnaire.questionnaire_version,
            )

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
