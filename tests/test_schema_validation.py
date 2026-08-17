import pytest
from pydantic import ValidationError

from src.schemas.questionnaires import QuestionnaireUpdate
from src.schemas.questions import QuestionUpdate


@pytest.mark.parametrize("invalid_id", [0, -1])
def test_question_update_rejects_nonpositive_wordpress_ids(invalid_id: int) -> None:
    with pytest.raises(ValidationError):
        QuestionUpdate(wordpress_id=invalid_id)


@pytest.mark.parametrize("invalid_id", [0, -1])
def test_questionnaire_update_rejects_nonpositive_wordpress_ids(invalid_id: int) -> None:
    with pytest.raises(ValidationError):
        QuestionnaireUpdate(wordpress_id=invalid_id)
