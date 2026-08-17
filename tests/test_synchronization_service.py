import asyncio
from src.models.questionnaires import Questionnaire
from src.models.wp_forms import WPForm
from src.repositories.questionnaires import QuestionnaireRepository
from src.repositories.wp_forms import WPFormRepository
from src.services.synchronization_service import SynchronizationService


class _QuestionnaireRepositoryStub(QuestionnaireRepository):
    def __init__(self, questionnaire: Questionnaire):
        self.questionnaire = questionnaire
        self.deactivated_ids: list[int] = []
        self.activated_version: tuple[int, int] | None = None

    async def get_all_questionnaires(self) -> list[Questionnaire]:
        return [self.questionnaire]

    async def deactivate_all_by_ids(self, questionnaire_ids: list[int]) -> int:
        self.deactivated_ids.extend(questionnaire_ids)
        return len(questionnaire_ids)

    async def activate_version(self, questionnaire_id: int, questionnaire_version: int) -> None:
        self.activated_version = questionnaire_id, questionnaire_version


class _WPFormRepositoryStub(WPFormRepository):
    def __init__(self, form: WPForm, questionnaire_hash: str):
        self.form = form
        self.questionnaire_hash = questionnaire_hash

    async def get_all_forms_with_hash(self) -> list[tuple[WPForm, str]]:
        return [(self.form, self.questionnaire_hash)]


def test_sync_reactivates_an_existing_matching_version() -> None:
    questionnaire_hash = "a" * 64
    questionnaire = Questionnaire(
        questionnaire_id=3,
        questionnaire_version=2,
        questionnaire_name="Test questionnaire",
        wordpress_id=17,
        tags=[],
        questionnaire_hash=questionnaire_hash,
        is_active=False,
    )
    form = WPForm(id=17)
    questionnaire_repository = _QuestionnaireRepositoryStub(questionnaire)
    wp_form_repository = _WPFormRepositoryStub(form, questionnaire_hash)
    service = SynchronizationService(
        questionnaire_repository,
        wp_form_repository,
    )

    asyncio.run(service.sync_questionnaires())

    assert questionnaire_repository.deactivated_ids == []
    assert questionnaire_repository.activated_version == (3, 2)
