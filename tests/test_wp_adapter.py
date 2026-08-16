from src.extras.wp_adapter import WPToQuestionnaireAdapter
from src.models.wp_fields import WPField
from src.schemas.dependencies import AllAnyEnum, ShowHideEnum


def test_answer_options_keep_labels_and_values() -> None:
    field = WPField(
        id=17,
        options=('a:1:{i:0;a:2:{s:5:"label";s:6:"Choice";s:5:"value";s:1:"A";}}'),
    )

    options = WPToQuestionnaireAdapter._decode_answer_options(field)

    assert len(options) == 1
    assert options[0].label == "Choice"
    assert options[0].value == "A"


def test_missing_dependency_modes_use_safe_defaults() -> None:
    field = WPField(id=17, field_options="a:0:{}")

    dependencies = WPToQuestionnaireAdapter._decode_dependencies(field)

    assert dependencies.show_hide is ShowHideEnum.SHOW
    assert dependencies.all_any is AllAnyEnum.ALL
    assert dependencies.conditions == []
