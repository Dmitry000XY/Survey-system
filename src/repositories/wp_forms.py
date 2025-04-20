from sqlalchemy import select, func, cast, String
from sqlalchemy.orm import selectinload

from src.models.wp_forms import WPForm
from src.models.wp_fields import WPField


class WPFormRepository:
    def __init__(self, session):
        self.session = session

    async def get_all_forms(self) -> list[WPForm]:
        query = select(WPForm)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_form(self, form_id: int) -> WPForm | None:
        return await self.session.get(WPForm, form_id)

    async def get_all_forms_with_hash(self) -> list[tuple[WPForm, str]]:
        """
        Возвращает список кортежей (WPForm, questionnaire_hash), где questionnaire_hash вычисляется как
        SHA2( CONCAT( <данные из WPForm>, GROUP_CONCAT( CONCAT( <данные из WPField> ) ) ), 512)
        При этом все NULL приводятся к '' через COALESCE.
        Также, форма загружается со всеми связанными WPField через relationship.
        """
        # Поля из WPForm
        form_id = func.coalesce(cast(WPForm.id, String), '')
        form_key = func.coalesce(WPForm.form_key, '')
        form_name = func.coalesce(WPForm.name, '')
        form_descr = func.coalesce(WPForm.description, '')
        form_parent = func.coalesce(cast(WPForm.parent_form_id, String), '')
        form_logged = func.coalesce(cast(WPForm.logged_in, String), '')
        form_editable = func.coalesce(cast(WPForm.editable, String), '')
        form_is_template = func.coalesce(cast(WPForm.is_template, String), '')
        form_default_tpl = func.coalesce(cast(WPForm.default_template, String), '')
        form_status = func.coalesce(WPForm.status, '')
        form_options = func.coalesce(WPForm.options, '')
        form_created = func.coalesce(cast(WPForm.created_at, String), '')

        # То же самое для каждого поля из WPField внутри group_concat
        field_concat = func.group_concat(
            func.concat(
                func.coalesce(cast(WPField.id, String), ''),
                func.coalesce(WPField.field_key, ''),
                func.coalesce(WPField.name, ''),
                func.coalesce(WPField.description, ''),
                func.coalesce(WPField.type, ''),
                func.coalesce(WPField.default_value, ''),
                func.coalesce(WPField.options, ''),
                func.coalesce(cast(WPField.field_order, String), ''),
                func.coalesce(cast(WPField.required, String), ''),
                func.coalesce(WPField.field_options, ''),
                func.coalesce(cast(WPField.form_id, String), ''),
                func.coalesce(cast(WPField.created_at, String), '')
            )
        )

        # Собираем всё вместе и считаем SHA2(..., 512)
        questionnaire_hash = func.sha2(
            func.concat(
                form_id, form_key, form_name, form_descr, form_parent, form_logged, form_editable,
                form_is_template, form_default_tpl, form_status, form_options, form_created,
                field_concat
            ),
            512
        ).label("questionnaire_hash")

        query = (
            select(WPForm, questionnaire_hash)
            .outerjoin(WPField, WPField.form_id == WPForm.id)
            .options(selectinload(WPForm.fields))
            .group_by(WPForm.id)
        )
        result = await self.session.execute(query)
        return result.all()
